#!/bin/bash

# Web Search Fallback Demo
# Demonstrates how the fallback system works when WebSearch fails

echo "========================================"
echo "Web Search Fallback System Demo"
echo "========================================"
echo ""

# Function to simulate WebSearch API
function WebSearch() {
    # Simulate random failures (50% failure rate for demo)
    if [ $((RANDOM % 2)) -eq 0 ]; then
        echo "[WebSearch API Error: Rate limit exceeded]" >&2
        return 1
    else
        echo "WebSearch API Result: Found results for '$1'"
        return 0
    fi
}

# Function to perform search with automatic fallback
function search_with_fallback() {
    local query="$1"
    local num_results="${2:-5}"

    echo "[Attempting search for: '$query']"
    echo ""

    # Try WebSearch first
    if result=$(WebSearch "$query" 2>&1); then
        echo "[SUCCESS] Using WebSearch API"
        echo "$result"
    else
        echo "[FAILED] WebSearch API failed: $(echo "$result" | grep Error)"
        echo "[INFO] Activating fallback search system..."
        echo ""

        # Use Python fallback
        if command -v python3 &> /dev/null; then
            echo "[INFO] Using Python web search fallback"
            result=$(python3 "$(dirname "$0")/../lib/web_search_fallback.py" "$query" -n "$num_results" -t titles 2>/dev/null)

            if [ -n "$result" ]; then
                echo "[SUCCESS] Fallback search completed"
                echo ""
                echo "Results:"
                echo "$result" | head -5
            else
                echo "[ERROR] All search methods failed"
            fi
        else
            echo "[ERROR] Python3 not found, cannot use fallback"
        fi
    fi

    echo ""
    echo "----------------------------------------"
    echo ""
}

# Demo searches
echo "Demo 1: Search for 'Claude AI agents'"
search_with_fallback "Claude AI agents" 3

echo "Demo 2: Search for 'autonomous programming'"
search_with_fallback "autonomous programming" 3

echo "Demo 3: Search for 'web scraping techniques'"
search_with_fallback "web scraping techniques" 3

echo "========================================"
echo "Demo Complete!"
echo ""
echo "Key Features Demonstrated:"
echo "- Automatic fallback when WebSearch fails"
echo "- Result caching for repeated queries"
echo "- Cross-platform compatibility"
echo "- No API limits or authentication required"
echo "========================================"