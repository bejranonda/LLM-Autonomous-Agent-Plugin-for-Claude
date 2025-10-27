#!/usr/bin/env python3
"""
Validation Hooks System for Pre/Post Operation Integrity

Integrates validation into major operations to prevent component loss.
Provides automatic validation before and after critical operations.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from backup_manager import BackupManager
from command_validator import CommandValidator
from recovery_manager import RecoveryManager

# Windows compatibility imports
if sys.platform == "win32":
else:


class ValidationHook:
    """Individual validation hook for a specific operation"""

    def __init__(self, name: str, validator_func: Callable, critical: bool = True):
        self.name = name
        self.validator_func = validator_func
        self.critical = critical
        self.results = []
        self.enabled = True

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the validation hook"""
        if not self.enabled:
            return {"skipped": True, "reason": "Hook disabled"}

        try:
            result = self.validator_func(context)
            result["hook_name"] = self.name
            result["timestamp"] = datetime.now().isoformat()
            self.results.append(result)
            return result
        except Exception as e:
            error_result = {
                "hook_name": self.name,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            self.results.append(error_result)
            return error_result


class ValidationHookManager:
    """Manages validation hooks for operations"""

    def __init__(self, plugin_dir: str = "."):
        self.plugin_dir = Path(plugin_dir)
        self.hooks_dir = self.plugin_dir / ".claude" / "validation_hooks"
        self.hooks_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.backup_manager = BackupManager(
            str(self.plugin_dir / ".claude" / "backups"))
        self.command_validator = CommandValidator(str(plugin_dir))
        self.recovery_manager = RecoveryManager(str(plugin_dir))

        # Hook registry
        self.pre_hooks = {}
        self.post_hooks = {}

        # Operation tracking
        self.active_operations = {}
        self.operation_history = []

        # Initialize default hooks
        self._initialize_default_hooks()

    def register_pre_hook(self, operation: str, hook: ValidationHook):
        """Register a pre-operation hook"""
        if operation not in self.pre_hooks:
            self.pre_hooks[operation] = []
        self.pre_hooks[operation].append(hook)

    def register_post_hook(self, operation: str, hook: ValidationHook):
        """Register a post-operation hook"""
        if operation not in self.post_hooks:
            self.post_hooks[operation] = []
        self.post_hooks[operation].append(hook)

    def execute_pre_validation(
    self,
    operation: str,
    context: Dict[str,
    Any]) -> Dict[str, Any]:,


)
        """Execute all pre-operation validation hooks"""
        validation_result = {
            "operation": operation,
            "phase": "pre",
            "timestamp": datetime.now().isoformat(),
            "hooks_executed": 0,
            "hooks_passed": 0,
            "hooks_failed": 0,
            "critical_failures": 0,
            "overall_passed": True,
            "backup_created": False,
            "backup_id": None,
            "hook_results": [],
            "recommendations": []
        }

        # Check if operation has registered hooks
        if operation not in self.pre_hooks:
            validation_result["overall_passed"] = True
            validation_result["recommendations"].append(
    "No pre-validation hooks registered for this operation",
)
            return validation_result

        # Create backup before operation
        files_to_modify = context.get("files_to_modify", [])
        if files_to_modify:
            backup_id = self.backup_manager.auto_backup_before_operation(
                operation, files_to_modify)
            if backup_id:
                validation_result["backup_created"] = True
                validation_result["backup_id"] = backup_id

        # Execute all pre-hooks
        for hook in self.pre_hooks[operation]:
            validation_result["hooks_executed"] += 1

            hook_result = hook.execute(context)
            validation_result["hook_results"].append(hook_result)

            if hook_result.get("success", True):
                validation_result["hooks_passed"] += 1
            else:
                validation_result["hooks_failed"] += 1
                validation_result["overall_passed"] = False

                if hook.critical:
                    validation_result["critical_failures"] += 1

        # Generate recommendations
        validation_result["recommendations"] = self._generate_pre_validation_recommendations(
            validation_result)

        # Store operation context for post-validation
        self.active_operations[operation] = {
            "context": context,
            "pre_validation": validation_result,
            "start_time": datetime.now().isoformat()
        }

        # Save validation results
        self._save_validation_results(validation_result)

        return validation_result

    def execute_post_validation(
    self,
    operation: str,
    context: Dict[str,
    Any]) -> Dict[str, Any]:,
)
        """Execute all post-operation validation hooks"""
        validation_result = {
            "operation": operation,
            "phase": "post",
            "timestamp": datetime.now().isoformat(),
            "hooks_executed": 0,
            "hooks_passed": 0,
            "hooks_failed": 0,
            "critical_failures": 0,
            "overall_passed": True,
            "issues_detected": [],
            "auto_recovery_attempted": False,
            "auto_recovery_results": {},
            "hook_results": [],
            "recommendations": []
        }

        # Check if operation has registered hooks
        if operation not in self.post_hooks:
            validation_result["overall_passed"] = True
            validation_result["recommendations"].append(
    "No post-validation hooks registered for this operation",
)
            return validation_result

        # Get pre-validation context for comparison
        pre_validation = None
        if operation in self.active_operations:
            pre_validation = self.active_operations[operation]["pre_validation"]

        # Execute all post-hooks
        for hook in self.post_hooks[operation]:
            validation_result["hooks_executed"] += 1

            # Add pre-validation context to post-validation
            hook_context = context.copy()
            if pre_validation:
                hook_context["pre_validation_results"] = pre_validation

            hook_result = hook.execute(hook_context)
            validation_result["hook_results"].append(hook_result)

            if hook_result.get("success", True):
                validation_result["hooks_passed"] += 1
            else:
                validation_result["hooks_failed"] += 1
                validation_result["overall_passed"] = False

                if hook.critical:
                    validation_result["critical_failures"] += 1

                # Collect issues for recovery
                if "issues" in hook_result:
                    validation_result["issues_detected"].extend(hook_result["issues"])

        # Attempt auto-recovery for critical issues
        if validation_result["issues_detected"] and 
            validation_result["critical_failures"] > 0:
            recovery_results = self._attempt_auto_recovery(validation_result["issues_detected"])
            validation_result["auto_recovery_attempted"] = True
            validation_result["auto_recovery_results"] = recovery_results

        # Generate recommendations
        validation_result["recommendations"] = self._generate_post_validation_recommendations(validation_result)

        # Complete operation tracking
        if operation in self.active_operations:
            operation_data = self.active_operations[operation]
            operation_data["post_validation"] = validation_result
            operation_data["end_time"] = datetime.now().isoformat()

            self.operation_history.append(operation_data)
            del self.active_operations[operation]

        # Save validation results
        self._save_validation_results(validation_result)

        return validation_result

    def wrap_operation_with_validation(
    self,
    operation: str,
    operation_func: Callable,
    **kwargs):,
)
        """
        Wrap an operation function with automatic validation

        Example:
        result = hook_manager.wrap_operation_with_validation(
            "command_restructure",
            restructure_commands,
            category="monitor",
            new_commands=["dashboard"]
        )
        """
        context = kwargs.copy()
        context["operation_name"] = operation

        # Pre-validation
        pre_result = self.execute_pre_validation(operation, context)

        # Check if pre-validation passed
        if not pre_result["overall_passed"] and pre_result["critical_failures"] > 0:
            return {
                "success": False,
                "error": "Pre-operation validation failed",
                "pre_validation": pre_result,
                "operation_aborted": True
            }

        try:
            # Execute the actual operation
            operation_result = operation_func(**kwargs)

            # Post-validation
            post_result = self.execute_post_validation(operation, context)

            # Return combined result
            return {
                "success": True,
                "operation_result": operation_result,
                "pre_validation": pre_result,
                "post_validation": post_result,
                "validation_passed": post_result["overall_passed"]
            }

        except Exception as e:
            # Operation failed, still try post-validation if possible
            try:
                post_result = self.execute_post_validation(operation, context)
            except:
                post_result = {"error": "Post-validation failed after operation error"}

            return {
                "success": False,
                "error": str(e),
                "pre_validation": pre_result,
                "post_validation": post_result,
                "operation_failed": True
            }

    def _initialize_default_hooks(self):
        """Initialize default validation hooks for common operations"""

        # Command operations
        self._register_command_hooks()

        # Agent operations
        self._register_agent_hooks()

        # File operations
        self._register_file_hooks()

        # Plugin operations
        self._register_plugin_hooks()

    def _register_command_hooks(self):
        """Register hooks for command operations"""

        # Pre-hook for command restructuring
        pre_command_restructure = ValidationHook(
            name="command_inventory_check",
            validator_func=self._validate_command_inventory,
            critical=True
        )
        self.register_pre_hook("command_restructure", pre_command_restructure)

        # Post-hook for command validation
        post_command_restructure = ValidationHook(
            name="command_integrity_check",
            validator_func=self._validate_command_integrity,
            critical=True
        )
        self.register_post_hook("command_restructure", post_command_restructure)

        # Hooks for command creation
        pre_command_create = ValidationHook(
            name="command_creation_pre_check",
            validator_func=self._validate_command_creation_prerequisites,
            critical=False
        )
        self.register_pre_hook("command_create", pre_command_create)

    def _register_agent_hooks(self):
        """Register hooks for agent operations"""

        # Pre-hook for agent modifications
        pre_agent_modify = ValidationHook(
            name="agent_backup_check",
            validator_func=self._validate_agent_modification,
            critical=True
        )
        self.register_pre_hook("agent_modify", pre_agent_modify)

        # Post-hook for agent validation
        post_agent_modify = ValidationHook(
            name="agent_integrity_check",
            validator_func=self._validate_agent_integrity,
            critical=True
        )
        self.register_post_hook("agent_modify", post_agent_modify)

    def _register_file_hooks(self):
        """Register hooks for file operations"""

        # Pre-hook for file system changes
        pre_file_changes = ValidationHook(
            name="file_inventory_snapshot",
            validator_func=self._create_file_inventory,
            critical=True
        )
        self.register_pre_hook("file_system_changes", pre_file_changes)

        # Post-hook for file validation
        post_file_changes = ValidationHook(
            name="file_integrity_check",
            validator_func=self._validate_file_integrity,
            critical=True
        )
        self.register_post_hook("file_system_changes", post_file_changes)

    def _register_plugin_hooks(self):
        """Register hooks for plugin operations"""

        # Pre-hook for plugin improvements
        pre_plugin_improve = ValidationHook(
            name="plugin_backup",
            validator_func=self._validate_plugin_modification,
            critical=True
        )
        self.register_pre_hook("plugin_improve", pre_plugin_improve)

        # Post-hook for plugin validation
        post_plugin_improve = ValidationHook(
            name="plugin_validation",
            validator_func=self._validate_plugin_integrity,
            critical=True
        )
        self.register_post_hook("plugin_improve", post_plugin_improve)

    # Hook validation functions
    def _validate_command_inventory(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate command inventory before restructuring"""
        validation = self.command_validator.validate_all_commands()

        result = {
            "success": validation["summary"]["overall_score"] >= 70,
            "validation": validation,
            "issues": []
        }

        if not result["success"]:
            result["issues"] = [
                f"Command system integrity score: {validation['summary']['overall_score']}/100",
                f"Missing commands: {len(validation['missing_commands'])}",
                f"Discoverability issues: {len(validation['discoverability_issues'])}"
            ]

        return result

    def _validate_command_integrity(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate command integrity after restructuring"""
        validation = self.command_validator.validate_all_commands()

        result = {
            "success": validation["summary"]["overall_score"] >= 80,
            "validation": validation,
            "issues": []
        }

        # Compare with pre-validation if available
        pre_validation = context.get("pre_validation_results")
        if pre_validation:
            pre_score = pre_validation.get("validation", {}).get("summary", {}).get("overall_score", 0)
            current_score = validation["summary"]["overall_score"]

            if current_score < pre_score:
                result["success"] = False
                result["issues"].append(
    f"Command integrity degraded: {pre_score} → {current_score}",
)

        # Check for new missing commands
        if validation["missing_commands"]:
            result["success"] = False
            result["issues"].extend([
                f"Missing command: {cmd['command']}" for cmd in 
                    validation["missing_commands"]
            ])

        return result

    def _validate_command_creation_prerequisites(
    self,
    context: Dict[str,
    Any]) -> Dict[str, Any]:,
)
        """Validate prerequisites for command creation"""
        category = context.get("category")
        name = context.get("name")

        result = {
            "success": True,
            "issues": []
        }

        # Check if command already exists
        if category and name:
            command_path = Path(f"commands/{category}/{name}.md")
            if command_path.exists():
                result["success"] = False
                result["issues"].append(f"Command already exists: {command_path}")

        # Validate category exists
        if category and not Path(f"commands/{category}").exists():
            result["success"] = False
            result["issues"].append(
    f"Command category does not exist: commands/{category}/",
)

        return result

    def _validate_agent_modification(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate agent modification prerequisites"""
        agent_file = context.get("agent_file")

        result = {
            "success": True,
            "issues": []
        }

        if agent_file and not Path(agent_file).exists():
            result["success"] = False
            result["issues"].append(f"Agent file does not exist: {agent_file}")

        # Check if modifying critical agent
        critical_agents = ["agents/orchestrator.md", "agents/code-analyzer.md", "agents/quality-controller.md"]
        if agent_file and agent_file in critical_agents:
            result["issues"].append(f"Modifying critical agent: {agent_file}")

        return result

    def _validate_agent_integrity(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate agent integrity after modification"""
        result = {
            "success": True,
            "issues": []
        }

        agent_file = context.get("agent_file")
        if agent_file and Path(agent_file).exists():
            # Basic validation - file exists and has content
            try:
                with open(agent_file, 'r') as f:
                    content = f.read()

                if len(content) < 100:
                    result["success"] = False
                    result["issues"].append(
    f"Agent file seems too short: {len(content)} characters",
)

                # Check for YAML frontmatter
                if not content.startswith('---'):
                    result["success"] = False
                    result["issues"].append(f"Agent missing YAML frontmatter")

            except Exception as e:
                result["success"] = False
                result["issues"].append(f"Failed to read agent file: {str(e)}")

        return result

    def _create_file_inventory(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Create file inventory before file system changes"""
        inventory = {
            "commands": [],
            "agents": [],
            "skills": [],
            "configs": [],
            "timestamp": datetime.now().isoformat()
        }

        # Scan directories
        for item in self.plugin_dir.glob("commands/**/*.md"):
            inventory["commands"].append(str(item.relative_to(self.plugin_dir)))

        for item in self.plugin_dir.glob("agents/**/*.md"):
            inventory["agents"].append(str(item.relative_to(self.plugin_dir)))

        for item in self.plugin_dir.glob("skills/**/SKILL.md"):
            inventory["skills"].append(str(item.relative_to(self.plugin_dir)))

        for item in self.plugin_dir.glob(".claude-plugin/**/*.json"):
            inventory["configs"].append(str(item.relative_to(self.plugin_dir)))

        # Save inventory
        inventory_file = self.hooks_dir / f"inventory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(inventory_file, 'w') as f:
            json.dump(inventory, f, indent=2)

        return {
            "success": True,
            "inventory": inventory,
            "inventory_file": str(inventory_file)
        }

    def _validate_file_integrity(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate file integrity after changes"""
        result = {
            "success": True,
            "issues": [],
            "missing_files": [],
            "extra_files": []
        }

        # Get current inventory and compare with pre-operation
        current_inventory = {
            "commands": [str(
    p.relative_to(self.plugin_dir)) for p in self.plugin_dir.glob("commands/**/*.md")],,
)
            "agents": [str(
    p.relative_to(self.plugin_dir)) for p in self.plugin_dir.glob("agents/**/*.md")],,
)
            "skills": [str(
    p.relative_to(
    self.plugin_dir)) for p in self.plugin_dir.glob("skills/**/SKILL.md")],,,
)
)
            "configs": [str(
    p.relative_to(
    self.plugin_dir)) for p in self.plugin_dir.glob(".claude-plugin/**/*.json")],,
)
)
        }

        # Find missing critical files
        critical_files = [
            "commands/dev/auto.md",
            "commands/analyze/project.md",
            "commands/validate/all.md",
            "agents/orchestrator.md",
            "skills/pattern-learning/SKILL.md",
            ".claude-plugin/plugin.json"
        ]

        for critical_file in critical_files:
            if not (self.plugin_dir / critical_file).exists():
                result["success"] = False
                result["missing_files"].append(critical_file)

        return result

    def _validate_plugin_modification(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate plugin modification prerequisites"""
        result = {
            "success": True,
            "issues": []
        }

        # Check if plugin.json exists and is valid
        plugin_file = self.plugin_dir / ".claude-plugin" / "plugin.json"
        if plugin_file.exists():
            try:
                with open(plugin_file, 'r') as f:
                    plugin_data = json.load(f)

                required_fields = ["name", "version", "description"]
                for field in required_fields:
                    if field not in plugin_data:
                        result["issues"].append(
    f"Plugin missing required field: {field}",
)

            except json.JSONDecodeError:
                result["success"] = False
                result["issues"].append("Invalid JSON in plugin.json")
        else:
            result["issues"].append("Plugin manifest not found")

        return result

    def _validate_plugin_integrity(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate plugin integrity after modification"""
        result = {
            "success": True,
            "issues": []
        }

        # Validate plugin structure
        required_dirs = ["commands", "agents", "skills"]
        for dir_name in required_dirs:
            dir_path = self.plugin_dir / dir_name
            if not dir_path.exists():
                result["success"] = False
                result["issues"].append(f"Required directory missing: {dir_name}")

        return result

    def _attempt_auto_recovery(self, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Attempt automatic recovery for detected issues"""
        recovery_results = {
            "attempted": True,
            "success": False,
            "recovered_components": 0,
            "failed_recoveries": 0,
            "recovery_details": []
        }

        # Group issues by component type
        missing_commands = []
        for issue in issues:
            if isinstance(issue, str) and "/commands/" in issue:
                missing_commands.append(issue)

        if missing_commands:
            try:
                # Create validation results structure for recovery manager
                validation_results = {
                    "missing_commands": [{"command": cmd.replace(
    ".md",
    "").replace("commands/",
    "/").replace("/",
    ":")} for cmd in missing_commands],
)
                }

                recovery = self.recovery_manager.recover_missing_components(validation_results)
                recovery_results["recovery_details"].append(recovery)
                recovery_results["recovered_components"] = recovery["recovery_summary"]["total_recovered"]
                recovery_results["failed_recoveries"] = recovery["recovery_summary"]["total_failed"]
                recovery_results["success"] = recovery["recovery_summary"]["total_recovered"] > 
                    
                    0

            except Exception as e:
                recovery_results["error"] = str(e)

        return recovery_results

    def _generate_pre_validation_recommendations(
    self,
    validation_result: Dict[str,
    Any]) -> List[str]:,
)
        """Generate recommendations based on pre-validation results"""
        recommendations = []

        if not validation_result["overall_passed"]:
            if validation_result["critical_failures"] > 0:
                recommendations.append(
    "[CRITICAL] Critical validation failures detected. Operation aborted.",
)
                recommendations.append(
    "Fix critical issues before proceeding with the operation.",
)
            else:
                recommendations.append(
    "[WARNING] Non-critical validation failures detected.",
)
                recommendations.append("Proceed with caution and monitor for issues.")

        if not validation_result["backup_created"]:
            recommendations.append(
    "[RECOMMENDATION] Consider manual backup before operation.",
)

        return recommendations

    def _generate_post_validation_recommendations(
    self,
    validation_result: Dict[str,
    Any]) -> List[str]:,
)
        """Generate recommendations based on post-validation results"""
        recommendations = []

        if not validation_result["overall_passed"]:
            if validation_result["critical_failures"] > 0:
                recommendations.append("[CRITICAL] Post-operation validation failed.")

                if validation_result["auto_recovery_attempted"]:
                    auto_recovery = validation_result["auto_recovery_results"]
                    if auto_recovery.get("success", False):
                        recommendations.append(
    f"[RECOVERED] Auto-recovery restored {auto_recovery['recovered_components']} components.",
)
                    else:
                        recommendations.append(
    "[RECOVERY FAILED] Auto-recovery failed. Manual intervention required.",
)
                        recommendations.append(
    "Run manual recovery commands to restore missing components.",
)
                else:
                    recommendations.append(
    "[ACTION REQUIRED] Run recovery system to restore missing components.",
)

        if validation_result["hooks_failed"] > 0:
            recommendations.append(
    f"[INFO] {validation_result['hooks_failed']} validation hooks failed.",
)

        return recommendations

    def _save_validation_results(self, validation_result: Dict[str, Any]):
        """Save validation results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Milliseconds
        filename = f"validation_{validation_result['operation']}_{validation_result['phase']}_{timestamp}.json"
        filepath = self.hooks_dir / filename

        try:
            with open(filepath, 'w') as f:
                json.dump(validation_result, f, indent=2)
        except Exception as e:
            # Don't fail validation if saving fails
            pass


def main():
    """CLI interface for validation hooks"""
    import argparse

    parser = argparse.ArgumentParser(description="Validation Hooks Manager")
    parser.add_argument("action", choices=["test-hooks", "validate-operation"])
    parser.add_argument("--plugin-dir", default=".", help="Plugin directory")
    parser.add_argument("--operation", help="Operation name to validate")
    parser.add_argument("--context", help="Context JSON file")

    args = parser.parse_args()

    hook_manager = ValidationHookManager(args.plugin_dir)

    if args.action == "test-hooks":
        print("🔧 Testing validation hooks...")

        # Test command inventory hook
        test_context = {"operation_name": "test", "files_to_modify": ["commands/monitor/dashboard.md"]}
        result = hook_manager._validate_command_inventory(test_context)

        print(f"Command inventory hook: {'✅' if result['success'] else '❌'}")
        if not result['success']:
            for issue in result['issues']:
                print(f"  • {issue}")

    elif args.action == "validate-operation":
        if not args.operation:
            print("❌ --operation required")
            sys.exit(1)

        context = {}
        if args.context:
            with open(args.context, 'r') as f:
                context = json.load(f)

        print(f"🔍 Validating operation: {args.operation}")

        # Pre-validation
        pre_result = hook_manager.execute_pre_validation(args.operation, context)
        print(f"Pre-validation: {'✅' if pre_result['overall_passed'] else '❌'}")
        print(f"  Hooks executed: {pre_result['hooks_executed']}")
        print(f"  Hooks passed: {pre_result['hooks_passed']}")

        if pre_result["backup_created"]:
            print(f"  📦 Backup created: {pre_result['backup_id']}")

        if pre_result["recommendations"]:
            print("  Recommendations:")
            for rec in pre_result["recommendations"]:
                print(f"    {rec}")


if __name__ == "__main__":
    main()
