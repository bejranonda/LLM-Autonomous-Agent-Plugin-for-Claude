#!/usr/bin/env python3
"""
Pattern Storage System for Autonomous Claude Agent Plugin

Manages pattern learning data using JSON files. Stores successful task patterns,
retrieves similar patterns for context-aware recommendations, and
tracks usage statistics.

import json
import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import platform

# Handle Windows compatibility for file locking
if platform.system() == "Windows":
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
            patterns_dir: Directory path for storing patterns (default: .claude-patterns)
        """
        self.patterns_dir = Path(patterns_dir)
        self.patterns_file = self.patterns_dir / "patterns.json"
        self._ensure_directory()

    def _ensure_directory(self):
        """Create patterns directory if it does not exist."""
        self.patterns_dir.mkdir(parents=True, exist_ok=True)
        if not self.patterns_file.exists():
            self._write_patterns([])

    def _read_patterns(self):
        """
        Read patterns from JSON file with file locking.

        Returns:
            List of pattern dictionaries
        """
        try:
            with open(self.patterns_file, "r", encoding="utf-8") as f:
                # Acquire shared lock for reading
                lock_file(f, exclusive=False)
                try:
                    content = f.read()
                    if not content.strip():
                        return []
                    data = json.loads(content)
                    # Handle both simple array and object with "patterns" array
                    if isinstance(data, list):
                        return data
                    elif isinstance(data, dict) and "patterns" in data:
                        return data["patterns"]
                    else:
                        print(f"Warning: Unexpected format in {self.patterns_file}", file=sys.stderr)
                        return []
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

"""
    def _write_patterns(self, patterns: List[Dict[str, Any]]):
"""
        Write patterns to JSON file with file locking.

        Args:
            patterns: List of pattern dictionaries to write
"""
        try:
            # Check if file exists and has existing structure
            existing_structure = None
            if self.patterns_file.exists():
                try:
                    with open(self.patterns_file, "r", encoding="utf-8") as f:
                        content = f.read()
                        if content.strip():
                            data = json.loads(content)
                            if isinstance(data, dict) and "patterns" in data:
                                existing_structure = data
                except:
                    pass  # Fall back to simple structure

            with open(self.patterns_file, "w", encoding="utf-8") as f:
                # Acquire exclusive lock for writing
                lock_file(f, exclusive=True)
                try:
                    if existing_structure:
                        # Preserve existing structure, update patterns array
                        existing_structure["patterns"] = patterns
                        # Update metadata if it exists, otherwise create it
                        if "metadata" not in existing_structure:
                            existing_structure["metadata"] = {}
                        existing_structure["metadata"]["last_updated"] = datetime.now().isoformat()
                        existing_structure["metadata"]["total_patterns"] = len(patterns)
                        json.dump(existing_structure, f, indent=2, ensure_ascii=False)
                    else:
                        # Simple array format
                        json.dump(patterns, f, indent=2, ensure_ascii=False)
                finally:
                    unlock_file(f)
        except Exception as e:
            print(f"Error writing patterns: {e}", file=sys.stderr)
            raise

"""
    def store_pattern():
        
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
        required_fields = ["task_type", "context", "skills_used", "approach", "quality_score"]
        missing_fields = [field for field in required_fields if field not in pattern]

        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Validate task_type
        valid_task_types = [
            "feature_implementation",
            "bug_fix",
            "refactoring",
            "testing",
            "debugging",
            "dashboard-improvement",
            "quality-improvement",
            "learning-activity",
            "project-analysis",
            "security-audit",
            "performance-optimization",
            "automation",
        ]
        if pattern["task_type"] not in valid_task_types:
            raise ValueError(f"Invalid task_type. Must be one of: {', '.join(valid_task_types)}")

        # Validate quality_score
        if not isinstance(pattern["quality_score"], (int, float)) or not (0 <= pattern["quality_score"] <= 1):
            raise ValueError("quality_score must be a number between 0 and 1")

        # Generate pattern_id if not provided
        if "pattern_id" not in pattern:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pattern["pattern_id"] = f"pattern_{timestamp}"

        # Add timestamp if not provided
        if "timestamp" not in pattern:
            pattern["timestamp"] = datetime.now().isoformat()

        # Initialize usage tracking
        if "usage_count" not in pattern:
            pattern["usage_count"] = 0
        if "success_rate" not in pattern:
            pattern["success_rate"] = 1.0 if pattern["quality_score"] >= 0.7 else 0.0

        # Store pattern
        patterns = self._read_patterns()
        patterns.append(pattern)
        self._write_patterns(patterns)

        return pattern["pattern_id"]

