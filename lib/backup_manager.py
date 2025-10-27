#!/usr/bin/env python3
"""
Automated Backup System for Critical Plugin Components

Provides versioned backups with automatic restoration capabilities.
Protects against accidental file loss during operations.
"""

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
# Windows compatibility imports
if sys.platform == "win32":
    import msvcrt
else:
    import fcntl


class BackupManager:
    """Manages automated backups and restoration operations"""

    def __init__(self, backup_dir: str = ".claude/backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # Critical files that must be protected
        self.critical_files = {
            "commands": [
                "commands/dev/auto.md",
                "commands/dev/release.md",
                "commands/dev/model-switch.md",
                "commands/dev/pr-review.md",
                "commands/analyze/project.md",
                "commands/analyze/quality.md",
                "commands/analyze/static.md",
                "commands/analyze/dependencies.md",
                "commands/validate/all.md",
                "commands/validate/fullstack.md",
                "commands/validate/plugin.md",
                "commands/validate/patterns.md",
                "commands/debug/eval.md",
                "commands/debug/gui.md",
                "commands/learn/init.md",
                "commands/learn/analytics.md",
                "commands/learn/performance.md",
                "commands/learn/predict.md",
                "commands/workspace/organize.md",
                "commands/workspace/reports.md",
                "commands/workspace/improve.md",
                "commands/monitor/recommend.md",
                "commands/monitor/dashboard.md"
            ],
            "agents": [
                "agents/orchestrator.md",
                "agents/code-analyzer.md",
                "agents/quality-controller.md",
                "agents/test-engineer.md",
                "agents/documentation-generator.md",
                "agents/learning-engine.md",
                "agents/background-task-manager.md"
            ],
            "skills": [
                "skills/pattern-learning/SKILL.md",
                "skills/code-analysis/SKILL.md",
                "skills/quality-standards/SKILL.md",
                "skills/testing-strategies/SKILL.md",
                "skills/documentation-best-practices/SKILL.md",
                "skills/validation-standards/SKILL.md",
                "skills/integrity-validation/SKILL.md"
            ],
            "configs": [
                ".claude-plugin/plugin.json"
            ]
        }

        # Backup metadata file
        self.metadata_file = self.backup_dir / "backup_metadata.json"
        self.lock_file = self.backup_dir / ".backup_lock"

    def acquire_lock(self) -> bool:
        """Acquire file lock for backup operations"""
        try:
            if sys.platform == "win32":
                self.lock_file.open('w').close()
                msvcrt.locking(self.lock_file.open('rb').fileno(), msvcrt.LK_NBLCK, 1)
            else:
                fd = self.lock_file.open('w').fileno()
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except (IOError, OSError):
            return False

    def release_lock(self):
        """Release file lock"""
        try:
            if self.lock_file.exists():
                self.lock_file.unlink()
        except:
            pass

    def create_backup(self, operation_name: str, reason: str = "pre-operation") -> str:
        """
        Create a backup of all critical files

        Args:
            operation_name: Name of operation (e.g., "command_restructure")
            reason: Reason for backup (pre-operation, manual, etc.)

        Returns:
            Backup ID (timestamp-based)
        """
        if not self.acquire_lock():
            raise RuntimeError("Backup operation already in progress")

        try:
            # Generate backup ID
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_id = f"{operation_name}_{timestamp}"
            backup_path = self.backup_dir / backup_id
            backup_path.mkdir(parents=True, exist_ok=True)

            backup_manifest = {
                "backup_id": backup_id,
                "operation": operation_name,
                "reason": reason,
                "timestamp": datetime.now().isoformat(),
                "files_backed_up": {},
                "files_failed": {},
                "git_commit": self._get_git_commit()
            }

            # Backup critical files
            for category, files in self.critical_files.items():
                backup_manifest["files_backed_up"][category] = {}
                category_dir = backup_path / category
                category_dir.mkdir(exist_ok=True)

                for file_path in files:
                    if Path(file_path).exists():
                        try:
                            # Create relative path structure
                            backup_file = category_dir / Path(file_path).name
                            backup_file.parent.mkdir(parents=True, exist_ok=True)

                            # Copy file with metadata
                            shutil.copy2(file_path, backup_file)

                            # Store metadata
                            backup_manifest["files_backed_up"][category][file_path] = {
                                "backup_path": str(backup_file),
                                "size": backup_file.stat().st_size,
                                "modified": datetime.fromtimestamp(backup_file.stat().st_mtime).isoformat(),
                                "hash": self._calculate_file_hash(file_path)
                            }
                        except Exception as e:
                            backup_manifest["files_failed"][file_path] = str(e)
                    else:
                        backup_manifest["files_failed"][file_path] = "File not found"

            # Save backup manifest
            manifest_path = backup_path / "backup_manifest.json"
            with open(manifest_path, 'w') as f:
                json.dump(backup_manifest, f, indent=2)

            # Update main metadata
            self._update_metadata(backup_id, operation_name, reason)

            # Cleanup old backups (keep last 20)
            self._cleanup_old_backups()

            return backup_id

        finally:
            self.release_lock()

    def restore_backup(self, backup_id: str, files_to_restore: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Restore files from backup

        Args:
            backup_id: ID of backup to restore from
            files_to_restore: Specific files to restore (None for all)

        Returns:
            Dictionary with restore results
        """
        backup_path = self.backup_dir / backup_id
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup {backup_id} not found")

        manifest_path = backup_path / "backup_manifest.json"
        if not manifest_path.exists():
            raise FileNotFoundError(f"Backup manifest not found for {backup_id}")

        with open(manifest_path, 'r') as f:
            backup_manifest = json.load(f)

        restore_results = {
            "backup_id": backup_id,
            "restored_files": {},
            "failed_files": {},
            "skipped_files": []
        }

        for category, category_files in backup_manifest["files_backed_up"].items():
            for original_path, backup_info in category_files.items():
                # Skip if not in requested files (when specific list provided)
                if files_to_restore and original_path not in files_to_restore:
                    continue

                try:
                    backup_file_path = backup_info["backup_path"]
                    if Path(backup_file_path).exists():
                        # Create directory structure if needed
                        Path(original_path).parent.mkdir(parents=True, exist_ok=True)

                        # Restore file
                        shutil.copy2(backup_file_path, original_path)

                        restore_results["restored_files"][original_path] = {
                            "restored_from": backup_file_path,
                            "original_size": backup_info["size"],
                            "restored_size": Path(original_path).stat().st_size
                        }
                    else:
                        restore_results["failed_files"][original_path] = "Backup file not found"

                except Exception as e:
                    restore_results["failed_files"][original_path] = str(e)

        return restore_results

    def list_backups(self) -> List[Dict[str, Any]]:
        """List all available backups with metadata"""
        backups = []

        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)

                for backup_id, backup_info in metadata.get("backups", {}).items():
                    backup_path = self.backup_dir / backup_id
                    if backup_path.exists():
                        backups.append({
                            "backup_id": backup_id,
                            "operation": backup_info.get("operation", "unknown"),
                            "reason": backup_info.get("reason", "unknown"),
                            "timestamp": backup_info.get("timestamp"),
                            "files_count": self._count_backup_files(backup_id),
                            "size_mb": self._calculate_backup_size(backup_id)
                        })

        return sorted(backups, key=lambda x: x["timestamp"], reverse=True)

    def validate_backup(self, backup_id: str) -> Dict[str, Any]:
        """
        Validate backup integrity

        Returns:
            Validation results with file integrity checks
        """
        backup_path = self.backup_dir / backup_id
        if not backup_path.exists():
            return {"valid": False, "error": "Backup not found"}

        manifest_path = backup_path / "backup_manifest.json"
        if not manifest_path.exists():
            return {"valid": False, "error": "Backup manifest missing"}

        try:
            with open(manifest_path, 'r') as f:
                backup_manifest = json.load(f)

            validation_result = {
                "valid": True,
                "backup_id": backup_id,
                "file_integrity": {},
                "missing_files": [],
                "corrupted_files": []
            }

            # Check each backed-up file
            for category, category_files in backup_manifest["files_backed_up"].items():
                for original_path, backup_info in category_files.items():
                    backup_file_path = backup_info["backup_path"]

                    if not Path(backup_file_path).exists():
                        validation_result["missing_files"].append(original_path)
                        validation_result["valid"] = False
                        continue

                    # Check file hash
                    current_hash = self._calculate_file_hash(backup_file_path)
                    original_hash = backup_info.get("hash")

                    if current_hash != original_hash:
                        validation_result["corrupted_files"].append(original_path)
                        validation_result["valid"] = False

                    validation_result["file_integrity"][original_path] = {
                        "exists": True,
                        "hash_match": current_hash == original_hash,
                        "size_match": Path(backup_file_path).stat().st_size == backup_info["size"]
                    }

            return validation_result

        except Exception as e:
            return {"valid": False, "error": str(e)}

    def _get_git_commit(self) -> Optional[str]:
        """Get current git commit hash"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except:
            return None

    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of file"""
        import hashlib

        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except:
            return "unknown"

    def _count_backup_files(self, backup_id: str) -> int:
        """Count files in backup"""
        backup_path = self.backup_dir / backup_id
        if not backup_path.exists():
            return 0

        count = 0
        for root, dirs, files in os.walk(backup_path):
            count += len(files)

        # Exclude manifest file from count
        return max(0, count - 1)

    def _calculate_backup_size(self, backup_id: str) -> float:
        """Calculate backup size in MB"""
        backup_path = self.backup_dir / backup_id
        if not backup_path.exists():
            return 0.0

        total_size = 0
        for root, dirs, files in os.walk(backup_path):
            for file in files:
                file_path = Path(root) / file
                if file_path.exists():
                    total_size += file_path.stat().st_size

        return round(total_size / (1024 * 1024), 2)

    def _update_metadata(self, backup_id: str, operation: str, reason: str):
        """Update main backup metadata file"""
        metadata = {"backups": {}}

        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)

        metadata["backups"][backup_id] = {
            "operation": operation,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        }

        # Track latest backup per operation type
        if "latest_backups" not in metadata:
            metadata["latest_backups"] = {}

        metadata["latest_backups"][operation] = backup_id

        # Update statistics
        metadata["total_backups"] = len(metadata["backups"])
        metadata["last_backup"] = datetime.now().isoformat()

        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)

    def _cleanup_old_backups(self, keep_count: int = 20):
        """Remove old backups, keeping only the most recent ones"""
        backups = self.list_backups()

        if len(backups) > keep_count:
            # Remove oldest backups
            for backup in backups[keep_count:]:
                backup_path = self.backup_dir / backup["backup_id"]
                try:
                    shutil.rmtree(backup_path)
                except:
                    pass

    def auto_backup_before_operation(self, operation_name: str, files_to_modify: List[str]) -> str:
        """
        Automatically create backup before an operation

        Args:
            operation_name: Name of the upcoming operation
            files_to_modify: List of files that will be modified

        Returns:
            Backup ID if backup created, None otherwise
        """
        # Check if any critical files are being modified
        critical_files_to_backup = set()

        for file_to_modify in files_to_modify:
            for category, critical_files in self.critical_files.items():
                if file_to_modify in critical_files:
                    critical_files_to_backup.add(file_to_modify)

        if critical_files_to_backup:
            # Create backup with specific critical files
            backup_id = self.create_backup(
                operation_name=operation_name,
                reason=f"auto_backup_before_{operation_name}"
            )
            return backup_id

        return None


def main():
    """CLI interface for backup manager"""
    import argparse

    parser = argparse.ArgumentParser(description="Automated Backup Manager")
    parser.add_argument("action", choices=["create", "restore", "list", "validate", "auto-backup"])
    parser.add_argument("--operation", help="Operation name for backup")
    parser.add_argument("--reason", help="Reason for backup")
    parser.add_argument("--backup-id", help="Backup ID to restore/validate")
    parser.add_argument("--files", nargs="+", help="Specific files to restore")
    parser.add_argument("--files-to-modify", nargs="+", help="Files that will be modified (for auto-backup)")
    parser.add_argument("--backup-dir", default=".claude/backups", help="Backup directory")

    args = parser.parse_args()

    backup_manager = BackupManager(args.backup_dir)

    if args.action == "create":
        if not args.operation:
            args.operation = "manual_backup"

        backup_id = backup_manager.create_backup(
            operation_name=args.operation,
            reason=args.reason or "manual"
        )
        print(f"✅ Backup created: {backup_id}")

    elif args.action == "restore":
        if not args.backup_id:
            print("❌ --backup-id required for restore")
            sys.exit(1)

        results = backup_manager.restore_backup(args.backup_id, args.files)

        print(f"📦 Restore from backup: {args.backup_id}")
        print(f"✅ Restored {len(results['restored_files'])} files")
        if results["failed_files"]:
            print(f"❌ Failed to restore {len(results['failed_files'])} files")
            for file, error in results["failed_files"].items():
                print(f"   {file}: {error}")

    elif args.action == "list":
        backups = backup_manager.list_backups()

        if backups:
            print(f"📋 Available Backups ({len(backups)}):")
            for backup in backups:
                print(f"   {backup['backup_id']}")
                print(f"   Operation: {backup['operation']}")
                print(f"   Files: {backup['files_count']}")
                print(f"   Size: {backup['size_mb']} MB")
                print(f"   Created: {backup['timestamp']}")
                print()
        else:
            print("📭 No backups found")

    elif args.action == "validate":
        if not args.backup_id:
            print("❌ --backup-id required for validate")
            sys.exit(1)

        validation = backup_manager.validate_backup(args.backup_id)

        if validation["valid"]:
            print(f"✅ Backup {args.backup_id} is valid")
        else:
            print(f"❌ Backup {args.backup_id} has issues:")
            if "error" in validation:
                print(f"   {validation['error']}")
            if validation.get("missing_files"):
                print(f"   Missing files: {len(validation['missing_files'])}")
            if validation.get("corrupted_files"):
                print(f"   Corrupted files: {len(validation['corrupted_files'])}")

    elif args.action == "auto-backup":
        if not args.operation or not args.files_to_modify:
            print("❌ --operation and --files-to-modify required for auto-backup")
            sys.exit(1)

        backup_id = backup_manager.auto_backup_before_operation(
            args.operation, args.files_to_modify
        )

        if backup_id:
            print(f"🔒 Auto-backup created: {backup_id}")
        else:
            print("ℹ️  No critical files to backup")


if __name__ == "__main__":
    main()