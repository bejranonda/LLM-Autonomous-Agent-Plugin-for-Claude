# Web Search Fallback Integration Guide

## Quick Start

This skill provides robust web search capabilities when the built-in WebSearch tool fails or hits limits.

## Integration in Agents

### Basic Fallback Pattern

```bash
# Try WebSearch first, fallback if it fails
search_query="your search terms"

# Attempt with WebSearch
if result=$(WebSearch "$search_query"); then
    echo "$result"
else
    # Fallback to bash+curl method
    result=$(python3 lib/web_search_fallback.py "$search_query" -n 10 -t json)
    echo "$result"
fi
```

### Advanced Integration with Error Detection

```python
# In Python-based agents
from lib.web_search_fallback import WebSearchFallback

def search_with_fallback(query, num_results=10):
    try:
        # Try primary WebSearch
        return web_search(query)
    except (APILimitError, ValidationError, ToolError) as e:
        # Use fallback
        print(f"WebSearch failed: {e}, using fallback")
        searcher = WebSearchFallback()
        return searcher.search(query, num_results=num_results)
```

### Orchestrator Integration

The orchestrator can automatically delegate to this skill when:

```yaml
trigger_conditions:
  - WebSearch returns error code
  - User mentions "search fallback"
  - Pattern database shows WebSearch failures > 3 in last hour
  - Bulk search operations (> 20 queries)
```

## Usage Patterns

### 1. Rate Limit Mitigation

```bash
# For bulk searches, use fallback with delays
for query in "${queries[@]}"; do
    python3 lib/web_search_fallback.py "$query" -n 5
    sleep 2  # Prevent rate limiting
done
```

### 2. Cross-Platform Compatibility

```bash
# Detect platform and use appropriate method
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    # Windows - use Python
    python3 lib/web_search_fallback.py "$query"
else
    # Unix-like - use bash or Python
    bash lib/web_search_fallback.sh "$query"
fi
```

### 3. Result Parsing

```bash
# Extract only titles
titles=$(python3 lib/web_search_fallback.py "$query" -t titles)

# Get JSON for programmatic use
json_results=$(python3 lib/web_search_fallback.py "$query" -t json)

# Parse JSON with jq if available
echo "$json_results" | jq '.[] | .title'
```

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| Connection timeout | Network issues | Retry with exponential backoff |
| Empty results | Query too specific | Broaden search terms |
| HTML parsing fails | Website structure changed | Try alternative search engine |
| Cache permission denied | Directory permissions | Create cache dir with proper permissions |

### Graceful Degradation

```bash
# Multiple fallback levels
search_result=""

# Level 1: WebSearch API
if ! search_result=$(WebSearch "$query" 2>/dev/null); then
    # Level 2: DuckDuckGo
    if ! search_result=$(python3 lib/web_search_fallback.py "$query" -e duckduckgo 2>/dev/null); then
        # Level 3: Searx
        if ! search_result=$(python3 lib/web_search_fallback.py "$query" -e searx 2>/dev/null); then
            # Level 4: Return error message
            search_result="All search methods failed. Please try again later."
        fi
    fi
fi

echo "$search_result"
```

## Performance Optimization

### Caching Strategy

```bash
# Use cache for repeated queries
python3 lib/web_search_fallback.py "$query"  # First query cached

# Subsequent queries use cache (60 min TTL)
python3 lib/web_search_fallback.py "$query"  # Returns instantly

# Force fresh results when needed
python3 lib/web_search_fallback.py "$query" --no-cache
```

### Parallel Searches

```bash
# Run multiple searches in parallel
search_terms=("term1" "term2" "term3")

for term in "${search_terms[@]}"; do
    python3 lib/web_search_fallback.py "$term" -n 5 &
done
wait  # Wait for all searches to complete
```

## Agent-Specific Examples

### For research-analyzer Agent

```bash
# Comprehensive research with fallback
research_topic="quantum computing applications"

# Get multiple perspectives
ddg_results=$(python3 lib/web_search_fallback.py "$research_topic" -e duckduckgo -n 15)
searx_results=$(python3 lib/web_search_fallback.py "$research_topic" -e searx -n 10)

# Combine and deduplicate results
echo "$ddg_results" > /tmp/research_results.txt
echo "$searx_results" >> /tmp/research_results.txt
```

### For background-task-manager Agent

```bash
# Non-blocking search in background
{
    python3 lib/web_search_fallback.py "$query" -n 20 > search_results.txt
    echo "Search completed: $(wc -l < search_results.txt) results found"
} &

# Continue with other tasks while search runs
echo "Search running in background..."
```

## Testing the Integration

### Unit Test

```bash
# Test fallback functionality
test_query="test search fallback"

# Test Python implementation
python3 lib/web_search_fallback.py "$test_query" -n 1 -v

# Test bash implementation
bash lib/web_search_fallback.sh "$test_query" -n 1

# Test cache functionality
python3 lib/web_search_fallback.py "$test_query"  # Creates cache
python3 lib/web_search_fallback.py "$test_query"  # Uses cache

# Verify cache file exists
ls -la .claude-patterns/search-cache/
```

### Integration Test

```bash
# Simulate WebSearch failure and fallback
function test_search_with_fallback() {
    local query="$1"

    # Simulate WebSearch failure
    if false; then  # Always fails
        echo "WebSearch result"
    else
        echo "WebSearch failed, using fallback..." >&2
        python3 lib/web_search_fallback.py "$query" -n 3 -t titles
    fi
}

test_search_with_fallback "integration test"
```

## Monitoring and Logging

### Track Fallback Usage

```python
# In pattern_storage.py integration
pattern = {
    "task_type": "web_search",
    "method_used": "fallback",
    "search_engine": "duckduckgo",
    "success": True,
    "response_time": 2.3,
    "cached": False,
    "timestamp": "2024-01-01T10:00:00"
}
```

### Success Metrics

Monitor these metrics in the pattern database:
- Fallback trigger frequency
- Success rate by search engine
- Average response time
- Cache hit rate
- Error types and frequencies

## Best Practices

1. **Always try WebSearch first** - It's the primary tool
2. **Use caching wisely** - Enable for repeated queries, disable for fresh data
3. **Handle errors gracefully** - Multiple fallback levels
4. **Respect rate limits** - Add delays for bulk operations
5. **Parse results appropriately** - Use JSON for structured data
6. **Log fallback usage** - Track patterns for optimization
7. **Test regularly** - HTML structures may change

## Troubleshooting

### Debug Mode

```bash
# Enable verbose output for debugging
python3 lib/web_search_fallback.py "debug query" -v

# Check cache status
ls -la .claude-patterns/search-cache/
find .claude-patterns/search-cache/ -type f -mmin -60  # Files < 60 min old

# Test specific search engine
python3 lib/web_search_fallback.py "test" -e duckduckgo -v
python3 lib/web_search_fallback.py "test" -e searx -v
```

### Common Issues

1. **No results returned**
   - Check internet connectivity
   - Verify search engine is accessible
   - Try different search terms

2. **Cache not working**
   - Check directory permissions
   - Verify disk space available
   - Clear old cache files

3. **Parsing errors**
   - HTML structure may have changed
   - Update parsing patterns in script
   - Try alternative search engine