"""
    def retrieve_patterns(
        self, context: str, task_type: Optional[str] = None, min_quality: float = 0.8, limit: int = 5
    )-> List[Dict[str, Any]]:
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
            if task_type and pattern.get("task_type") != task_type:
                continue

            # Filter by quality score
            if pattern.get("quality_score", 0) < min_quality:
                continue

            # Calculate relevance score based on keyword matching
            context_text = f"{pattern.get('context', '')} {pattern.get('approach', '')}".lower()
            relevance_score = sum(1 for term in search_terms if term in context_text)

            if relevance_score > 0:
                matches.append({"pattern": pattern, "relevance_score": relevance_score})

        # Sort by relevance, then by quality score and usage count
        matches.sort(
            key=lambda x: (x["relevance_score"], x["pattern"].get("quality_score", 0), x["pattern"].get("usage_count", 0)),
            reverse=True,
        )

        # Return top N matches
        return [match["pattern"] for match in matches[:limit]]

    # Alias for backward compatibility with tests
"""
    def get_patterns(self) -> List[Dict[str, Any]]:
        """Alias to get all patterns for backward compatibility."""
        return self._read_patterns()

    def get_similar_patterns(
        self, task_type: str = None, context: Dict[str, Any] = None, min_quality: float = 0.8, limit: int = 5
    )-> List[Dict[str, Any]]:
        """Get Similar Patterns. Alias for retrieve_patterns method for backward compatibility."""
        context_str = str(context) if context else ""
        return self.retrieve_patterns(context_str, task_type, min_quality, limit)

    def get_skill_effectiveness(self, skill_name: str) -> Dict[str, Any]:
        """Calculate skill effectiveness from stored patterns."""
        patterns = self._read_patterns()

        skill_usage = 0
        successful_usage = 0
        total_quality = 0.0

        for pattern in patterns:
            skills_used = pattern.get("skills_used", [])
            if skill_name in skills_used:
                skill_usage += 1
                quality_score = pattern.get("quality_score", 0)
                total_quality += quality_score
                if quality_score >= 0.7:  # Consider 70%+ as success
                    successful_usage += 1

        if skill_usage == 0:
            return {"skill": skill_name, "usage_count": 0, "success_rate": 0.0, "avg_quality": 0.0}

        return {
            "skill": skill_name,
            "usage_count": skill_usage,
            "success_rate": successful_usage / skill_usage,
            "avg_quality": total_quality / skill_usage,
        }

    def update_usage():
        
        Update usage statistics for a pattern.

        Args:
            pattern_id: ID of the pattern to update
            success: Whether the pattern usage was successful

        Returns:
            True if pattern was found and updated, False otherwise
"""
        patterns = self._read_patterns()

        for pattern in patterns:
            if pattern.get("pattern_id") == pattern_id:
                # Increment usage count
                pattern["usage_count"] = pattern.get("usage_count", 0) + 1

                # Update success rate using running average
                current_rate = pattern.get("success_rate", 1.0)
                current_count = pattern.get("usage_count", 1)

                if success:
                    # Increase success rate
                    pattern["success_rate"] = (current_rate * (current_count - 1) + 1.0) / current_count
                else:
                    # Decrease success rate
                    pattern["success_rate"] = (current_rate * (current_count - 1)) / current_count

                # Update last used timestamp
                pattern["last_used"] = datetime.now().isoformat()

                self._write_patterns(patterns)
                return True

        print(f"Error: Pattern '{pattern_id}' not found", file=sys.stderr)
        return False

"""
    def get_statistics():
        
        Get overall pattern statistics.

        Returns:
            Dictionary with statistics about stored patterns
