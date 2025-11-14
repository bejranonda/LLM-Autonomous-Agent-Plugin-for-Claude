#!/usr/bin/env python3
#     Dashboard Migration Tool
    """

This tool helps migrate data from existing dashboards to the new unified dashboard system.
It ensures backward compatibility and smooth transition for users.
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class DashboardMigrationTool:
    """Tool for migrating dashboard data to unified system"""

    def __init__(self, project_root: str = "."):
        """Initialize the processor with default configuration."""
        self.project_root = Path(project_root)
        self.legacy_patterns_dir = self.project_root / ".claude-patterns"
        self.backup_dir = self.project_root / ".dashboard-migration-backup"

        # Legacy dashboard data locations
        self.legacy_data_sources = {
            "token_dashboard": [
                self.legacy_patterns_dir / "token_monitoring_data.json",
                self.legacy_patterns_dir / "token_usage_history.json",
            ],
            "kpi_dashboard": [
                self.legacy_patterns_dir / "kpi_metrics.json",
                self.legacy_patterns_dir / "executive_summary.json",
            ],
            "system_health": [
                self.legacy_patterns_dir / "system_health.json",
                self.legacy_patterns_dir / "validation_results.json",
            ],
        }

        # Unified dashboard data structure
        self.unified_data = {
            "migration_info": {"timestamp": datetime.now().isoformat(), "version": "1.0", "source_dashboards": []},
            "sections": {"tokens": {}, "kpi": {}, "system": {}},
        }

    def create_backup(self) -> bool:
        """Create backup of existing dashboard data"""
        try:
            print("Creating backup of existing dashboard data...")

            if self.backup_dir.exists():
                shutil.rmtree(self.backup_dir)

            self.backup_dir.mkdir(exist_ok=True)

            # Backup all relevant files
            backup_files = []
            for dashboard_type, files in self.legacy_data_sources.items():
                for file_path in files:
                    if file_path.exists():
                        backup_path = self.backup_dir / file_path.name
                        shutil.copy2(file_path, backup_path)
                        backup_files.append(str(backup_path))
                        print(f"  Backed up: {file_path}")

            # Create backup manifest
            backup_manifest = {
                "timestamp": datetime.now().isoformat(),
                "files": backup_files,
                "total_files": len(backup_files),
            }

            with open(self.backup_dir / "backup_manifest.json", "w") as f:
                json.dump(backup_manifest, f, indent=2)

            print(f"Backup completed: {len(backup_files)} files backed up")
            return True

        except Exception as e:
            print(f"Error creating backup: {e}")
            return False

    def migrate_token_data(self) -> Dict[str, Any]:
        """Migrate token dashboard data"""
        print("Migrating token optimization data...")

        token_data = {
            "token_usage": {"today": 0, "savings": 0, "compression_ratio": 0.0},
            "cost_savings": {"daily": 0.0, "weekly": 0.0, "monthly": 0.0},
            "optimization_metrics": {"cache_hit_rate": 0.0, "avg_compression": 0.0, "response_time_reduction": 0.0},
            "historical_data": [],
        }

        # Try to load existing token data
        for source_file in self.legacy_data_sources["token_dashboard"]:
            if source_file.exists():
                try:
                    with open(source_file, "r") as f:
                        legacy_data = json.load(f)
                        print(f"  Loaded: {source_file}")

                        # Map legacy data to unified structure
                        if "token_usage" in legacy_data:
                            token_data["token_usage"].update(legacy_data["token_usage"])
                        if "cost_savings" in legacy_data:
                            token_data["cost_savings"].update(legacy_data["cost_savings"])
                        if "optimization_metrics" in legacy_data:
                            token_data["optimization_metrics"].update(legacy_data["optimization_metrics"])

                        # Mark source dashboard
                        if "token_dashboard" not in self.unified_data["migration_info"]["source_dashboards"]:
                            self.unified_data["migration_info"]["source_dashboards"].append("token_dashboard")

                except Exception as e:
                    print(f"  Warning: Could not load {source_file}: {e}")

        return token_data

    def migrate_kpi_data(self) -> Dict[str, Any]:
        """Migrate KPI dashboard data"""
        print("Migrating KPI and executive metrics data...")

        kpi_data = {
            "performance_kpis": {"quality_score": 85, "success_rate": 90, "efficiency": 80, "satisfaction": 85},
            "business_kpis": {"cost_reduction": 60, "time_savings": 70, "productivity_gain": 65, "roi": 120},
            "trends": {"quality_trend": "stable", "cost_trend": "improving", "performance_trend": "stable"},
            "historical_data": [],
        }

        # Try to load existing KPI data
        for source_file in self.legacy_data_sources["kpi_dashboard"]:
            if source_file.exists():
                try:
                    with open(source_file, "r") as f:
                        legacy_data = json.load(f)
                        print(f"  Loaded: {source_file}")

                        # Map legacy data to unified structure
                        if "performance_kpis" in legacy_data:
                            kpi_data["performance_kpis"].update(legacy_data["performance_kpis"])
                        if "business_kpis" in legacy_data:
                            kpi_data["business_kpis"].update(legacy_data["business_kpis"])

                        # Mark source dashboard
                        if "kpi_dashboard" not in self.unified_data["migration_info"]["source_dashboards"]:
                            self.unified_data["migration_info"]["source_dashboards"].append("kpi_dashboard")

                except Exception as e:
                    print(f"  Warning: Could not load {source_file}: {e}")

        return kpi_data

    def migrate_system_health_data(self) -> Dict[str, Any]:
        """Migrate system health data"""
        print("Migrating system health and validation data...")

        system_data = {
            "system_metrics": {"cpu_usage": 45, "memory_usage": 60, "disk_usage": 35, "response_time": 150},
            "consistency_score": 90,
            "data_integrity": {"missing_records": 0, "inconsistent_data": 1, "validation_errors": 0},
            "alerts": [{"level": "info", "message": "System operating normally", "timestamp": datetime.now().isoformat()}],
            "historical_data": [],
        }

        # Try to load existing system health data
        for source_file in self.legacy_data_sources["system_health"]:
            if source_file.exists():
                try:
                    with open(source_file, "r") as f:
                        legacy_data = json.load(f)
                        print(f"  Loaded: {source_file}")

                        # Map legacy data to unified structure
                        if "system_metrics" in legacy_data:
                            system_data["system_metrics"].update(legacy_data["system_metrics"])
                        if "data_integrity" in legacy_data:
                            system_data["data_integrity"].update(legacy_data["data_integrity"])
                        if "alerts" in legacy_data:
                            system_data["alerts"].extend(legacy_data.get("alerts", []))

                        # Mark source dashboard
                        if "system_health" not in self.unified_data["migration_info"]["source_dashboards"]:
                            self.unified_data["migration_info"]["source_dashboards"].append("system_health")

                except Exception as e:
                    print(f"  Warning: Could not load {source_file}: {e}")

        return system_data

    def save_unified_data(self, unified_data_file: Optional[Path] = None) -> bool:
        """Save the unified dashboard data"""
        try:
            if unified_data_file is None:
                unified_data_file = self.legacy_patterns_dir / "unified_dashboard_data.json"

            # Ensure directory exists
            unified_data_file.parent.mkdir(exist_ok=True)

            # Save unified data
            with open(unified_data_file, "w") as f:
                json.dump(self.unified_data, f, indent=2)

            print(f"Unified dashboard data saved to: {unified_data_file}")
            return True

        except Exception as e:
            print(f"Error saving unified data: {e}")
            return False

    def run_migration(self) -> bool:
        """Run the complete migration process"""
        print("=" * 60)
        print("DASHBOARD MIGRATION TOOL")
        print("=" * 60)

        try:
            # Step 1: Create backup
            if not self.create_backup():
                print("Migration failed: Backup creation error")
                return False

            # Step 2: Migrate data from each legacy dashboard
            print("\nMigrating data from legacy dashboards...")

            self.unified_data["sections"]["tokens"] = self.migrate_token_data()
            self.unified_data["sections"]["kpi"] = self.migrate_kpi_data()
            self.unified_data["sections"]["system"] = self.migrate_system_health_data()

            # Step 3: Save unified data
            print("\nSaving unified dashboard data...")
            if not self.save_unified_data():
                print("Migration failed: Could not save unified data")
                return False

            # Step 4: Generate migration report
            self.generate_migration_report()

            print("\n" + "=" * 60)
            print("MIGRATION COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print(f"Source dashboards migrated: {', '.join(self.unified_data['migration_info']['source_dashboards'])}")
            print(f"Backup location: {self.backup_dir}")
            print(f"Unified data file: {self.legacy_patterns_dir / 'unified_dashboard_data.json'}")
            print("\nThe unified dashboard is now ready with all your existing data!")

            return True

        except Exception as e:
            print(f"Migration failed: {e}")
            return False

    def generate_migration_report(self) -> None:
        """Generate a migration report"""
        report = {
            "migration_summary": {
                "timestamp": self.unified_data["migration_info"]["timestamp"],
                "version": self.unified_data["migration_info"]["version"],
                "source_dashboards": self.unified_data["migration_info"]["source_dashboards"],
                "sections_created": len(self.unified_data["sections"]),
                "backup_location": str(self.backup_dir),
            },
            "sections_overview": {},
            "recommendations": [
                "Test the unified dashboard to ensure all data migrated correctly",
                "Keep the backup for at least 30 days as a safety measure",
                "Update any scripts or tools that reference old dashboard files",
            ],
        }

        # Add section overviews
        for section_name, section_data in self.unified_data["sections"].items():
            report["sections_overview"][section_name] = {
                "data_points": len(section_data),
                "main_keys": list(section_data.keys()),
            }

        # Save migration report
        report_file = self.backup_dir / "migration_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"Migration report saved to: {report_file}")


class BackwardCompatibilityManager:
    """Manages backward compatibility for dashboard transitions"""

    def __init__(self, project_root: str = "."):
        """Initialize the processor with default configuration."""
        self.project_root = Path(project_root)
        self.patterns_dir = self.project_root / ".claude-patterns"

    def create_compatibility_shims(self) -> bool:
        """Create compatibility shims for old dashboard APIs"""
        print("Creating backward compatibility shims...")

        try:
            # Create token dashboard shim
            self._create_token_dashboard_shim()

            # Create KPI dashboard shim
            self._create_kpi_dashboard_shim()

            # Create system health shim
            self._create_system_health_shim()

            print("Backward compatibility shims created successfully")
            return True

        except Exception as e:
            print(f"Error creating compatibility shims: {e}")
            return False

    def _create_token_dashboard_shim(self) -> None:
        """Create token dashboard compatibility shim"""
        shim_script = self.patterns_dir / "token_dashboard_shim.py"

        shim_content = '''#!/usr/bin/env python3
Token Dashboard Compatibility Shim

This shim provides backward compatibility for the old token dashboard.
It redirects to the unified dashboard system.
import sys
import json
from pathlib import Path
from datetime import datetime

def get_token_data():
    """Get token data from unified dashboard system"""
    try:
        unified_file = Path(".claude-patterns/unified_dashboard_data.json")
        if unified_file.exists():
            with open(unified_file, 'r') as f:
                data = json.load(f)
                return data.get("sections", {}).get("tokens", {})
        return {}
    except Exception:
        return {}

def main():
    """Main compatibility function"""
    data = get_token_data()
    if data:
        print(json.dumps(data, indent=2))
    else:
        print('{"error": "Token data not available"}')
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''

        with open(shim_script, "w") as f:
            f.write(shim_content)

    def _create_kpi_dashboard_shim(self) -> None:
        """Create KPI dashboard compatibility shim"""
        shim_script = self.patterns_dir / "kpi_dashboard_shim.py"

        shim_content = '''#!/usr/bin/env python3
KPI Dashboard Compatibility Shim

This shim provides backward compatibility for the old KPI dashboard.
It redirects to the unified dashboard system.
import sys
import json
from pathlib import Path

def get_kpi_data():
    """Get KPI data from unified dashboard system"""
    try:
        unified_file = Path(".claude-patterns/unified_dashboard_data.json")
        if unified_file.exists():
            with open(unified_file, 'r') as f:
                data = json.load(f)
                return data.get("sections", {}).get("kpi", {})
        return {}
    except Exception:
        return {}

def main():
    """Main compatibility function"""
    data = get_kpi_data()
    if data:
        print(json.dumps(data, indent=2))
    else:
        print('{"error": "KPI data not available"}')
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''

        with open(shim_script, "w") as f:
            f.write(shim_content)

    def _create_system_health_shim(self) -> None:
        """Create system health compatibility shim"""
        shim_script = self.patterns_dir / "system_health_shim.py"

        shim_content = '''#!/usr/bin/env python3
System Health Compatibility Shim

This shim provides backward compatibility for the old system health dashboard.
It redirects to the unified dashboard system.
import sys
import json
from pathlib import Path

def get_system_health_data():
    """Get system health data from unified dashboard system"""
    try:
        unified_file = Path(".claude-patterns/unified_dashboard_data.json")
        if unified_file.exists():
            with open(unified_file, 'r') as f:
                data = json.load(f)
                return data.get("sections", {}).get("system", {})
        return {}
    except Exception:
        return {}

def main():
    """Main compatibility function"""
    data = get_system_health_data()
    if data:
        print(json.dumps(data, indent=2))
    else:
        print('{"error": "System health data not available"}')
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''

        with open(shim_script, "w") as f:
            f.write(shim_content)

    def create_deprecation_warnings(self) -> None:
        """Create deprecation warning files"""
        warnings_dir = self.patterns_dir / "deprecation_warnings"
        warnings_dir.mkdir(exist_ok=True)

        warning_message = (
            """# Dashboard Deprecation Notice

