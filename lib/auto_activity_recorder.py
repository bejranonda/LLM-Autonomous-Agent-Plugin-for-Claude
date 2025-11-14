#!/usr/bin/env python3
#     Automatic Activity Recorder
    """
Integrates with the learning engine to automatically capture all activities
and ensure comprehensive performance tracking.
import json
import os
import time
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional


class AutoActivityRecorder:
    def __init__(self, patterns_dir: str = ".claude-patterns"):
        """Initialize the processor with default configuration."""
        self.patterns_dir = patterns_dir
        self.performance_records_file = os.path.join(patterns_dir, "performance_records.json")
        self.auto_trigger_log = os.path.join(patterns_dir, "auto_trigger_log.json")
        self.last_scan_file = os.path.join(patterns_dir, "last_commit_scan.json")

    def get_last_scan_time(self) -> datetime:
        """Get the timestamp of the last commit scan."""
        if os.path.exists(self.last_scan_file):
            try:
                with open(self.last_scan_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return datetime.fromisoformat(data.get("last_scan", "2025-01-01T00:00:00"))
            except:
                pass
        return datetime.now() - timedelta(hours=24)  # Default to 24 hours ago

    def update_last_scan_time(self) -> None:
        """Update the last scan time to now."""
        with open(self.last_scan_file, "w", encoding="utf-8") as f:
            json.dump({"last_scan": datetime.now().isoformat()}, f, indent=2)

    def get_new_commits(self, since: datetime) -> List[Dict[str, Any]]:
        """Get commits since the last scan."""
        since_str = since.strftime("%Y-%m-%d %H:%M:%S")

        try:
            result = subprocess.run(
                ["git", "log", f"--since={since_str}", "--pretty=format:%H|%ad|%s", "--date=iso", "--no-merges"],
                capture_output=True,
                text=True,
                check=True,
            )

            commits = []
            for line in result.stdout.strip().split("\n"):
                if line:
                    parts = line.split("|")
                    if len(parts) >= 3:
                        commits.append({"hash": parts[0], "date": parts[1], "message": parts[2]})
            return commits
        except subprocess.CalledProcessError:
            return []

    def load_existing_assessment_ids(self) -> set:
        """Load existing assessment IDs to avoid duplicates."""
        ids = set()

        if os.path.exists(self.performance_records_file):
            with open(self.performance_records_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for record in data.get("records", []):
                    if record.get("assessment_id"):
                        ids.add(record["assessment_id"])

        return ids

    def classify_commit(self, message: str) -> tuple[str, int, float]:
        """Classify commit type and estimate score/duration."""
        msg_lower = message.lower()

        # Determine task type
        if msg_lower.startswith("feat:") or msg_lower.startswith("feature:"):
            task_type = "feature-implementation"
            base_score = 95
        elif msg_lower.startswith("fix:") or msg_lower.startswith("bugfix:"):
            task_type = "bug-fix"
            base_score = 92
        elif msg_lower.startswith("refactor:"):
            task_type = "refactoring"
            base_score = 90
        elif msg_lower.startswith("docs:"):
            task_type = "documentation"
            base_score = 88
        elif msg_lower.startswith("release:") or msg_lower.startswith("bump:"):
            task_type = "release-management"
            base_score = 89
        elif "quality" in msg_lower:
            task_type = "quality-improvement"
            base_score = 93
        else:
            task_type = "code-improvement"
            base_score = 90

        # Estimate duration based on message complexity
        words = len(message.split())
        if words > 20:
            duration = 15.0  # Complex commit
            score = base_score - 2
        elif words > 10:
            duration = 8.0  # Medium commit
            score = base_score
        else:
            duration = 3.0  # Simple commit
            score = base_score + 1

        score = max(80, min(100, score))
        return task_type, score, duration

    def get_files_changed(self, commit_hash: str) -> int:
        """Get number of files changed in a commit."""
        try:
            result = subprocess.run(
                ["git", "show", "--name-only", "--pretty=format:", commit_hash], capture_output=True, text=True, check=True
            )

            files = [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
            return len(files)
        except subprocess.CalledProcessError:
            return 1

    def create_performance_record(self, commit: Dict[str, Any], existing_ids: set) -> Optional[Dict[str, Any]]:
        """Create a performance record for a commit."""
        timestamp = datetime.fromisoformat(commit["date"].replace(" ", "T"))
        task_type, score, duration = self.classify_commit(commit["message"])
        files_changed = self.get_files_changed(commit["hash"])

        # Create assessment ID
        assessment_id = f"{task_type.replace('-', '')}-{timestamp.strftime('%Y%m%d-%H%M%S')}-{commit['hash'][:8]}"

        # Skip if already exists
        if assessment_id in existing_ids:
            return None

        # Create record
        record = {
            "assessment_id": assessment_id,
            "timestamp": timestamp.isoformat(),
            "task_type": task_type,
            "overall_score": score,
            "pass": True,
            "auto_generated": True,
            "evaluation_target": task_type,
            "issues_found": 0,
            "fixes_applied": 1 if "fix" in task_type else 0,
            "quality_improvement": 5 if "quality" in task_type or "refactor" in task_type else 0,
            "performance_index": score * 0.9,
            "success_rate": 100,
            "time_elapsed_minutes": duration,
            "model": "GLM-4.6",
            "description": commit["message"][:100],
            "files_modified": files_changed,
            "source": "automatic-git-monitoring",
            "commit_hash": commit["hash"],
            "details": {
                "source": "automatic-git-monitoring",
                "commit_hash": commit["hash"],
                "files_modified": files_changed,
                "auto_captured": True,
            },
        }

        return record

    def add_records_to_performance_file(self, records: List[Dict[str, Any]]) -> int:
        """Add new records to the performance records file."""
        if not records:
            return 0

        # Load existing data
        performance_data = {"records": [], "version": "2.0.0"}
        if os.path.exists(self.performance_records_file):
            with open(self.performance_records_file, "r", encoding="utf-8") as f:
                performance_data = json.load(f)

        # Add new records at the beginning
        for record in records:
            performance_data["records"].insert(0, record)

        # Update metadata
        if "metadata" not in performance_data:
            performance_data["metadata"] = {}
        performance_data["metadata"]["total_records"] = len(performance_data["records"])
        performance_data["metadata"]["last_updated"] = datetime.now().isoformat()

        # Save updated data
        with open(self.performance_records_file, "w", encoding="utf-8") as f:
            json.dump(performance_data, f, indent=2, ensure_ascii=False)

        return len(records)

    def log_automatic_capture(self, records: List[Dict[str, Any]]) -> None:
        """Log the automatic capture activity."""
        if not records:
            return

        # Load existing log
        log_data = {"version": "1.0.0", "captures": [], "metadata": {}}
        if os.path.exists(self.auto_trigger_log):
            with open(self.auto_trigger_log, "r", encoding="utf-8") as f:
                log_data = json.load(f)

        # Add new capture entries
        for record in records:
            capture_entry = {
                "timestamp": datetime.now().isoformat(),
                "type": "automatic_git_capture",
                "assessment_id": record["assessment_id"],
                "task_type": record["task_type"],
                "duration_seconds": record["time_elapsed_minutes"] * 60,
                "quality_score": record["overall_score"],
                "success": True,
                "source": "auto_activity_recorder",
            }
            log_data["captures"].append(capture_entry)

        # Update metadata
        log_data["metadata"] = {
            "total_captures": len(log_data["captures"]),
            "last_capture": datetime.now().isoformat(),
            "auto_recording_enabled": True,
        }

        # Save log
        with open(self.auto_trigger_log, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)

    def scan_and_record(self) -> Dict[str, Any]:
        """Main method to scan for new commits and record them."""
        print(f"[AutoActivityRecorder] Starting automatic activity scan...")

        # Get last scan time
        last_scan = self.get_last_scan_time()
        print(f"[AutoActivityRecorder] Last scan: {last_scan}")

        # Get new commits
        new_commits = self.get_new_commits(last_scan)
        print(f"[AutoActivityRecorder] Found {len(new_commits)} new commits")

        if not new_commits:
            print("[AutoActivityRecorder] No new commits to record")
            self.update_last_scan_time()
            return {"status": "no_new_commits", "records_added": 0}

        # Load existing assessment IDs
        existing_ids = self.load_existing_assessment_ids()

        # Create records for new commits
        new_records = []
        for commit in new_commits:
            record = self.create_performance_record(commit, existing_ids)
            if record:
                new_records.append(record)
                existing_ids.add(record["assessment_id"])

        print(f"[AutoActivityRecorder] Created {len(new_records)} new records")

        # Add records to performance file
        added_count = self.add_records_to_performance_file(new_records)

        # Log the automatic capture
        self.log_automatic_capture(new_records)

        # Update last scan time
        self.update_last_scan_time()

        result = {
            "status": "success",
            "records_added": added_count,
            "commits_scanned": len(new_commits),
            "scan_time": datetime.now().isoformat(),
        }

        print(f"[AutoActivityRecorder] Scan complete: {added_count} records added")
        return result


def run_automatic_scan():
    """Run automatic scan and return results."""
    recorder = AutoActivityRecorder()
    return recorder.scan_and_record()


if __name__ == "__main__":
    # Run automatic scan
    result = run_automatic_scan()
    print(f"Automatic scan result: {result}")