"""
        patterns = self._read_patterns()

        if not patterns:
            return {"total_patterns": 0, "average_quality": 0.0, "task_type_distribution": {}, "most_used_skills": {}}

        # Calculate statistics
        task_types = {}
        skills_usage = {}
        total_quality = 0

        for pattern in patterns:
            # Task type distribution
            task_type = pattern.get("task_type", "unknown")
            task_types[task_type] = task_types.get(task_type, 0) + 1

            # Skills usage
            for skill in pattern.get("skills_used", []):
                skills_usage[skill] = skills_usage.get(skill, 0) + 1

            # Quality score
            total_quality += pattern.get("quality_score", 0)

        return {
            "total_patterns": len(patterns),
            "average_quality": total_quality / len(patterns),
            "task_type_distribution": task_types,
            "most_used_skills": dict(
                sorted(skills_usage.items(), key=lambda x: x[1], reverse=True)[:10],
            ),
        }

"""
    def _load_unified_data():
        
        Load unified data from unified_data.json file.

        Returns:
            Unified data dictionary with default structure
"""
        unified_file = self.patterns_dir / "unified_data.json"

        if not unified_file.exists():
            return {
                "version": "1.0.0",
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "patterns": [],
                "skill_metrics": {"skill_effectiveness": {}, "skill_usage_history": []},
                "agent_metrics": {"agent_effectiveness": {}, "agent_performance": []},
                "quality_history": {"quality_assessments": []},
                "performance_records": {"records": []},
                "model_performance": {"models": {}},
                "system_health": {"status": "unknown"},
                "project_context": {"detected_languages": [], "frameworks": [], "project_type": "unknown"},
            }

        try:
            with open(unified_file, "r", encoding="utf-8") as f:
                lock_file(f, exclusive=False)
                try:
                    return json.load(f)
                finally:
                    unlock_file(f)
        except Exception as e:
            print(f"Warning: Could not load unified data: {e}", file=sys.stderr)
            return self._load_unified_data()  # Return default structure

"""
    def _save_unified_data():
        
        Save unified data to unified_data.json file.

        Args:
            unified_data: Complete unified data dictionary

        Returns:
            True if successful, False otherwise
"""
        unified_file = self.patterns_dir / "unified_data.json"

        # Update timestamp
        unified_data["last_updated"] = datetime.now().isoformat()

        try:
            with open(unified_file, "w", encoding="utf-8") as f:
                lock_file(f, exclusive=True)
                try:
                    json.dump(unified_data, f, indent=2, ensure_ascii=False)
                    return True
                finally:
                    unlock_file(f)
        except Exception as e:
            print(f"Error saving unified data: {e}", file=sys.stderr)
            return False

"""
    def store_to_unified():
        
        Store data directly to unified structure.

        Args:
            data_type: Type of data (skill_metrics, agent_performance, etc.)
            data: Data to store

        Returns:
            True if successful, False otherwise
"""
        unified = self._load_unified_data()

        try:
            if data_type == "skill_metrics":
                if "skill_effectiveness" in data:
                    unified["skill_metrics"]["skill_effectiveness"].update(data["skill_effectiveness"])
                if "skill_usage_history" in data:
                    unified["skill_metrics"]["skill_usage_history"].extend(data.get("skill_usage_history", []))

            elif data_type == "agent_performance":
                if "agent_effectiveness" in data:
                    unified["agent_metrics"]["agent_effectiveness"].update(data["agent_effectiveness"])
                if "agent_performance" in data:
                    unified["agent_metrics"]["agent_performance"].extend(data.get("agent_performance", []))

            elif data_type == "quality_history":
                if isinstance(data, dict) and "quality_assessments" in data:
                    unified["quality_history"]["quality_assessments"].extend(data["quality_assessments"])
                else:
                    unified["quality_history"]["quality_assessments"].append(data)

            elif data_type == "performance_records":
                if isinstance(data, dict) and "records" in data:
                    unified["performance_records"]["records"].extend(data["records"])
                else:
                    unified["performance_records"]["records"].append(data)

            elif data_type == "model_performance":
                unified["model_performance"].update(data)

            elif data_type == "system_health":
                unified["system_health"].update(data)

            elif data_type == "project_context":
                unified["project_context"].update(data)

            else:
                print(f"Warning: Unknown data_type '{data_type}' for unified storage", file=sys.stderr)
                return False

            return self._save_unified_data(unified)

        except Exception as e:
            print(f"Error storing to unified data: {e}", file=sys.stderr)
            return False

"""
    def consolidate_all_data():
        
        Consolidate all scattered data files into unified_data.json.

        Returns:
            True if successful, False otherwise
"""
        try:
            # Start with empty unified structure
            unified = self._load_unified_data()

            # 1. Load patterns (already in right format)
            unified["patterns"] = self._read_patterns()

            # 2. Load skill metrics
            skill_file = self.patterns_dir / "skill_metrics.json"
            if skill_file.exists():
                try:
                    with open(skill_file, "r", encoding="utf-8") as f:
                        skill_data = json.load(f)
                        unified["skill_metrics"] = skill_data
                except Exception as e:
                    print(f"Warning: Could not load skill_metrics.json: {e}", file=sys.stderr)

            # 3. Load agent metrics
            agent_file = self.patterns_dir / "agent_metrics.json"
            if agent_file.exists():
                try:
                    with open(agent_file, "r", encoding="utf-8") as f:
                        agent_data = json.load(f)
                        unified["agent_metrics"] = agent_data
                except Exception as e:
                    print(f"Warning: Could not load agent_metrics.json: {e}", file=sys.stderr)

            # 4. Load quality history
            quality_file = self.patterns_dir / "quality_history.json"
            if quality_file.exists():
                try:
                    with open(quality_file, "r", encoding="utf-8") as f:
                        quality_data = json.load(f)
                        unified["quality_history"] = quality_data
                except Exception as e:
                    print(f"Warning: Could not load quality_history.json: {e}", file=sys.stderr)

            # 5. Load performance records
            perf_file = self.patterns_dir / "performance_records.json"
            if perf_file.exists():
                try:
                    with open(perf_file, "r", encoding="utf-8") as f:
                        perf_data = json.load(f)
                        unified["performance_records"] = perf_data
                except Exception as e:
                    print(f"Warning: Could not load performance_records.json: {e}", file=sys.stderr)

            # 6. Load model performance if exists
            model_file = self.patterns_dir / "model_performance.json"
            if model_file.exists():
                try:
                    with open(model_file, "r", encoding="utf-8") as f:
                        model_data = json.load(f)
                        unified["model_performance"] = model_data
                except Exception as e:
                    print(f"Warning: Could not load model_performance.json: {e}", file=sys.stderr)

            # 7. Update project context from patterns
            if unified["patterns"]:
                # Extract languages and frameworks from patterns
                languages = set()
                frameworks = set()

                for pattern in unified["patterns"]:
                    context = pattern.get("context", {})
                    if isinstance(context, dict):
                        if "languages" in context:
                            languages.update(context["languages"])
                        if "frameworks" in context:
                            frameworks.update(context["frameworks"])

                unified["project_context"]["detected_languages"] = list(languages)
                unified["project_context"]["frameworks"] = list(frameworks)
                unified["project_context"]["project_type"] = "autonomous-agent-plugin"

            # 8. Update system health
            unified["system_health"] = {
                "status": "healthy",
                "total_patterns": len(unified["patterns"]),
                "total_skills": len(unified["skill_metrics"].get("skill_effectiveness", {})),
                "total_agents": len(unified["agent_metrics"].get("agent_effectiveness", {})),
                "last_consolidated": datetime.now().isoformat(),
            }

            # Save the consolidated data
            return self._save_unified_data(unified)

        except Exception as e:
            print(f"Error consolidating data: {e}", file=sys.stderr)
            return False

"""
    def store_pattern_enhanced():
        
        Enhanced pattern storage that also updates unified data.

        Args:
            pattern: Pattern dictionary

        Returns:
            pattern_id of stored pattern