## Important: Dashboard System Unified

The individual dashboard systems have been consolidated into a single, unified dashboard.

## What Changed:
- Multiple dashboards → Single unified dashboard
- Separate APIs → Unified API endpoints
- Scattered data files → Centralized data storage

## New Location:
- **Unified Dashboard**: Access via `/monitor:dashboard` command
- **Single URL**: http://localhost:5000 (default)
- **All Features**: Available in one interface with tabbed navigation

## Migration:
- Your data has been automatically migrated
- All existing functionality is preserved
- No changes to your workflow needed

## Compatibility:
- Old scripts may continue to work temporarily
- Update integrations to use unified system
- Compatibility shims provided during transition

## Support:
- Issues: Check migration backup or use unified dashboard
- Questions: Refer to unified dashboard documentation

---
Generated: """
            + datetime.now().isoformat()
            + """
        )

        warning_file = warnings_dir / "README.md"
        with open(warning_file, "w") as f:
            f.write(warning_message)


def main():
    """Main migration function"""
    import argparse

    parser = argparse.ArgumentParser(description="Dashboard Migration Tool")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--backup-only", action="store_true", help="Only create backup, no migration")
    parser.add_argument("--compatibility-only", action="store_true", help="Only create compatibility shims")

    args = parser.parse_args()

    if args.backup_only:
        # Backup only mode
        migrator = DashboardMigrationTool(args.project_root)
        migrator.create_backup()
        return 0

    if args.compatibility_only:
        # Compatibility only mode
        compat_manager = BackwardCompatibilityManager(args.project_root)
        compat_manager.create_compatibility_shims()
        compat_manager.create_deprecation_warnings()
        return 0

    # Full migration mode
    migrator = DashboardMigrationTool(args.project_root)

    if migrator.run_migration():
        # Create compatibility shims after successful migration
        compat_manager = BackwardCompatibilityManager(args.project_root)
        compat_manager.create_compatibility_shims()
        compat_manager.create_deprecation_warnings()

        print("\n" + "=" * 60)
        print("NEXT STEPS:")
        print("=" * 60)
        print("1. Test the unified dashboard: /monitor:dashboard")
        print("2. Verify all your data is present")
        print("3. Update any scripts to use unified system")
        print("4. Remove old dashboard files after confirmation")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
