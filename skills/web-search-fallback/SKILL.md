---
name: web-search-fallback
description: Bash+curl web search fallback for when WebSearch API fails or hits limits
category: research
requires_approval: false
---

# Web Search Fallback Skill

## Overview
Provides robust web search capabilities using Bash+curl HTML scraping when the built-in WebSearch tool fails, errors, or hits usage limits. This skill uses lightweight HTML endpoints from search engines to retrieve results without API dependencies.

## When to Apply
- WebSearch returns validation or tool errors
- You hit daily or session usage limits
- You need fine-grained control over output formatting
- You want custom filtering, scraping, or data extraction
- WebSearch is unavailable or restricted

## Core Capabilities

### Basic Search Template
```bash
curl -s -A "Mozilla/5.0" \
"https://html.duckduckgo.com/html/?q=your+search+terms" \
| grep -o '<a[^>]*class="result__a"[^>]*>[^<]*</a>'
```

### Advanced Search Templates

#### 1. Get Top 10 Result Titles
```bash
curl -s -A "Mozilla/5.0" \
"https://html.duckduckgo.com/html/?q=query" \
| grep -o '<a[^>]*class="result__a"[^>]*>[^<]*</a>' \
| head -10
```

#### 2. Extract Results with Context
```bash
curl -s -A "Mozilla/5.0" \
"https://html.duckduckgo.com/html/?q=query" \
| grep -A 2 -B 2 "keyword"
```

#### 3. Clean HTML Entities
```bash
curl -s -A "Mozilla/5.0" \
"https://html.duckduckgo.com/html/?q=query" \
| grep -o '<a[^>]*class="result__a"[^>]*>[^<]*</a>' \
| sed 's/&#x27;/'"'"'/g; s/&amp;/\&/g; s/&lt;/</g; s/&gt;/>/g'
```

## Implementation Approaches

### DuckDuckGo HTML Interface
**Endpoint**: `https://html.duckduckgo.com/html/`
**Method**: GET with query parameter
**Parsing**: Extract `result__a` class anchors for titles and links

```bash
# Full result extraction with URLs
curl -s -A "Mozilla/5.0" \
"https://html.duckduckgo.com/html/?q=python+async+programming" \
| grep -o '<a[^>]*class="result__a"[^>]*href="[^"]*"[^>]*>[^<]*</a>' \
| sed 's/<a[^>]*href="\([^"]*\)"[^>]*>\([^<]*\)<\/a>/\2 - \1/g'
```

### Searx Instance (Alternative)
**Endpoint**: `https://searx.be/search`
**Method**: GET with format=json for structured data

```bash
# JSON formatted results
curl -s "https://searx.be/search?q=query&format=json" \
| python3 -m json.tool
```

### Result Extraction Patterns

#### Extract Titles Only
```bash
curl -s -A "Mozilla/5.0" \
"https://html.duckduckgo.com/html/?q=query" \
| grep -o '<a[^>]*class="result__a"[^>]*>[^<]*</a>' \
| sed 's/<[^>]*>//g'
```

#### Extract URLs Only
```bash
curl -s -A "Mozilla/5.0" \
"https://html.duckduckgo.com/html/?q=query" \
| grep -o 'href="[^"]*"' \
| sed 's/href="//g; s/"//g' \
| grep -E '^https?://'
```

#### Extract Snippets
```bash
curl -s -A "Mozilla/5.0" \
"https://html.duckduckgo.com/html/?q=query" \
| grep -o '<a[^>]*class="result__snippet"[^>]*>[^<]*</a>' \
| sed 's/<[^>]*>//g'
```

## Error Handling

### Rate Limiting Mitigation
```bash
# Add delay between requests
for query in "term1" "term2" "term3"; do
  curl -s -A "Mozilla/5.0" \
  "https://html.duckduckgo.com/html/?q=$query" \
  | grep -o '<a[^>]*class="result__a"[^>]*>[^<]*</a>' \
  | head -5
  sleep 2  # 2 second delay
done
```

### Fallback Chain
```bash
# Try multiple search engines in sequence
search_query="your search terms"
encoded_query=$(echo "$search_query" | sed 's/ /+/g')

# Try DuckDuckGo first
result=$(curl -s -A "Mozilla/5.0" \
"https://html.duckduckgo.com/html/?q=$encoded_query" 2>/dev/null)

if [ -z "$result" ]; then
  # Fallback to Searx
  result=$(curl -s "https://searx.be/search?q=$encoded_query&format=json" 2>/dev/null)
fi

echo "$result"
```

## Advantages
- ✅ Avoids WebSearch API limits and restrictions
- ✅ Uses lightweight, static HTML endpoints (no JS rendering)
- ✅ Works with standard Unix tools (grep/sed/awk) for custom parsing
- ✅ Compatible across multiple search engines
- ✅ Simple anti-bot bypass using standard user agent headers
- ✅ No authentication or API keys required
- ✅ Cross-platform compatibility (Linux, macOS, Windows with WSL)

## Best Practices

### 1. URL Encoding
Always encode search queries properly:
```bash
encoded=$(python3 -c "import urllib.parse; print(urllib.parse.quote('search terms'))")
curl -s "https://html.duckduckgo.com/html/?q=$encoded"
```

### 2. User Agent Rotation
Use varied user agents to avoid detection:
```bash
agents=(
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
)
ua=${agents[$RANDOM % ${#agents[@]}]}
curl -s -A "$ua" "https://html.duckduckgo.com/html/?q=query"
```

### 3. Result Caching
Cache results to minimize requests:
```bash
cache_dir=".claude-patterns/search-cache"
mkdir -p "$cache_dir"
query_hash=$(echo -n "$query" | md5sum | cut -d' ' -f1)
cache_file="$cache_dir/$query_hash.txt"

if [ -f "$cache_file" ] && [ $(find "$cache_file" -mmin -60) ]; then
  cat "$cache_file"  # Use cached result if less than 60 minutes old
else
  result=$(curl -s -A "Mozilla/5.0" "https://html.duckduckgo.com/html/?q=$query")
  echo "$result" > "$cache_file"
  echo "$result"
fi
```

## Integration with Plugin

This fallback skill can be automatically triggered by:
- The orchestrator when WebSearch fails
- Research agents when API limits are reached
- Background task manager for bulk search operations
- Any agent needing web search capabilities

## Example Usage in Agents

```bash
# In an agent's implementation
if ! web_search_result=$(WebSearch "query"); then
  echo "WebSearch failed, using fallback method..."
  web_search_result=$(bash -c '
    curl -s -A "Mozilla/5.0" \
    "https://html.duckduckgo.com/html/?q=query" \
    | grep -o "<a[^>]*class=\"result__a\"[^>]*>[^<]*</a>" \
    | head -10 \
    | sed "s/<[^>]*>//g"
  ')
fi
```

## Limitations
- HTML structure may change (requires periodic updates)
- Less structured than API responses
- May require additional parsing for complex data extraction
- Subject to rate limiting if overused
- Results may vary in format between search engines

## Maintenance
- Regularly test HTML selectors for changes
- Update parsing patterns as needed
- Monitor success rates in pattern database
- Add new search engine endpoints as backups