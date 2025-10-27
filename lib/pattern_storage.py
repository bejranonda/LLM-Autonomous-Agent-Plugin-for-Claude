#!/usr/bin/env python3
"""
Pattern Storage System for Autonomous Claude Agent Plugin

Manages pattern learning data using JSON files. Stores successful task patterns,
retrieves similar patterns for context-aware recommendations, and 
    tracks usage statistics.
"""

import json
import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import platform

# Handle Windows compatibility for file locking
if platform.system() == 'Windows':
    import msvcrt
    def lock_file(f, exclusive=False):
        """Windows file locking using msvcrt."""
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK if exclusive else msvcrt.LK_NBLCK, 1)

    def unlock_file(f):
        """Windows file unlocking."""
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except:
            pass
else:
    import fcntl
    def lock_file(f, exclusive=False):
        """Unix file locking using fcntl."""
        fcntl.flock(f.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)

    def unlock_file(f):
        """Unix file unlocking."""
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


class PatternStorage:
    """Manages storage and retrieval of learned patterns."""

    def __init__(self, patterns_dir: str = ".claude-patterns"):
        """
        Initialize pattern storage.

        Args:
            patterns_dir: Directory path for storing patterns (
    default: .claude-patterns,
)
        """
        self.patterns_dir = Path(patterns_dir)
        self.patterns_file = self.patterns_dir / "patterns.json"
        self._ensure_directory()

    def _ensure_directory(self):
        """Create patterns directory if it doesn't exist."""
        self.patterns_dir.mkdir(parents=True, exist_ok=True)
        if not self.patterns_file.exists():
            self._write_patterns([])

    def _read_patterns(self) -> List[Dict[str, Any]]:
        """
        Read patterns from JSON file with file locking.

        Returns:
            List of pattern dictionaries
        """
        try:
            with open(self.patterns_file, 'r', encoding='utf-8') as f:
                # Acquire shared lock for reading
                lock_file(f, exclusive=False)
                try:
                    content = f.read()
                    if not content.strip():
                        return []
                    return json.loads(content)
                finally:
                    unlock_file(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            print(
    f"Error: Malformed JSON in {self.patterns_file}: {e}",
    file=sys.stderr,
)
            return []
        except Exception as e:
            print(f"Error reading patterns: {e}", file=sys.stderr)
            return []

    def _write_patterns(self, patterns: List[Dict[str, Any]]):
        """
        Write patterns to JSON file with file locking.

        Args:
            patterns: List of pattern dictionaries to write
        """
        try:
            with open(self.patterns_file, 'w', encoding='utf-8') as f:
                # Acquire exclusive lock for writing
                lock_file(f, exclusive=True)
                try:
                    json.dump(patterns, f, indent=2, ensure_ascii=False)
                finally:
                    unlock_file(f)
        except Exception as e:
            print(f"Error writing patterns: {e}", file=sys.stderr)
            raise

    def store_pattern(self, pattern: Dict[str, Any]) -> str:
        """
        Store a new pattern.

        Args:
            pattern: Pattern dictionary containing task information

        Returns:
            pattern_id of the stored pattern

        Required pattern fields:
            - task_type: Type of task (
    feature_implementation,
    bug_fix,
    refactoring,
    testing,
)
            - context: Natural language description of task context
            - skills_used: List of skills used
            - approach: Detailed description of approach taken
            - quality_score: Quality score (0.0 to 1.0)
        """
        # Validate required fields
        required_fields = ['task_type', 'context', 'skills_used', 'approach', 'quality_score']
        missing_fields = [field for field in required_fields if field not in pattern]

        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Validate task_type
        valid_task_types = ['feature_implementation', 'bug_fix', 'refactoring', 'testing']
        if pattern['task_type'] not in valid_task_types:
            raise ValueError(
    f"Invalid task_type. Must be one of: {',
    '.join(valid_task_types)}",
)

        # Validate quality_score
        if not isinstance(
    pattern['quality_score'],
    (int, float)) or not (0 <= pattern['quality_score'] <= 1):,
)
            raise ValueError("quality_score must be a number between 0 and 1")

        # Generate pattern_id if not provided
        if 'pattern_id' not in pattern:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            pattern['pattern_id'] = f"pattern_{timestamp}"

        # Add timestamp if not provided
        if 'timestamp' not in pattern:
            pattern['timestamp'] = datetime.now().isoformat()

        # Initialize usage tracking
        if 'usage_count' not in pattern:
            pattern['usage_count'] = 0
        if 'success_rate' not in pattern:
            pattern['success_rate'] = 1.0 if pattern['quality_score'] >= 0.7 else 0.0

        # Store pattern
        patterns = self._read_patterns()
        patterns.append(pattern)
        self._write_patterns(patterns)

        return pattern['pattern_id']

    def retrieve_patterns(
        self,
        context: str,
        task_type: Optional[str] = None,
        min_quality: float = 0.8,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve patterns matching search criteria.

        Args:
            context: Search keywords (searches in context and approach fields)
            task_type: Filter by task type (optional)
            min_quality: Minimum quality score (default: 0.8)
            limit: Maximum number of results (default: 5)

        Returns:
            List of matching patterns, sorted by relevance and quality
        """
        patterns = self._read_patterns()

        # Convert context to lowercase for case-insensitive matching
        search_terms = context.lower().split()

        # Filter patterns
        matches = []
        for pattern in patterns:
            # Filter by task_type if specified
            if task_type and pattern.get('task_type') != task_type:
                continue

            # Filter by quality score
            if pattern.get('quality_score', 0) < min_quality:
                continue

            # Calculate relevance score based on keyword matching
            context_text = f"{pattern.get('context', '')} {pattern.get('approach', '')}".lower()
            relevance_score = sum(1 for term in search_terms if term in context_text)

            if relevance_score > 0:
                matches.append({
                    'pattern': pattern,
                    'relevance_score': relevance_score
                })

        # Sort by relevance, then by quality score and usage count
        matches.sort(
            key=lambda x: (
                x['relevance_score'],
                x['pattern'].get('quality_score', 0),
                x['pattern'].get('usage_count', 0)
            ),
            reverse=True
        )

        # Return top N matches
        return [match['pattern'] for match in matches[:limit]]

    def update_usage(self, pattern_id: str, success: bool = True) -> bool:
        """
        Update usage statistics for a pattern.

        Args:
            pattern_id: ID of the pattern to update
            success: Whether the pattern usage was successful

        Returns:
            True if pattern was found and updated, False otherwise
        """
        patterns = self._read_patterns()

        for pattern in patterns:
            if pattern.get('pattern_id') == pattern_id:
                # Increment usage count
                pattern['usage_count'] = pattern.get('usage_count', 0) + 1

                # Update success rate using running average
                current_rate = pattern.get('success_rate', 1.0)
                current_count = pattern.get('usage_count', 1)

                if success:
                    # Increase success rate
                    pattern['success_rate'] = (current_rate * (current_count - 1) + 1.0) / current_count
                else:
                    # Decrease success rate
                    pattern['success_rate'] = (current_rate * (current_count - 1)) / current_count

                # Update last used timestamp
                pattern['last_used'] = datetime.now().isoformat()

                self._write_patterns(patterns)
                return True

        print(f"Error: Pattern '{pattern_id}' not found", file=sys.stderr)
        return False

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get overall pattern statistics.

        Returns:
            Dictionary with statistics about stored patterns
        """
        patterns = self._read_patterns()

        if not patterns:
            return {
                'total_patterns': 0,
                'average_quality': 0.0,
                'task_type_distribution': {},
                'most_used_skills': {}
            }

        # Calculate statistics
        task_types = {}
        skills_usage = {}
        total_quality = 0

        for pattern in patterns:
            # Task type distribution
            task_type = pattern.get('task_type', 'unknown')
            task_types[task_type] = task_types.get(task_type, 0) + 1

            # Skills usage
            for skill in pattern.get('skills_used', []):
                skills_usage[skill] = skills_usage.get(skill, 0) + 1

            # Quality score
            total_quality += pattern.get('quality_score', 0)

        return {
            'total_patterns': len(patterns),
            'average_quality': total_quality / len(patterns),
            'task_type_distribution': task_types,
            'most_used_skills': dict(
    sorted(skills_usage.items(), key=lambda x: x[1], reverse=True)[:10],
)
        }


def main():
    """Command-line interface for pattern storage."""
    parser = argparse.ArgumentParser(description='Pattern Storage System')
    parser.add_argument(
    '--dir',
    default='.claude-patterns',
    help='Patterns directory path',
)

    subparsers = parser.add_subparsers(dest='action', help='Action to perform')

    # Store action
    store_parser = subparsers.add_parser('store', help='Store a new pattern')
    store_parser.add_argument('--pattern', required=True, help='Pattern JSON string')

    # Retrieve action
    retrieve_parser = subparsers.add_parser('retrieve', help='Retrieve patterns')
    retrieve_parser.add_argument(
    '--context',
    required=True,
    help='Search context/keywords',
)
    retrieve_parser.add_argument('--task-type', help='Filter by task type')
    retrieve_parser.add_argument(
    '--min-quality',
    type=float,
    default=0.8,
    help='Minimum quality score',
)
    retrieve_parser.add_argument('--limit', type=int, default=5, help='Maximum results')

    # Update action
    update_parser = subparsers.add_parser('update', help='Update pattern usage')
    update_parser.add_argument('--pattern-id', required=True, help='Pattern ID')
    update_parser.add_argument(
    '--success',
    action='store_true',
    help='Mark as successful usage',
)
    update_parser.add_argument(
    '--failure',
    dest='success',
    action='store_false',
    help='Mark as failed usage',
)
    update_parser.set_defaults(success=True)

    # Statistics action
    subparsers.add_parser('stats', help='Show pattern statistics')

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    storage = PatternStorage(args.dir)

    try:
        if args.action == 'store':
            pattern = json.loads(args.pattern)
            pattern_id = storage.store_pattern(pattern)
            print(json.dumps({'success': True, 'pattern_id': pattern_id}, indent=2))

        elif args.action == 'retrieve':
            patterns = storage.retrieve_patterns(
                args.context,
                task_type=args.task_type,
                min_quality=args.min_quality,
                limit=args.limit
            )
            print(json.dumps(patterns, indent=2))

        elif args.action == 'update':
            success = storage.update_usage(args.pattern_id, args.success)
            print(json.dumps({'success': success}, indent=2))

        elif args.action == 'stats':
            stats = storage.get_statistics()
            print(json.dumps(stats, indent=2))

    except Exception as e:
        print(
    json.dumps({'success': False, 'error': str(e)}, indent=2),
    file=sys.stderr,
)
        sys.exit(1)


if __name__ == '__main__':
    main()
