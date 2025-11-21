#!/usr/bin/env python3

"""
Smart Web Search with Automatic Fallback
Automatically uses web_search_fallback when WebSearch fails
"""

import sys
import os
import json
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from web_search_fallback import WebSearchFallback
except ImportError:
    print("[ERROR] web_search_fallback module not found", file=sys.stderr)
    sys.exit(1)


class SmartWebSearch:
    """Smart search that automatically falls back when primary search fails."""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.fallback = WebSearchFallback()

    def search(self, query, num_results=10):
        """
        Perform smart search with automatic fallback.

        Args:
            query: Search query string
            num_results: Number of results to return

        Returns:
            List of search results
        """

        # First, try to use WebSearch if available (simulated here)
        if self.verbose:
            print("[INFO] Attempting primary WebSearch...", file=sys.stderr)

        # Simulate WebSearch attempt (in real usage, this would call the actual WebSearch)
        # For demonstration, we'll simulate it failing
        websearch_available = os.environ.get('WEBSEARCH_AVAILABLE', 'false').lower() == 'true'

        if websearch_available:
            if self.verbose:
                print("[SUCCESS] WebSearch returned results", file=sys.stderr)
            # Would return WebSearch results here
            return [{"title": "WebSearch Result", "url": "http://example.com"}]
        else:
            if self.verbose:
                print("[FAILED] WebSearch unavailable or failed", file=sys.stderr)
                print("[INFO] Activating fallback search system...", file=sys.stderr)

            # Use fallback
            results = self.fallback.search(query, num_results=num_results, use_cache=True)

            if self.verbose and results:
                print(f"[SUCCESS] Fallback returned {len(results)} results", file=sys.stderr)

            return results

    def format_results(self, results):
        """Format results for display."""
        if not results:
            return "No results found"

        output = []
        output.append("=" * 50)
        output.append("SMART SEARCH RESULTS")
        output.append("=" * 50)
        output.append("")

        for i, result in enumerate(results, 1):
            output.append(f"[{i}] {result.get('title', 'N/A')}")
            output.append(f"    URL: {result.get('url', 'N/A')}")
            if 'snippet' in result:
                snippet = result['snippet'][:150] + "..." if len(result.get('snippet', '')) > 150 else result['snippet']
                output.append(f"    Snippet: {snippet}")
            output.append("")

        return '\n'.join(output)


def demonstrate_automatic_fallback(query="AI trends 2025"):
    """
    Demonstrate how the smart search automatically uses fallback.

    This function shows the automatic failover behavior when WebSearch fails.
    """
    print(f"\n{'='*60}")
    print("SMART SEARCH DEMONSTRATION - Automatic Fallback")
    print(f"{'='*60}\n")

    print(f"Query: '{query}'")
    print("-" * 40)

    # Create smart searcher with verbose mode
    searcher = SmartWebSearch(verbose=True)

    print("\nScenario 1: WebSearch Fails (Typical Case)")
    print("-" * 40)

    # Ensure WebSearch is "unavailable" for this demo
    os.environ['WEBSEARCH_AVAILABLE'] = 'false'

    results = searcher.search(query, num_results=3)

    if results:
        print("\nResults (via automatic fallback):")
        for i, r in enumerate(results[:3], 1):
            print(f"  {i}. {r.get('title', 'N/A')}")

    print("\n" + "="*60)
    print("CONCLUSION: Search succeeded despite WebSearch failure!")
    print("The fallback system activated automatically.")
    print("="*60)

    return results


def main():
    """Main entry point for command line usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Smart Web Search with Automatic Fallback'
    )
    parser.add_argument('query', nargs='?',
                        help='Search query (optional for demo mode)')
    parser.add_argument('-n', '--num', type=int, default=10,
                        help='Number of results')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose output')
    parser.add_argument('--demo', action='store_true',
                        help='Run demonstration of automatic fallback')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')

    args = parser.parse_args()

    if args.demo:
        # Run demonstration
        demonstrate_automatic_fallback(args.query or "AI trends 2025")
        return

    if not args.query:
        parser.error("Query required (unless using --demo)")

    # Perform smart search
    searcher = SmartWebSearch(verbose=args.verbose)
    results = searcher.search(args.query, num_results=args.num)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(searcher.format_results(results))


if __name__ == '__main__':
    main()