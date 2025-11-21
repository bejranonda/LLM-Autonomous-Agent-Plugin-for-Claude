#!/usr/bin/env python3

"""
Web Search Fallback Utility
Provides bash+curl web search capabilities when WebSearch API fails or hits limits.
Compatible with Windows, Linux, and macOS.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Configuration
CACHE_DIR = Path(".claude-patterns/search-cache")
CACHE_DURATION = 60  # minutes
DEFAULT_RESULTS = 10

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
]

# Search engine endpoints
SEARCH_ENGINES = {
    "duckduckgo": {
        "url": "https://html.duckduckgo.com/html/?q={query}",
        "parser": "html_duckduckgo"
    },
    "searx": {
        "url": "https://searx.be/search?q={query}&format=json",
        "parser": "json_searx"
    }
}


class WebSearchFallback:
    """Web search fallback implementation using HTML scraping."""

    def __init__(self, cache_dir: Path = CACHE_DIR, cache_duration: int = CACHE_DURATION):
        self.cache_dir = cache_dir
        self.cache_duration = cache_duration
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_user_agent(self) -> str:
        """Get a random user agent."""
        import random
        return random.choice(USER_AGENTS)

    def url_encode(self, query: str) -> str:
        """URL encode a search query."""
        return urllib.parse.quote(query)

    def clean_html(self, text: str) -> str:
        """Clean common HTML entities."""
        replacements = {
            '&#x27;': "'",
            '&amp;': '&',
            '&lt;': '<',
            '&gt;': '>',
            '&quot;': '"',
            '&nbsp;': ' '
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def get_cache_key(self, query: str) -> str:
        """Generate cache key for a query."""
        return hashlib.md5(query.encode()).hexdigest()

    def check_cache(self, query: str) -> Optional[List[Dict[str, str]]]:
        """Check if cached results exist and are still valid."""
        cache_key = self.get_cache_key(query)
        cache_file = self.cache_dir / f"{cache_key}.json"

        if cache_file.exists():
            # Check if cache is still valid
            file_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
            if datetime.now() - file_time < timedelta(minutes=self.cache_duration):
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except (json.JSONDecodeError, IOError):
                    pass
        return None

    def save_cache(self, query: str, results: List[Dict[str, str]]) -> None:
        """Save results to cache."""
        cache_key = self.get_cache_key(query)
        cache_file = self.cache_dir / f"{cache_key}.json"

        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
        except IOError:
            pass  # Silently fail cache write

    def fetch_url(self, url: str, headers: Optional[Dict[str, str]] = None) -> Optional[str]:
        """Fetch URL content with error handling."""
        if headers is None:
            headers = {'User-Agent': self.get_user_agent()}

        try:
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=10) as response:
                return response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"[ERROR] Failed to fetch URL: {e}", file=sys.stderr)
            return None

    def parse_duckduckgo_html(self, html: str, num_results: int) -> List[Dict[str, str]]:
        """Parse DuckDuckGo HTML results."""
        results = []

        # Extract result links and titles
        pattern = r'<a[^>]*class="result__a"[^>]*href="([^"]*)"[^>]*>([^<]*)</a>'
        matches = re.findall(pattern, html)

        for url, title in matches[:num_results]:
            if url and title:
                results.append({
                    'title': self.clean_html(title.strip()),
                    'url': url.strip()
                })

        # Also try to extract snippets if available
        snippet_pattern = r'<a[^>]*class="result__snippet"[^>]*>([^<]*)</a>'
        snippets = re.findall(snippet_pattern, html)

        for i, snippet in enumerate(snippets[:len(results)]):
            if i < len(results):
                results[i]['snippet'] = self.clean_html(snippet.strip())

        return results

    def parse_searx_json(self, json_str: str, num_results: int) -> List[Dict[str, str]]:
        """Parse Searx JSON results."""
        try:
            data = json.loads(json_str)
            results = []

            for item in data.get('results', [])[:num_results]:
                result = {
                    'title': item.get('title', 'N/A'),
                    'url': item.get('url', 'N/A')
                }
                if 'content' in item:
                    result['snippet'] = item['content']
                results.append(result)

            return results
        except json.JSONDecodeError:
            return []

    def search_engine(self, engine: str, query: str, num_results: int) -> Optional[List[Dict[str, str]]]:
        """Search using a specific engine."""
        if engine not in SEARCH_ENGINES:
            return None

        config = SEARCH_ENGINES[engine]
        encoded_query = self.url_encode(query)
        url = config['url'].format(query=encoded_query)

        content = self.fetch_url(url)
        if not content:
            return None

        # Parse based on engine type
        if config['parser'] == 'html_duckduckgo':
            return self.parse_duckduckgo_html(content, num_results)
        elif config['parser'] == 'json_searx':
            return self.parse_searx_json(content, num_results)

        return None

    def search(self, query: str, num_results: int = DEFAULT_RESULTS,
               use_cache: bool = True, engine: Optional[str] = None) -> List[Dict[str, str]]:
        """Perform search with fallback and caching."""

        # Check cache if enabled
        if use_cache:
            cached = self.check_cache(query)
            if cached:
                print("[Using cached results]", file=sys.stderr)
                return cached[:num_results]

        results = []

        # If specific engine requested
        if engine:
            results = self.search_engine(engine, query, num_results) or []
        else:
            # Try engines in order
            for engine_name in ['duckduckgo', 'searx']:
                print(f"[Searching {engine_name}...]", file=sys.stderr)
                results = self.search_engine(engine_name, query, num_results)
                if results:
                    break
                time.sleep(1)  # Small delay between engines

        # Save to cache if we got results
        if results and use_cache:
            self.save_cache(query, results)

        return results

    def format_results(self, results: List[Dict[str, str]], format_type: str = 'full') -> str:
        """Format search results for display."""
        if not results:
            return "[No results found]"

        output = []

        if format_type == 'titles':
            for r in results:
                output.append(r.get('title', 'N/A'))
        elif format_type == 'urls':
            for r in results:
                output.append(r.get('url', 'N/A'))
        elif format_type == 'json':
            return json.dumps(results, indent=2, ensure_ascii=False)
        else:  # full
            for i, r in enumerate(results, 1):
                output.append(f"[Result {i}]")
                output.append(f"Title: {r.get('title', 'N/A')}")
                output.append(f"URL: {r.get('url', 'N/A')}")
                if 'snippet' in r:
                    output.append(f"Snippet: {r.get('snippet', 'N/A')}")
                output.append("-" * 40)

        return '\n'.join(output)


def run_bash_fallback(query: str, num_results: int = DEFAULT_RESULTS) -> Optional[str]:
    """Run bash version of web search fallback (cross-platform)."""
    script_path = Path(__file__).parent / "web_search_fallback.sh"

    if not script_path.exists():
        return None

    try:
        # Make script executable on Unix-like systems
        if sys.platform != 'win32':
            os.chmod(script_path, 0o755)

        # Run the bash script
        result = subprocess.run(
            ['bash', str(script_path), query, '-n', str(num_results)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return result.stdout
        else:
            print(f"[Bash fallback error]: {result.stderr}", file=sys.stderr)
            return None
    except Exception as e:
        print(f"[Bash fallback failed]: {e}", file=sys.stderr)
        return None


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description='Web Search Fallback - Alternative search when WebSearch API fails'
    )
    parser.add_argument('query', help='Search query')
    parser.add_argument('-n', '--num', type=int, default=DEFAULT_RESULTS,
                        help=f'Number of results (default: {DEFAULT_RESULTS})')
    parser.add_argument('-t', '--type', choices=['full', 'titles', 'urls', 'json'],
                        default='full', help='Output format')
    parser.add_argument('--no-cache', action='store_true',
                        help='Disable result caching')
    parser.add_argument('-e', '--engine', choices=['duckduckgo', 'searx'],
                        help='Specific search engine to use')
    parser.add_argument('--bash', action='store_true',
                        help='Use bash implementation if available')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose output')

    args = parser.parse_args()

    if args.verbose:
        print(f"[Query: {args.query}]", file=sys.stderr)
        print(f"[Results: {args.num}]", file=sys.stderr)
        print(f"[Cache: {not args.no_cache}]", file=sys.stderr)
        print(f"[Format: {args.type}]", file=sys.stderr)

    # Try bash implementation if requested
    if args.bash:
        result = run_bash_fallback(args.query, args.num)
        if result:
            print(result)
            return
        else:
            print("[Bash fallback unavailable, using Python]", file=sys.stderr)

    # Use Python implementation
    searcher = WebSearchFallback()
    results = searcher.search(
        args.query,
        num_results=args.num,
        use_cache=not args.no_cache,
        engine=args.engine
    )

    if results:
        print(searcher.format_results(results, args.type))
    else:
        print("[ERROR] Search failed", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()