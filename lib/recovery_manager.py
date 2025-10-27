#!/usr/bin/env python3
"""
Recovery Manager for Automatic Component Restoration

Provides intelligent recovery mechanisms for missing components.
Uses multiple recovery strategies: backups, Git history, templates, and patterns.
"""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
# Import other modules
from backup_manager import BackupManager
from command_validator import CommandValidator

# Windows compatibility imports
if sys.platform == "win32":
else:


class RecoveryManager:
    """Manages automatic recovery of missing components"""

    def __init__(self, plugin_dir: str = "."):
        self.plugin_dir = Path(plugin_dir)
        self.backup_manager = BackupManager(str(self.plugin_dir / ".claude" / "backups"))
        self.command_validator = CommandValidator(str(plugin_dir))

        # Recovery strategies in order of preference
        self.recovery_strategies = [
            "backup_restore",
            "git_recovery",
            "template_creation",
            "pattern_based",
            "manual_guidance"
        ]

        # Component templates and patterns
        self.component_templates = self._load_component_templates()

    def recover_missing_components(
    self,
    validation_results: Dict[str,
    Any]) -> Dict[str, Any]:,
)
        """
        Recover all missing components based on validation results

        Args:
            validation_results: Results from command validator or integrity checker

        Returns:
            Complete recovery operation results
        """
        recovery_results = {
            "timestamp": datetime.now().isoformat(),
            "recovery_session_id": self._generate_session_id(),
            "components_recovered": {},
            "components_failed": {},
            "recovery_summary": {
                "total_missing": 0,
                "total_recovered": 0,
                "total_failed": 0,
                "success_rate": 0
            },
            "strategies_used": set()
        }

        # Identify missing components from validation results
        missing_components = self._identify_missing_components(validation_results)
        recovery_results["recovery_summary"]["total_missing"] = len(missing_components)

        # Attempt recovery for each missing component
        for component in missing_components:
            component_result = self._recover_single_component(component)
            component_id = self._get_component_id(component)

            if component_result["success"]:
                recovery_results["components_recovered"][component_id] = component_result
                recovery_results["recovery_summary"]["total_recovered"] += 1
            else:
                recovery_results["components_failed"][component_id] = component_result
                recovery_results["recovery_summary"]["total_failed"] += 1

            # Track strategies used
            recovery_results["strategies_used"].add(component_result["strategy_used"])

        # Calculate success rate
        total = recovery_results["recovery_summary"]["total_missing"]
        if total > 0:
            recovered = recovery_results["recovery_summary"]["total_recovered"]
            recovery_results["recovery_summary"]["success_rate"] = int((recovered / total) * 100)

        return recovery_results

    def recover_specific_component(
    self,
    component_type: str,
    component_path: str) -> Dict[str, Any]:,
)
        """
        Recover a specific component

        Args:
            component_type: Type of component (command, agent, skill, config)
            component_path: Path or identifier of component

        Returns:
            Recovery results for the specific component
        """
        component = {
            "type": component_type,
            "path": component_path,
            "critical": self._is_critical_component(component_type, component_path)
        }

        return self._recover_single_component(component)

    def create_recovery_plan(
    self,
    missing_components: List[Dict[str,
    Any]]) -> Dict[str, Any]:,
)
        """
        Create a recovery plan without executing it

        Args:
            missing_components: List of missing component information

        Returns:
            Detailed recovery plan with recommended strategies
        """
        recovery_plan = {
            "timestamp": datetime.now().isoformat(),
            "components": {},
            "recommended_actions": [],
            "estimated_time": 0,
            "confidence_score": 0
        }

        total_time = 0
        total_confidence = 0
        component_count = len(missing_components)

        for component in missing_components:
            component_id = self._get_component_id(component)

            # Analyze recovery options
            recovery_options = self._analyze_recovery_options(component)

            # Select best strategy
            best_strategy = self._select_best_recovery_strategy(recovery_options)

            # Estimate time and confidence
            estimated_time = self._estimate_recovery_time(component, best_strategy)
            confidence = self._calculate_recovery_confidence(recovery_options)

            recovery_plan["components"][component_id] = {
                "component": component,
                "recovery_options": recovery_options,
                "recommended_strategy": best_strategy,
                "estimated_time_seconds": estimated_time,
                "confidence_score": confidence,
                "manual_intervention_required": best_strategy == "manual_guidance"
            }

            total_time += estimated_time
            total_confidence += confidence

        # Calculate overall metrics
        if component_count > 0:
            recovery_plan["estimated_time"] = total_time
            recovery_plan["confidence_score"] = int(total_confidence / component_count)

        # Generate recommended actions
        recovery_plan["recommended_actions"] = self._generate_recommended_actions(recovery_plan)

        return recovery_plan

    def _recover_single_component(self, component: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt to recover a single component using all available strategies"""
        recovery_result = {
            "component": component,
            "success": False,
            "strategy_used": None,
            "strategy_results": {},
            "recovered_file": None,
            "backup_used": None,
            "time_taken": 0,
            "error": None
        }

        start_time = datetime.now()

        # Try each recovery strategy in order
        for strategy in self.recovery_strategies:
            try:
                strategy_result = self._execute_recovery_strategy(component, strategy)
                recovery_result["strategy_results"][strategy] = strategy_result

                if strategy_result["success"]:
                    recovery_result["success"] = True
                    recovery_result["strategy_used"] = strategy
                    recovery_result["recovered_file"] = strategy_result.get("recovered_file")
                    recovery_result["backup_used"] = strategy_result.get("backup_id")
                    break

            except Exception as e:
                recovery_result["strategy_results"][strategy] = {
                    "success": False,
                    "error": str(e)
                }

        recovery_result["time_taken"] = (datetime.now() - start_time).total_seconds()

        if not recovery_result["success"]:
            # Try manual guidance as last resort
            manual_guidance = self._generate_manual_guidance(component)
            recovery_result["manual_guidance"] = manual_guidance

        return recovery_result

    def _execute_recovery_strategy(
    self,
    component: Dict[str,
    Any],
    strategy: str) -> Dict[str, Any]:,
)
        """Execute a specific recovery strategy"""
        strategy_result = {
            "strategy": strategy,
            "success": False,
            "details": {},
            "error": None
        }

        try:
            if strategy == "backup_restore":
                return self._recover_from_backup(component)
            elif strategy == "git_recovery":
                return self._recover_from_git(component)
            elif strategy == "template_creation":
                return self._recover_from_template(component)
            elif strategy == "pattern_based":
                return self._recover_from_pattern(component)
            elif strategy == "manual_guidance":
                return self._provide_manual_guidance(component)
            else:
                strategy_result["error"] = f"Unknown recovery strategy: {strategy}"
                return strategy_result

        except Exception as e:
            strategy_result["error"] = str(e)
            return strategy_result

    def _recover_from_backup(self, component: Dict[str, Any]) -> Dict[str, Any]:
        """Recover component from backup"""
        strategy_result = {
            "strategy": "backup_restore",
            "success": False,
            "backup_id": None,
            "recovered_file": None
        }

        # Find the most recent backup containing this component
        backups = self.backup_manager.list_backups()

        for backup in backups:
            backup_id = backup["backup_id"]

            # Check if component exists in this backup
            if self._component_in_backup(component, backup_id):
                try:
                    # Restore from this backup
                    restore_results = self.backup_manager.restore_backup(
                        backup_id,
                        [component["path"]]
                    )

                    if component["path"] in restore_results["restored_files"]:
                        strategy_result["success"] = True
                        strategy_result["backup_id"] = backup_id
                        strategy_result["recovered_file"] = component["path"]
                        break

                except Exception as e:
                    strategy_result["error"] = f"Backup restore failed: {str(e)}"
                    continue

        if not strategy_result["success"] and not strategy_result.get("error"):
            strategy_result["error"] = "Component not found in any backup"

        return strategy_result

    def _recover_from_git(self, component: Dict[str, Any]) -> Dict[str, Any]:
        """Recover component from Git history"""
        strategy_result = {
            "strategy": "git_recovery",
            "success": False,
            "git_commit": None,
            "recovered_file": None
        }

        try:
            # Search Git history for the component
            file_path = component["path"]
            result = subprocess.run(
                ["git", "log", "--all", "--full-history", "--", file_path],
                capture_output=True,
                text=True,
                check=True
            )

            if result.stdout:
                # Extract commit hash
                lines = result.stdout.split('\n')
                commit_line = next((line for line in lines if 
                    line.startswith('commit ')), None)

                if commit_line:
                    commit_hash = commit_line.split()[1]

                    # Try to restore from this commit
                    restore_result = subprocess.run(
                        ["git", "checkout", commit_hash, "--", file_path],
                        capture_output=True,
                        text=True,
                        check=True
                    )

                    if Path(file_path).exists():
                        strategy_result["success"] = True
                        strategy_result["git_commit"] = commit_hash
                        strategy_result["recovered_file"] = file_path
                    else:
                        strategy_result["error"] = "File restore failed after checkout"

            else:
                strategy_result["error"] = "Component not found in Git history"

        except subprocess.CalledProcessError as e:
            strategy_result["error"] = f"Git operation failed: {e.stderr}"
        except Exception as e:
            strategy_result["error"] = f"Git recovery failed: {str(e)}"

        return strategy_result

    def _recover_from_template(self, component: Dict[str, Any]) -> Dict[str, Any]:
        """Recover component from template"""
        strategy_result = {
            "strategy": "template_creation",
            "success": False,
            "template_used": None,
            "recovered_file": None
        }

        template_info = self._find_component_template(component)

        if not template_info:
            strategy_result["error"] = "No template found for this component type"
            return strategy_result

        try:
            # Load and customize template
            template_content = self._load_and_customize_template(component, template_info)

            # Create component file
            component_path = Path(component["path"])
            component_path.parent.mkdir(parents=True, exist_ok=True)

            with open(component_path, 'w', encoding='utf-8') as f:
                f.write(template_content)

            strategy_result["success"] = True
            strategy_result["template_used"] = template_info["template_path"]
            strategy_result["recovered_file"] = component["path"]

        except Exception as e:
            strategy_result["error"] = f"Template creation failed: {str(e)}"

        return strategy_result

    def _recover_from_pattern(self, component: Dict[str, Any]) -> Dict[str, Any]:
        """Recover component based on existing patterns"""
        strategy_result = {
            "strategy": "pattern_based",
            "success": False,
            "reference_component": None,
            "recovered_file": None
        }

        # Find similar existing components
        reference = self._find_similar_component(component)

        if not reference:
            strategy_result["error"] = "No similar component found for pattern-based recovery"
            return strategy_result

        try:
            # Use reference component as template
            component_path = Path(component["path"])
            reference_path = Path(reference["path"])

            # Read reference component
            with open(reference_path, 'r', encoding='utf-8') as f:
                reference_content = f.read()

            # Customize based on component
            customized_content = self._customize_content_from_reference(
                reference_content, component, reference
            )

            # Create component file
            component_path.parent.mkdir(parents=True, exist_ok=True)

            with open(component_path, 'w', encoding='utf-8') as f:
                f.write(customized_content)

            strategy_result["success"] = True
            strategy_result["reference_component"] = reference["path"]
            strategy_result["recovered_file"] = component["path"]

        except Exception as e:
            strategy_result["error"] = f"Pattern-based recovery failed: {str(e)}"

        return strategy_result

    def _provide_manual_guidance(self, component: Dict[str, Any]) -> Dict[str, Any]:
        """Provide manual guidance for component recovery"""
        strategy_result = {
            "strategy": "manual_guidance",
            "success": False,
            "guidance": {},
            "steps": []
        }

        guidance = self._generate_manual_guidance(component)
        strategy_result["guidance"] = guidance
        strategy_result["steps"] = guidance.get("steps", [])

        return strategy_result

    def _identify_missing_components(
    self,
    validation_results: Dict[str,
    Any]) -> List[Dict[str, Any]]:,
)
        """Identify missing components from validation results"""
        missing_components = []

        # Check for missing commands
        if "missing_commands" in validation_results:
            for missing_cmd in validation_results["missing_commands"]:
                component = {
                    "type": "command",
                    "path": f"commands{missing_cmd['command'].replace(':', '/')}.md",
                    "critical": missing_cmd.get("severity") == "critical",
                    "category": missing_cmd.get("category"),
                    "name": missing_cmd["command"].split(
    ":")[1] if ":" in missing_cmd["command"] else missing_cmd["command"],
)
                }
                missing_components.append(component)

        # Check for syntax errors that indicate broken files
        if "syntax_errors" in validation_results:
            for error in validation_results["syntax_errors"]:
                if "error" in str(
    error).lower() and ("not found" in str(error) or "missing" in str(error)):,
)
                    component = {
                        "type": "file",
                        "path": error["file"],
                        "critical": error.get("severity") == "critical",
                        "name": Path(error["file"]).name
                    }
                    missing_components.append(component)

        return missing_components

    def _find_component_template(
    self,
    component: Dict[str,
    Any]) -> Optional[Dict[str, Any]]:,
)
        """Find template for component type"""
        component_type = component["type"]

        if component_type in self.component_templates:
            return self.component_templates[component_type]

        return None

    def _load_and_customize_template(
    self,
    component: Dict[str,
    Any],
    template_info: Dict[str,
    Any]) -> str:,
)
        """Load and customize template content"""
        template_path = Path(template_info["template_path"])

        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()

        # Customize template
        customizations = template_info.get("customizations", {})
        for placeholder, value in customizations.items():
            template_content = template_content.replace(placeholder, str(value))

        return template_content

    def _find_similar_component(
    self,
    component: Dict[str,
    Any]) -> Optional[Dict[str, Any]]:,
)
        """Find similar existing component"""
        component_type = component["type"]

        if component_type == "command":
            # Find similar commands in same category
            category = component.get("category")
            if category:
                category_path = self.plugin_dir / "commands" / category
                if category_path.exists():
                    similar_files = []
                    for cmd_file in category_path.glob("*.md"):
                        if cmd_file.stem != component.get("name", ""):
                            similar_files.append({
                                "path": str(cmd_file),
                                "name": cmd_file.stem,
                                "similarity": self._calculate_similarity(
                                    component.get("name", ""), cmd_file.stem
                                )
                            })

                    if similar_files:
                        # Return most similar
                        similar_files.sort(key=lambda x: x["similarity"], reverse=True)
                        return similar_files[0]

        return None

    def _customize_content_from_reference(
    self,
    content: str,
    target: Dict[str,
    Any],
    reference: Dict[str,
    Any]) -> str:,
)
        """Customize content from reference component"""
        # Basic content customization
        customized = content

        # Replace references to component name
        ref_name = reference.get("name", "")
        target_name = target.get("name", "")

        if ref_name and target_name:
            # Simple string replacements
            customized = customized.replace(ref_name, target_name)

            # Replace frontmatter fields
            frontmatter_pattern = r'(^---\s*\n.*?name:\s*)(\w+)(.*?\n---)'
            customized = re.sub(
                frontmatter_pattern,
                lambda m: f"{m.group(1)}{target_name}{m.group(3)}",
                customized,
                flags=re.DOTALL
            )

        # Replace category references
        target_category = target.get("category")
        if target_category:
            ref_category = reference.get("category")
            if ref_category:
                customized = customized.replace(f"/{ref_category}:", f"/{target_category}:")

        return customized

    def _generate_manual_guidance(self, component: Dict[str, Any]) -> Dict[str, Any]:
        """Generate manual guidance for component recovery"""
        component_type = component["type"]
        component_path = component["path"]

        guidance = {
            "component": component,
            "steps": [],
            "reference_materials": [],
            "estimated_difficulty": "medium",
            "estimated_time": "10-30 minutes"
        }

        if component_type == "command":
            guidance["steps"] = [
                f"1. Create file: {component_path}",
                f"2. Add YAML frontmatter with name, description, usage, category: {component.get(
    'category')}",,
)
                "3. Add command description and usage examples",
                "4. Include parameter documentation if applicable",
                "5. Test command discoverability: run validation check"
            ]
            guidance["reference_materials"] = [
                "commands/dev/auto.md (example command)",
                "docs/templates/command_template.md (if available)",
                "Plugin development guidelines"
            ]

        elif component_type == "agent":
            guidance["steps"] = [
                f"1. Create file: {component_path}",
                "2. Add YAML frontmatter with name, description, tools, model",
                "3. Write agent responsibilities and skills integration",
                "4. Define approach and handoff protocol",
                "5. Validate agent integration"
            ]

        guidance["estimated_difficulty"] = "high" if 
            component.get("critical") else "medium"

        return guidance

    def _load_component_templates(self) -> Dict[str, Any]:
        """Load component templates"""
        templates = {
            "command": {
                "template_path": "templates/command_template.md",
                "customizations": {
                    "{{CATEGORY}}": "unknown",
                    "{{NAME}}": "unknown",
                    "{{DESCRIPTION}}": "Command description",
                    "{{USAGE}}": "/category:name"
                }
            },
            "agent": {
                "template_path": "templates/agent_template.md",
                "customizations": {
                    "{{NAME}}": "agent-name",
                    "{{DESCRIPTION}}": "Agent description"
                }
            }
        }

        # Check if templates exist in different locations
        template_locations = [
            "templates/",
            "docs/templates/",
            ".claude/templates/"
        ]

        for location in template_locations:
            location_path = Path(location)
            if location_path.exists():
                # Update template paths
                for template_type, template_info in templates.items():
                    template_file = location_path / Path(template_info["template_path"]).name
                    if template_file.exists():
                        template_info["template_path"] = str(template_file)

        return templates

    def _component_in_backup(self, component: Dict[str, Any], backup_id: str) -> bool:
        """Check if component exists in specific backup"""
        backup_path = self.backup_manager.backup_dir / backup_id
        manifest_path = backup_path / "backup_manifest.json"

        if not manifest_path.exists():
            return False

        try:
            with open(manifest_path, 'r') as f:
                backup_manifest = json.load(f)

            component_path = component["path"]

            # Search through all categories
            for category_files in backup_manifest.get("files_backed_up", {}).values():
                if component_path in category_files:
                    return True

            return False

        except:
            return False

    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings"""
        import difflib
        return difflib.SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

    def _is_critical_component(self, component_type: str, component_path: str) -> bool:
        """Determine if component is critical"""
        critical_patterns = [
            "commands/dev/",
            "commands/analyze/",
            "commands/validate/",
            "agents/orchestrator.md",
            ".claude-plugin/plugin.json"
        ]

        for pattern in critical_patterns:
            if pattern in component_path:
                return True

        return False

    def _get_component_id(self, component: Dict[str, Any]) -> str:
        """Generate unique component identifier"""
        return f"{component['type']}:{component['path']}"

    def _generate_session_id(self) -> str:
        """Generate recovery session ID"""
        return f"recovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def _analyze_recovery_options(
    self,
    component: Dict[str,
    Any]) -> List[Dict[str, Any]]:,
)
        """Analyze available recovery options for component"""
        options = []

        # Check backup availability
        if self._check_backup_availability(component):
            options.append({
                "strategy": "backup_restore",
                "available": True,
                "confidence": 0.95,
                "estimated_time": 5
            })

        # Check Git availability
        if self._check_git_availability(component):
            options.append({
                "strategy": "git_recovery",
                "available": True,
                "confidence": 0.85,
                "estimated_time": 10
            })

        # Check template availability
        if self._check_template_availability(component):
            options.append({
                "strategy": "template_creation",
                "available": True,
                "confidence": 0.70,
                "estimated_time": 15
            })

        # Check pattern availability
        if self._check_pattern_availability(component):
            options.append({
                "strategy": "pattern_based",
                "available": True,
                "confidence": 0.60,
                "estimated_time": 20
            })

        # Manual guidance is always available
        options.append({
            "strategy": "manual_guidance",
            "available": True,
            "confidence": 0.30,
            "estimated_time": 30
        })

        return options

    def _select_best_recovery_strategy(
    self,
    recovery_options: List[Dict[str,
    Any]]) -> str:,
)
        """Select best recovery strategy based on confidence and time"""
        available_options = [opt for opt in recovery_options if opt["available"]]

        if not available_options:
            return "manual_guidance"

        # Sort by confidence (descending), then by time (ascending)
        available_options.sort(key=lambda x: (-x["confidence"], x["estimated_time"]))

        return available_options[0]["strategy"]

    def _estimate_recovery_time(self, component: Dict[str, Any], strategy: str) -> int:
        """Estimate recovery time in seconds"""
        base_times = {
            "backup_restore": 5,
            "git_recovery": 10,
            "template_creation": 15,
            "pattern_based": 20,
            "manual_guidance": 30
        }

        # Adjust for component complexity
        complexity_factor = 1.0
        if component.get("critical"):
            complexity_factor = 1.2
        if component["type"] == "command":
            complexity_factor *= 1.1

        return int(base_times.get(strategy, 30) * complexity_factor)

    def _calculate_recovery_confidence(
    self,
    recovery_options: List[Dict[str,
    Any]]) -> int:,
)
        """Calculate overall recovery confidence score"""
        available_options = [opt for opt in recovery_options if opt["available"]]

        if not available_options:
            return 0

        # Weight the options
        weights = {
            "backup_restore": 0.4,
            "git_recovery": 0.3,
            "template_creation": 0.15,
            "pattern_based": 0.1,
            "manual_guidance": 0.05
        }

        total_confidence = 0
        for option in available_options:
            strategy = option["strategy"]
            confidence = option["confidence"]
            weight = weights.get(strategy, 0.05)
            total_confidence += confidence * weight

        return int(total_confidence * 100)

    def _generate_recommended_actions(self, recovery_plan: Dict[str, Any]) -> List[str]:
        """Generate recommended recovery actions"""
        actions = []

        components = recovery_plan["components"]
        confidence = recovery_plan["confidence_score"]
        estimated_time = recovery_plan["estimated_time"]

        if confidence > 80:
            actions.append(
    f"[HIGH] Automatic recovery recommended ({confidence}% confidence)",
)
            actions.append(f"Estimated time: {estimated_time} seconds")
        elif confidence > 50:
            actions.append(
    f"[MED] Recovery with manual intervention likely ({confidence}% confidence)",
)
            actions.append(
    f"Estimated time: {estimated_time} seconds (may require additional work)",
)
        else:
            actions.append(
    f"[LOW] Manual recreation recommended ({confidence}% confidence)",
)
            actions.append("Focus on components with highest recovery potential first")

        # Check for components requiring manual intervention
        manual_components = [
            comp_id for comp_id, comp_info in components.items()
            if comp_info.get("manual_intervention_required")
        ]

        if manual_components:
            actions.append(
    f"[ATTENTION] {len(manual_components)} components require manual intervention",
)

        # Critical components priority
        critical_components = [
            comp_id for comp_id, comp_info in components.items()
            if comp_info.get("component", {}).get("critical")
        ]

        if critical_components:
            actions.append(
    f"[PRIORITY] Recover {len(critical_components)} critical components first",
)

        return actions

    def _check_backup_availability(self, component: Dict[str, Any]) -> bool:
        """Check if component is available in backups"""
        backups = self.backup_manager.list_backups()
        return len(backups) > 0

    def _check_git_availability(self, component: Dict[str, Any]) -> bool:
        """Check if component is available in Git"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True,
                check=True
            )
            return True
        except:
            return False

    def _check_template_availability(self, component: Dict[str, Any]) -> bool:
        """Check if template is available for component"""
        template_info = self._find_component_template(component)
        return template_info is not None and Path(
    template_info["template_path"]).exists(,
)

    def _check_pattern_availability(self, component: Dict[str, Any]) -> bool:
        """Check if pattern-based recovery is possible"""
        similar = self._find_similar_component(component)
        return similar is not None


def main():
    """CLI interface for recovery manager"""
    import argparse

    parser = argparse.ArgumentParser(description="Recovery Manager for Missing Components")
    parser.add_argument("action", choices=["recover", "plan", "single"])
    parser.add_argument("--plugin-dir", default=".", help="Plugin directory")
    parser.add_argument("--component-type", choices=["command", "agent", "skill", "config"],
                       help="Type of component to recover")
    parser.add_argument("--component-path", help="Path or identifier of component")
    parser.add_argument("--validation-file", help="Validation results file")

    args = parser.parse_args()

    recovery_manager = RecoveryManager(args.plugin_dir)

    if args.action == "recover":
        if not args.validation_file:
            print("❌ --validation-file required for recovery")
            sys.exit(1)

        with open(args.validation_file, 'r') as f:
            validation_results = json.load(f)

        results = recovery_manager.recover_missing_components(validation_results)

        print(f"🔄 Recovery Session: {results['recovery_session_id']}")
        print(
    f"📊 Summary: {results['recovery_summary']['total_recovered']}/{results['recovery_summary']['total_missing']} recovered",
)
        print(f"✅ Success Rate: {results['recovery_summary']['success_rate']}%")
        print(
    f"⏱ Time Taken: {sum(
    r['time_taken'] for r in results['components_recovered'].values()):.2f}s",,
)
)

        if results['components_failed']:
            print(f"\n❌ Failed Recoveries ({len(results['components_failed'])}):")
            for comp_id, failure in results['components_failed'].items():
                print(f"  {comp_id}: {failure.get('error', 'Unknown error')}")

    elif args.action == "plan":
        if not args.validation_file:
            print("❌ --validation-file required for recovery plan")
            sys.exit(1)

        with open(args.validation_file, 'r') as f:
            validation_results = json.load(f)

        # Identify missing components (simplified for demo)
        missing_components = []  # Would be extracted from validation_results

        plan = recovery_manager.create_recovery_plan(missing_components)

        print(f"📋 Recovery Plan")
        print(f"⏱ Estimated Time: {plan['estimated_time']} seconds")
        print(f"🎯 Confidence: {plan['confidence_score']}%")

        if plan['recommended_actions']:
            print(f"\n💡 Recommended Actions:")
            for action in plan['recommended_actions']:
                print(f"  {action}")

    elif args.action == "single":
        if not args.component_type or not args.component_path:
            print(
    "❌ --component-type and --component-path required for single recovery",
)
            sys.exit(1)

        result = recovery_manager.recover_specific_component(
            args.component_type, args.component_path
        )

        print(f"🔧 Component Recovery: {args.component_type}:{args.component_path}")
        print(f"Success: {'✅' if result['success'] else '❌'}")
        if result['success']:
            print(f"Strategy: {result['strategy_used']}")
            print(f"File: {result['recovered_file']}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
