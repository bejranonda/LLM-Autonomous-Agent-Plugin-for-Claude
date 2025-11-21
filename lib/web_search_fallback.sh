#!/bin/bash

# Web Search Fallback Script
# Provides bash+curl web search when WebSearch API fails
# Usage: ./web_search_fallback.sh "search query" [options]

set -euo pipefail

# Configuration
CACHE_DIR=".claude-patterns/search-cache"
CACHE_DURATION=60  # minutes
DEFAULT_RESULTS=10
USER_AGENTS=(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
)

# Function to URL encode strings
url_encode() {
    local string="${1}"
    python3 -c "import urllib.parse; print(urllib.parse.quote('${string}'))"
}

# Function to clean HTML entities
clean_html() {
    sed 's/&#x27;/'"'"'/g; s/&amp;/\&/g; s/&lt;/</g; s/&gt;/>/g; s/&quot;/"/g'
}

# Function to get random user agent
get_user_agent() {
    echo "${USER_AGENTS[$RANDOM % ${#USER_AGENTS[@]}]}"
}

# Function to check cache
check_cache() {
    local query_hash="${1}"
    local cache_file="${CACHE_DIR}/${query_hash}.txt"

    if [ -f "$cache_file" ]; then
        if [ $(find "$cache_file" -mmin -${CACHE_DURATION} 2>/dev/null | wc -l) -gt 0 ]; then
            cat "$cache_file"
            return 0
        fi
    fi
    return 1
}

# Function to save to cache
save_cache() {
    local query_hash="${1}"
    local content="${2}"
    mkdir -p "$CACHE_DIR"
    echo "$content" > "${CACHE_DIR}/${query_hash}.txt"
}

# Function to search DuckDuckGo
search_duckduckgo() {
    local query="${1}"
    local num_results="${2:-$DEFAULT_RESULTS}"
    local encoded_query=$(url_encode "$query")
    local user_agent=$(get_user_agent)

    curl -s -A "$user_agent" \
        "https://html.duckduckgo.com/html/?q=${encoded_query}" \
        | grep -o '<a[^>]*class="result__a"[^>]*href="[^"]*"[^>]*>[^<]*</a>' \
        | head -n "$num_results" \
        | while IFS= read -r line; do
            # Extract URL and title
            url=$(echo "$line" | grep -o 'href="[^"]*"' | sed 's/href="//; s/"//')
            title=$(echo "$line" | sed 's/<[^>]*>//g' | clean_html)
            echo "[TITLE] $title"
            echo "[URL] $url"
            echo "---"
        done
}

# Function to search Searx (JSON format)
search_searx() {
    local query="${1}"
    local num_results="${2:-$DEFAULT_RESULTS}"
    local encoded_query=$(url_encode "$query")

    local result=$(curl -s "https://searx.be/search?q=${encoded_query}&format=json" 2>/dev/null || echo "{}")

    if command -v jq &> /dev/null; then
        echo "$result" | jq -r ".results[:${num_results}] | .[] | \"[TITLE] \\(.title)\\n[URL] \\(.url)\\n---\""
    else
        # Fallback to Python if jq is not available
        echo "$result" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    results = data.get('results', [])[:${num_results}]
    for r in results:
        print(f\"[TITLE] {r.get('title', 'N/A')}\")
        print(f\"[URL] {r.get('url', 'N/A')}\")
        print('---')
except:
    pass
"
    fi
}

# Function to perform search with fallback
perform_search() {
    local query="${1}"
    local num_results="${2:-$DEFAULT_RESULTS}"
    local use_cache="${3:-true}"

    # Generate cache key
    local query_hash=$(echo -n "$query" | md5sum | cut -d' ' -f1)

    # Check cache if enabled
    if [ "$use_cache" = "true" ]; then
        if cached_result=$(check_cache "$query_hash"); then
            echo "[CACHED RESULT]"
            echo "$cached_result"
            return 0
        fi
    fi

    # Try DuckDuckGo first
    echo "[Searching DuckDuckGo...]" >&2
    local result=$(search_duckduckgo "$query" "$num_results" 2>/dev/null)

    if [ -z "$result" ] || [ $(echo "$result" | wc -l) -lt 3 ]; then
        # Fallback to Searx
        echo "[DuckDuckGo failed, trying Searx...]" >&2
        result=$(search_searx "$query" "$num_results" 2>/dev/null)
    fi

    if [ -n "$result" ]; then
        # Save to cache if enabled
        if [ "$use_cache" = "true" ]; then
            save_cache "$query_hash" "$result"
        fi
        echo "$result"
        return 0
    else
        echo "[ERROR] All search methods failed" >&2
        return 1
    fi
}

# Function to extract specific content type
extract_content() {
    local content="${1}"
    local type="${2}"

    case "$type" in
        "titles")
            echo "$content" | grep "^\[TITLE\]" | sed 's/^\[TITLE\] //'
            ;;
        "urls")
            echo "$content" | grep "^\[URL\]" | sed 's/^\[URL\] //'
            ;;
        "json")
            # Convert to JSON format
            echo "$content" | awk '
                BEGIN { print "[" }
                /^\[TITLE\]/ {
                    if (NR > 1 && title) print ",";
                    title = substr($0, 9);
                    gsub(/"/, "\\\"", title);
                }
                /^\[URL\]/ {
                    url = substr($0, 7);
                    gsub(/"/, "\\\"", url);
                    printf "  {\"title\": \"%s\", \"url\": \"%s\"}", title, url;
                }
                END { print "\n]" }
            '
            ;;
        *)
            echo "$content"
            ;;
    esac
}

# Main function
main() {
    local query=""
    local num_results=$DEFAULT_RESULTS
    local use_cache="true"
    local output_type="full"
    local verbose="false"

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -n|--num)
                num_results="$2"
                shift 2
                ;;
            -t|--type)
                output_type="$2"
                shift 2
                ;;
            --no-cache)
                use_cache="false"
                shift
                ;;
            -v|--verbose)
                verbose="true"
                shift
                ;;
            -h|--help)
                cat << EOF
Web Search Fallback Script
Usage: $0 "search query" [options]

Options:
    -n, --num NUM       Number of results to return (default: $DEFAULT_RESULTS)
    -t, --type TYPE     Output type: full, titles, urls, json (default: full)
    --no-cache          Disable result caching
    -v, --verbose       Enable verbose output
    -h, --help          Show this help message

Examples:
    $0 "python async programming" -n 5
    $0 "machine learning" -t titles
    $0 "web scraping" -t json --no-cache

EOF
                exit 0
                ;;
            *)
                query="$1"
                shift
                ;;
        esac
    done

    # Validate query
    if [ -z "$query" ]; then
        echo "Error: No search query provided" >&2
        echo "Usage: $0 \"search query\" [options]" >&2
        exit 1
    fi

    if [ "$verbose" = "true" ]; then
        echo "[Query: $query]" >&2
        echo "[Results: $num_results]" >&2
        echo "[Cache: $use_cache]" >&2
        echo "[Output: $output_type]" >&2
    fi

    # Perform search
    result=$(perform_search "$query" "$num_results" "$use_cache")

    if [ $? -eq 0 ]; then
        # Extract and display based on output type
        extract_content "$result" "$output_type"
    else
        exit 1
    fi
}

# Run main function if script is executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi