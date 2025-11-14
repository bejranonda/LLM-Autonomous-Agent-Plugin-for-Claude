#!/usr/bin/env python3
#     Comprehensive Data Migration Script
    """
Migrates all scattered data from multiple sources into unified parameter storage
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


def load_json_file(file_path: Path) -> Dict[str, Any]:
    """Load JSON file with error handling."""
    try:
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Warning: Error loading {file_path}: {e}")
        return {}


def save_json_file(data: Dict[str, Any], file_path: Path):
    """Save JSON file with proper formatting."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error: Failed to save {file_path}: {e}")
        return False


def migrate_quality_history() -> Dict[str, Any]:
    """Migrate quality history from .claude-patterns/quality_history.json"""
    quality_file = Path(".claude-patterns/quality_history.json")
    quality_data = load_json_file(quality_file)

    migrated = {"assessments": [], "timeline": [], "statistics": {}}

    if "quality_assessments" in quality_data:
        for assessment in quality_data["quality_assessments"]:
            # Convert to unified format
            unified_assessment = {
                "assessment_id": assessment.get("assessment_id"),
                "timestamp": assessment.get("timestamp"),
                "overall_score": assessment.get("overall_score", 0),
                "pass": assessment.get("pass", False),
                "task_type": assessment.get("task_type"),
                "breakdown": assessment.get("breakdown", {}),
                "details": assessment.get("details", {}),
                "issues_found": assessment.get("issues_found", []),
                "recommendations": assessment.get("recommendations", []),
                "skills_used": assessment.get("skills_used", []),
                "migration_source": "quality_history.json",
            }
            migrated["assessments"].append(unified_assessment)

            # Add timeline entry
            timeline_entry = {
                "timestamp": assessment.get("timestamp"),
                "score": assessment.get("overall_score", 0),
                "model_used": assessment.get("details", {}).get("model_used", "Unknown"),
                "task_type": assessment.get("task_type", "unknown"),
            }
            migrated["timeline"].append(timeline_entry)

    # Calculate statistics
    if migrated["assessments"]:
        scores = [a["overall_score"] for a in migrated["assessments"]]
        migrated["statistics"] = {
            "total_assessments": len(migrated["assessments"]),
            "average_score": sum(scores) / len(scores),
            "pass_rate": sum(1 for a in migrated["assessments"] if a["pass"]) / len(migrated["assessments"]),
            "latest_score": scores[-1] if scores else 0,
        }

    print(f"Migrated {len(migrated['assessments'])} quality assessments")
    return migrated


def migrate_patterns() -> Dict[str, Any]:
    """Migrate patterns from .claude-patterns/patterns.json"""
    patterns_file = Path(".claude-patterns/patterns.json")
    patterns_data = load_json_file(patterns_file)

    migrated = {
        "project_context": patterns_data.get("project_context", {}),
        "patterns": [],
        "skill_effectiveness": {},
        "agent_performance": {},
    }

    if "patterns" in patterns_data:
        for pattern in patterns_data["patterns"]:
            # Convert to unified format
            unified_pattern = {
                "pattern_id": pattern.get("pattern_id"),
                "timestamp": pattern.get("timestamp"),
                "task_type": pattern.get("task_type"),
                "context": pattern.get("context", {}),
                "execution": pattern.get("execution", {}),
                "outcome": pattern.get("outcome", {}),
                "reuse_count": pattern.get("reuse_count", 0),
                "migration_source": "patterns.json",
            }
            migrated["patterns"].append(unified_pattern)

    # Extract skill effectiveness
    if "skill_effectiveness" in patterns_data:
        migrated["skill_effectiveness"] = patterns_data["skill_effectiveness"]

    if "agent_performance" in patterns_data:
        migrated["agent_performance"] = patterns_data["agent_performance"]

    print(f"Migrated {len(migrated['patterns'])} learning patterns")
    return migrated


def migrate_assessments() -> Dict[str, Any]:
    """Migrate assessments from .claude-patterns/assessments.json"""
    assessments_file = Path(".claude-patterns/assessments.json")
    assessments_data = load_json_file(assessments_file)

    migrated = {"validations": [], "plugin_validations": []}

    if "assessments" in assessments_data:
        for assessment in assessments_data["assessments"]:
            unified_assessment = {
                "assessment_id": assessment.get("assessment_id"),
                "timestamp": assessment.get("timestamp"),
                "command_name": assessment.get("command_name"),
                "assessment_type": assessment.get("assessment_type"),
                "overall_score": assessment.get("overall_score", 0),
                "breakdown": assessment.get("breakdown", {}),
                "details": assessment.get("details", {}),
                "issues_found": assessment.get("issues_found", []),
                "recommendations": assessment.get("recommendations", []),
                "agents_used": assessment.get("agents_used", []),
                "migration_source": "assessments.json",
            }

            if assessment.get("assessment_type") == "plugin-validation":
                migrated["plugin_validations"].append(unified_assessment)
            else:
                migrated["validations"].append(unified_assessment)

    print(f"Migrated {len(migrated['validations']) + len(migrated['plugin_validations'])} assessments")
    return migrated


def migrate_model_performance() -> Dict[str, Any]:
    """Migrate model performance from various sources"""
    model_perf_file = Path(".claude-patterns/model_performance.json")
    model_data = load_json_file(model_perf_file)

    migrated = {"models": {}, "usage_stats": {"total_queries": 0, "model_switches": 0, "preferred_models": []}}

    # Handle different model performance data structures
    if "models" in model_data:
        for model_name, model_stats in model_data["models"].items():
            migrated["models"][model_name] = {
                "scores": model_stats.get("scores", []),
                "success_rate": model_stats.get("success_rate", 0.0),
                "contribution": model_stats.get("contribution", 0.0),
                "total_tasks": model_stats.get("total_tasks", 0),
                "last_updated": model_stats.get("last_updated", datetime.now().isoformat()),
                "migration_source": "model_performance.json",
            }
    else:
        # Handle direct model data structure
        for model_name, model_stats in model_data.items():
            if isinstance(model_stats, dict):
                migrated["models"][model_name] = {
                    "scores": model_stats.get("recent_scores", model_stats.get("scores", [])),
                    "success_rate": model_stats.get("success_rate", 0.0),
                    "contribution": model_stats.get("contribution_to_project", model_stats.get("contribution", 0.0)),
                    "total_tasks": model_stats.get("total_tasks", 0),
                    "last_updated": model_stats.get("last_updated", datetime.now().isoformat()),
                    "migration_source": "model_performance.json",
                }

    print(f"Migrated performance data for {len(migrated['models'])} models")
    return migrated


def migrate_autofix_patterns() -> Dict[str, Any]:
    """Migrate auto-fix patterns from patterns/autofix-patterns.json"""
    autofix_file = Path("patterns/autofix-patterns.json")
    autofix_data = load_json_file(autofix_file)

    migrated = {"patterns": autofix_data, "success_rates": {}, "usage_stats": {}}

    print(f"Migrated {len(autofix_data)} auto-fix patterns")
    return migrated


def create_unified_storage() -> Dict[str, Any]:
    """Create the comprehensive unified storage structure."""
    return {
        "version": "2.0.0",
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "migration_sources": [],
            "total_records_migrated": 0,
            "migration_status": "in_progress",
        },
        "quality": {"assessments": {"current": {}, "history": [], "statistics": {}}, "timeline": [], "metrics": {}},
        "models": {"active_model": "GLM-4.6", "performance": {}, "usage_stats": {}},  # Based on recent usage
        "learning": {
            "patterns": {"project_context": {}, "patterns": [], "skill_effectiveness": {}, "agent_performance": {}},
            "analytics": {},
        },
        "validation": {"recent_validations": [], "plugin_validations": [], "compliance_status": {}},
        "autofix": {"patterns": {}, "success_rates": {}, "usage_stats": {}},
        "dashboard": {"metrics": {}, "real_time": {}, "charts": {}},
    }


def run_comprehensive_migration():
    """Run the comprehensive data migration."""
    print("Starting Comprehensive Data Migration...")
    print("=" * 50)

    # Create unified storage structure
    unified_data = create_unified_storage()
    migration_sources = []
    total_migrated = 0

    # 1. Migrate quality history
    print("\nMigrating Quality History...")
    quality_data = migrate_quality_history()
    if quality_data["assessments"]:
        unified_data["quality"]["assessments"]["history"] = quality_data["assessments"]
        unified_data["quality"]["timeline"] = quality_data["timeline"]
        unified_data["quality"]["assessments"]["statistics"] = quality_data["statistics"]
        migration_sources.append("quality_history.json")
        total_migrated += len(quality_data["assessments"])

    # 2. Migrate learning patterns
    print("\nMigrating Learning Patterns...")
    patterns_data = migrate_patterns()
    unified_data["learning"]["patterns"] = patterns_data
    migration_sources.append("patterns.json")
    total_migrated += len(patterns_data["patterns"])

    # 3. Migrate assessments
    print("\nMigrating Assessments...")
    assessments_data = migrate_assessments()
    unified_data["validation"]["recent_validations"] = assessments_data["validations"]
    unified_data["validation"]["plugin_validations"] = assessments_data["plugin_validations"]
    migration_sources.append("assessments.json")
    total_migrated += len(assessments_data["validations"]) + len(assessments_data["plugin_validations"])

    # 4. Migrate model performance
    print("\nMigrating Model Performance...")
    model_data = migrate_model_performance()
    unified_data["models"]["performance"] = model_data["models"]
    unified_data["models"]["usage_stats"] = model_data["usage_stats"]
    migration_sources.append("model_performance.json")
    total_migrated += len(model_data["models"])

    # 5. Migrate auto-fix patterns
    print("\nMigrating Auto-Fix Patterns...")
    autofix_data = migrate_autofix_patterns()
    unified_data["autofix"] = autofix_data
    migration_sources.append("autofix-patterns.json")
    total_migrated += len(autofix_data["patterns"])

    # Update metadata
    unified_data["metadata"]["migration_sources"] = migration_sources
    unified_data["metadata"]["total_records_migrated"] = total_migrated
    unified_data["metadata"]["migration_status"] = "completed"
    unified_data["metadata"]["last_updated"] = datetime.now().isoformat()

    # Set current quality assessment if available
    if unified_data["quality"]["assessments"]["history"]:
        latest = max(unified_data["quality"]["assessments"]["history"], key=lambda x: x.get("timestamp", ""))
        unified_data["quality"]["assessments"]["current"] = latest

    # Set active model based on most recent usage
    if unified_data["quality"]["timeline"]:
        recent_entries = [e for e in unified_data["quality"]["timeline"] if e.get("timestamp")]
        if recent_entries:
            latest_entry = max(recent_entries, key=lambda x: x.get("timestamp", ""))
            unified_data["models"]["active_model"] = latest_entry.get("model_used", "GLM-4.6")

    # Initialize dashboard metrics
    unified_data["dashboard"]["metrics"] = {
        "total_assessments": len(unified_data["quality"]["assessments"]["history"]),
        "current_quality_score": unified_data["quality"]["assessments"]["current"].get("overall_score", 0),
        "active_models": len(unified_data["models"]["performance"]),
        "total_patterns": len(unified_data["learning"]["patterns"]["patterns"]),
        "system_health": 100.0,
    }

    unified_data["dashboard"]["real_time"] = {
        "current_model": unified_data["models"]["active_model"],
        "last_activity": datetime.now().isoformat(),
        "last_migration": unified_data["metadata"]["last_updated"],
    }

    # Save unified data
    unified_dir = Path(".claude-unified")
    unified_dir.mkdir(exist_ok=True)

    unified_file = unified_dir / "unified_parameters.json"

    # Create backup of existing file
    if unified_file.exists():
        backup_file = unified_dir / f"unified_parameters_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        unified_file.rename(backup_file)
        print(f"Created backup: {backup_file}")

    # Save new unified data
    if save_json_file(unified_data, unified_file):
        print(f"\nMigration Complete!")
        print(f"Unified storage saved to: {unified_file}")
        print(f"Total records migrated: {total_migrated}")
        print(f"Sources processed: {', '.join(migration_sources)}")
        print(f"File size: {unified_file.stat().st_size:,} bytes")

        # Validate the migrated data
        print(f"\nValidating Migrated Data...")
        validation_results = validate_unified_data(unified_data)

        if validation_results["valid"]:
            print("Data validation passed!")
        else:
            print("Data validation issues found:")
            for error in validation_results["errors"]:
                print(f"   - {error}")

        if validation_results["warnings"]:
            print("Warnings:")
            for warning in validation_results["warnings"]:
                print(f"   - {warning}")

        return True
    else:
        print("Failed to save unified data")
        return False


def validate_unified_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate the unified data structure."""
    results = {"valid": True, "errors": [], "warnings": []}

    # Check required sections
    required_sections = ["quality", "models", "learning", "validation", "autofix", "dashboard"]
    for section in required_sections:
        if section not in data:
            results["valid"] = False
            results["errors"].append(f"Missing required section: {section}")

    # Validate quality data
    if "quality" in data:
        quality = data["quality"]
        if "assessments" in quality and "history" in quality["assessments"]:
            history = quality["assessments"]["history"]
            if history:
                # Check for duplicate assessment IDs
                ids = [a.get("assessment_id") for a in history if a.get("assessment_id")]
                duplicates = [aid for aid in set(ids) if ids.count(aid) > 1]
                if duplicates:
                    results["warnings"].append(f"Duplicate assessment IDs: {duplicates}")

                # Check score ranges
                invalid_scores = [a for a in history if not (0 <= a.get("overall_score", 0) <= 100)]
                if invalid_scores:
                    results["errors"].append(f"Found {len(invalid_scores)} assessments with invalid scores")

    # Validate model data
    if "models" in data and "performance" in data["models"]:
        models = data["models"]["performance"]
        for model_name, model_data in models.items():
            if "success_rate" in model_data and not (0 <= model_data["success_rate"] <= 1):
                results["errors"].append(f"Invalid success rate for model {model_name}")

    return results


if __name__ == "__main__":
    success = run_comprehensive_migration()
    sys.exit(0 if success else 1)