"""
        # Store pattern using existing method
        pattern_id = self.store_pattern(pattern)

        # Also update unified data
        try:
            unified = self._load_unified_data()

            # Add pattern to unified structure
            unified["patterns"].append(pattern)

            # Update skill metrics if pattern has skills
            if "skills_used" in pattern:
                for skill in pattern["skills_used"]:
                    if "skill_effectiveness" not in unified["skill_metrics"]:
                        unified["skill_metrics"]["skill_effectiveness"] = {}

                    if skill not in unified["skill_metrics"]["skill_effectiveness"]:
                        unified["skill_metrics"]["skill_effectiveness"][skill] = {
                            "total_uses": 0,
                            "successful_uses": 0,
                            "success_rate": 0.0,
                            "avg_contribution_score": 0.0,
                        }

                    skill_metrics = unified["skill_metrics"]["skill_effectiveness"][skill]
                    skill_metrics["total_uses"] += 1

                    if pattern.get("quality_score", 0) > 0.7:  # Consider 70%+ as success
                        skill_metrics["successful_uses"] += 1

                    # Update success rate
                    skill_metrics["success_rate"] = skill_metrics["successful_uses"] / skill_metrics["total_uses"]

                    # Update avg contribution score
                    current_avg = skill_metrics["avg_contribution_score"]
                    pattern_score = pattern.get("quality_score", 0)
                    skill_metrics["avg_contribution_score"] = (current_avg + pattern_score) / 2

            self._save_unified_data(unified)

        except Exception as e:
            print(f"Warning: Could not update unified data: {e}", file=sys.stderr)

        return pattern_id


"""
def main():
    """Command-line interface for pattern storage."""
    parser = argparse.ArgumentParser(description="Pattern Storage System")
    parser.add_argument(
        "--dir",
        default=".claude-patterns",
        help="Patterns directory path",
    )

    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    # Store action
    store_parser = subparsers.add_parser("store", help="Store a new pattern")
    store_parser.add_argument("--pattern", required=True, help="Pattern JSON string")

    # Retrieve action
    retrieve_parser = subparsers.add_parser("retrieve", help="Retrieve patterns")
    retrieve_parser.add_argument(
        "--context",
        required=True,
        help="Search context/keywords",
    )
    retrieve_parser.add_argument("--task-type", help="Filter by task type")
    retrieve_parser.add_argument(
        "--min-quality",
        type=float,
        default=0.8,
        help="Minimum quality score",
    )
    retrieve_parser.add_argument("--limit", type=int, default=5, help="Maximum results")

    # Update action
    update_parser = subparsers.add_parser("update", help="Update pattern usage")
    update_parser.add_argument("--pattern-id", required=True, help="Pattern ID")
    update_parser.add_argument(
        "--success",
        action="store_true",
        help="Mark as successful usage",
    )
    update_parser.add_argument(
        "--failure",
        dest="success",
        action="store_false",
        help="Mark as failed usage",
    )
    update_parser.set_defaults(success=True)

    # Statistics action
    subparsers.add_parser("stats", help="Show pattern statistics")

    # Check action - for /learn:init smart detection
    subparsers.add_parser("check", help="Check if pattern database exists and is valid")

    # Init action - for /learn:init initialization
    init_parser = subparsers.add_parser("init", help="Initialize or update pattern database")
    init_parser.add_argument("--version", default="7.6.7", help="Plugin version")

    # Validate action - for /learn:init validation
    subparsers.add_parser("validate", help="Validate pattern database integrity")

    # Unified data actions
    # Consolidate action
    subparsers.add_parser("consolidate", help="Consolidate all data into unified_data.json")

    # Store to unified action
    unified_parser = subparsers.add_parser("store-unified", help="Store data to unified structure")
    unified_parser.add_argument(
        "--type",
        required=True,
        choices=[
            "skill_metrics",
            "agent_performance",
            "quality_history",
            "performance_records",
            "model_performance",
            "system_health",
            "project_context",
        ],
        help="Type of data to store",
    )
    unified_parser.add_argument("--data", required=True, help="Data JSON string")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    storage = PatternStorage(args.dir)

    try:
        if args.action == "store":
            pattern = json.loads(args.pattern)
            pattern_id = storage.store_pattern(pattern)
            print(json.dumps({"success": True, "pattern_id": pattern_id}, indent=2))

        elif args.action == "retrieve":
            patterns = storage.retrieve_patterns(
                args.context, task_type=args.task_type, min_quality=args.min_quality, limit=args.limit
            )
            print(json.dumps(patterns, indent=2))

        elif args.action == "update":
            success = storage.update_usage(args.pattern_id, args.success)
            print(json.dumps({"success": success}, indent=2))

        elif args.action == "stats":
            stats = storage.get_statistics()
            print(json.dumps(stats, indent=2))

        elif args.action == "consolidate":
            success = storage.consolidate_all_data()
            if success:
                print(json.dumps({"success": True, "message": "Data consolidated successfully"}, indent=2))
            else:
                print(json.dumps({"success": False, "error": "Consolidation failed"}, indent=2))

        elif args.action == "store-unified":
            data = json.loads(args.data)
            success = storage.store_to_unified(args.type, data)
            if success:
                print(json.dumps({"success": True, "message": f"Data stored to unified structure"}, indent=2))
            else:
                print(json.dumps({"success": False, "error": "Failed to store data"}, indent=2))

        elif args.action == "check":
            # Check if pattern database exists and is valid
            patterns_dir = Path(args.dir)
            patterns_file = patterns_dir / "patterns.json"
            config_file = patterns_dir / "config.json"

            result = {
                "exists": patterns_dir.exists(),
                "patterns_file_exists": patterns_file.exists() if patterns_dir.exists() else False,
                "config_file_exists": config_file.exists() if patterns_dir.exists() else False,
                "complete": False,
                "version": None,
                "pattern_count": 0,
                "status": "not_initialized",
            }

            if patterns_file.exists():
                try:
                    with open(patterns_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, dict):
                            patterns = data.get("patterns", [])
                        else:
                            patterns = data
                        result["pattern_count"] = len(patterns)
                except:
                    result["status"] = "corrupt"
                    print(json.dumps(result, indent=2))
                    sys.exit(0)

            if config_file.exists():
                try:
                    with open(config_file, "r", encoding="utf-8") as f:
                        config = json.load(f)
                        result["version"] = config.get("version", "unknown")
                except:
                    pass

            # Determine status
            required_files = ["patterns.json", "task_queue.json", "quality_history.json", "config.json"]
            all_exist = all((patterns_dir / f).exists() for f in required_files)

            if all_exist and patterns_file.exists():
                result["complete"] = True
                result["status"] = "initialized"
            elif patterns_dir.exists() and patterns_file.exists():
                result["status"] = "partial"
                result["complete"] = False
            else:
                result["status"] = "not_initialized"

            print(json.dumps(result, indent=2))

        elif args.action == "init":
            # Initialize or update pattern database
            patterns_dir = Path(args.dir)
            patterns_dir.mkdir(parents=True, exist_ok=True)

            # Initialize all required files
            patterns_file = patterns_dir / "patterns.json"
            if not patterns_file.exists():
                with open(patterns_file, "w", encoding="utf-8") as f:
                    json.dump({"version": "1.0", "patterns": [], "skill_effectiveness": {}}, f, indent=2)

            task_queue_file = patterns_dir / "task_queue.json"
            if not task_queue_file.exists():
                with open(task_queue_file, "w", encoding="utf-8") as f:
                    json.dump({"queue": []}, f, indent=2)

            quality_history_file = patterns_dir / "quality_history.json"
            if not quality_history_file.exists():
                with open(quality_history_file, "w", encoding="utf-8") as f:
                    json.dump({"history": []}, f, indent=2)

            config_file = patterns_dir / "config.json"
            config = {
                "version": args.version,
                "initialized_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
            }
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)

            result = {
                "success": True,
                "message": "Pattern database initialized successfully",
                "version": args.version,
                "files_created": ["patterns.json", "task_queue.json", "quality_history.json", "config.json"],
            }
            print(json.dumps(result, indent=2))

        elif args.action == "validate":
            # Validate pattern database integrity
            patterns_dir = Path(args.dir)

            result = {"valid": True, "errors": [], "warnings": [], "files_checked": []}

            # Check each required file
            required_files = {
                "patterns.json": {"patterns": list, "skill_effectiveness": dict},
                "task_queue.json": {"queue": list},
                "quality_history.json": {"history": list},
                "config.json": {"version": str},
            }

            for filename, required_structure in required_files.items():
                filepath = patterns_dir / filename
                result["files_checked"].append(filename)

                if not filepath.exists():
                    result["errors"].append(f"{filename} does not exist")
                    result["valid"] = False
                    continue

                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    # Check required keys and types
                    for key, expected_type in required_structure.items():
                        if key not in data:
                            result["warnings"].append(f'{filename}: missing key "{key}"')
                        elif not isinstance(data[key], expected_type):
                            result["errors"].append(f'{filename}: "{key}" should be {expected_type.__name__}')
                            result["valid"] = False

                except json.JSONDecodeError as e:
                    result["errors"].append(f"{filename}: invalid JSON - {str(e)}")
                    result["valid"] = False
                except Exception as e:
                    result["errors"].append(f"{filename}: error reading file - {str(e)}")
                    result["valid"] = False

            print(json.dumps(result, indent=2))

    except Exception as e:
        print(
            json.dumps({"success": False, "error": str(e)}, indent=2),
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
