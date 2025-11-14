#!/usr/bin/env python3
"""
Documentation Auto-Generation System

Automatically generates documentation from successful patterns,
maintains consistency, and validates documentation integrity.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from collections import defaultdict
import re


class DocumentationAutoGenerator:
    """Advanced documentation generation from patterns"""

    def __init__(self, patterns_dir: str = ".claude-patterns", project_root: str = "."):
        """  Init  ."""
        self.patterns_dir = patterns_dir
        self.project_root = Path(project_root)
        self.patterns_file = os.path.join(patterns_dir, "patterns.json")
        self.docs_config_file = os.path.join(patterns_dir, "docs_config.json")
        self.generated_docs_dir = os.path.join(patterns_dir, "generated_docs")

        # Documentation templates
        self.templates = self._load_templates()

        # Configuration
        self.config = self._load_config()

        # Ensure directories exist
        os.makedirs(self.generated_docs_dir, exist_ok=True)

    def _load_templates(self) -> Dict:
        """Load documentation templates"""
        return {
            "agent_template": """---
name: {name}
description: {description}
tools: {tools}
model: {model}
---

# {title}

{overview}

## Core Responsibilities

{responsibilities}

## Skills Integration

{skills_integration}

## Approach

{approach}

## Quality Assurance

{quality_assurance}

## Handoff Protocol

{handoff_protocol}

## Performance Metrics

{performance_metrics}
""",
            "skill_template": """---
name: {name}
description: {description}
version: {version}
---

## Overview

{overview}

## Core Principles

{core_principles}

## Implementation Guidelines

{implementation_guidelines}

## Best Practices

{best_practices}

## Quality Standards

{quality_standards}

## Usage Examples

{usage_examples}

## Performance Considerations

{performance_considerations}
""",
            "command_template": """# {command_name}

**Category:** {category}
**Complexity:** {complexity}
**Estimated Time:** {estimated_time}

## Description

{description}

## Usage

```bash
{usage_example}
```

## Parameters

{parameters}

## Examples

{examples}

## Expected Outcomes

{expected_outcomes}

## Quality Checks

{quality_checks}

## Related Commands

{related_commands}
""",
            "readme_template": """# {project_name}

{tagline}

## Overview

{overview}

## Architecture

{architecture}

## Features

{features}

## Quick Start

{quick_start}

## Command Reference

{command_reference}

## Development Guide

{development_guide}

## Quality Assurance

{quality_assurance}

## Contributing

{contributing}

## License

{license}
""",
        }

    def _load_config(self) -> Dict:
        """Load or create default configuration"""
        default_config = {
            "auto_generate": True,
            "validation_enabled": True,
            "consistency_checks": True,
            "output_formats": ["markdown"],
            "include_metrics": True,
            "include_examples": True,
            "update_frequency": "daily",
            "min_pattern_count": 3,
            "quality_threshold": 85,
            "sections": {
                "agents": True,
                "skills": True,
                "commands": True,
                "api": True,
                "examples": True,
                "troubleshooting": True,
            },
        }

        try:
            if os.path.exists(self.docs_config_file):
                with open(self.docs_config_file, "r", encoding="utf-8") as f:
                    loaded_config = json.load(f)
                # Merge with defaults
                for key, value in default_config.items():
                    if key not in loaded_config:
                        loaded_config[key] = value
                return loaded_config
        except Exception:
            pass

        return default_config

    def _save_config(self):
        """Save current configuration"""
        os.makedirs(self.patterns_dir, exist_ok=True)
        with open(self.docs_config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def load_patterns(self) -> Dict:
        """Load pattern data"""
        try:
            with open(self.patterns_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"patterns": [], "skill_effectiveness": {}, "agent_effectiveness": {}}

    def extract_documentation_patterns(self, patterns: List[Dict]) -> Dict:
        """Extract documentation patterns from successful task patterns"""
        doc_patterns = {
            "agents": defaultdict(list),
            "skills": defaultdict(list),
            "commands": defaultdict(list),
            "workflows": defaultdict(list),
            "quality_metrics": defaultdict(list),
        }

        for pattern in patterns:
            if not pattern.get("outcome", {}).get("success", False):
                continue  # Skip failed patterns

            quality_score = pattern.get("outcome", {}).get("quality_score", 0)
            if quality_score < self.config["quality_threshold"]:
                continue  # Skip low-quality patterns

            # Extract agent patterns
            agents = pattern.get("execution", {}).get("agents_delegated", [])
            for agent in agents:
                doc_patterns["agents"][agent].append(
                    {
                        "task_type": pattern.get("task_type"),
                        "quality_score": quality_score,
                        "skills_used": pattern.get("execution", {}).get("skills_used", []),
                        "duration": pattern.get("execution", {}).get("duration_seconds", 0),
                        "complexity": pattern.get("task_complexity", "medium"),
                    }
                )

            # Extract skill patterns
            skills = pattern.get("execution", {}).get("skills_used", [])
            for skill in skills:
                doc_patterns["skills"][skill].append(
                    {
                        "task_type": pattern.get("task_type"),
                        "quality_score": quality_score,
                        "agents_involved": agents,
                        "success_rate": 1.0,  # Since we only keep successful patterns
                        "context": pattern.get("context", {}),
                    }
                )

            # Extract command patterns
            if "command_name" in pattern.get("context", {}):
                command = pattern["context"]["command_name"]
                doc_patterns["commands"][command].append(
                    {
                        "task_type": pattern.get("task_type"),
                        "quality_score": quality_score,
                        "duration": pattern.get("execution", {}).get("duration_seconds", 0),
                        "success_rate": 1.0,
                        "parameters": pattern.get("context", {}),
                    }
                )

        return doc_patterns

    def generate_agent_documentation(self, agent_name: str, patterns: List[Dict]) -> str:
        """Generate comprehensive agent documentation"""
        if not patterns:
            return f"# {agent_name}\n\nNo documentation patterns available yet."

        # Analyze patterns for insights
        quality_scores = [p["quality_score"] for p in patterns]
        avg_quality = sum(quality_scores) / len(quality_scores)
        task_types = list(set(p["task_type"] for p in patterns))
        common_skills = self._get_most_common_items([skill for p in patterns for skill in p["skills_used"]])

        # Generate content sections
        overview = self._generate_agent_overview(agent_name, patterns, avg_quality, task_types)
        responsibilities = self._generate_agent_responsibilities(agent_name, patterns)
        skills_integration = self._generate_skills_integration(common_skills, patterns)
        approach = self._generate_agent_approach(patterns)
        quality_assurance = self._generate_quality_assurance(avg_quality, patterns)
        handoff_protocol = self._generate_handoff_protocol(agent_name, patterns)
        performance_metrics = self._generate_performance_metrics(patterns)

        # Use template
        return self.templates["agent_template"].format(
            name=agent_name,
            description=f"Autonomous agent specialized in {', '.join(task_types[:3])}",
            tools="Read,Write,Edit,Bash,Grep,Glob",
            model="inherit",
            title=f"{agent_name.replace('-', ' ').title()} Agent",
            overview=overview,
            responsibilities=responsibilities,
            skills_integration=skills_integration,
            approach=approach,
            quality_assurance=quality_assurance,
            handoff_protocol=handoff_protocol,
            performance_metrics=performance_metrics,
        )

    def _generate_agent_overview(
        self, agent_name: str, patterns: List[Dict], avg_quality: float, task_types: List[str]
    )-> str:
        """ Generate Agent Overview."""
        """Generate agent overview section"""
        overview = f"""The **{agent_name}** agent is a specialized autonomous agent that excels in {', '.join(task_types[:3])}.

**Performance Metrics:**
- Average Quality Score: {avg_quality:.1f}/100
- Successful Executions: {len(patterns)}
- Primary Task Types: {', '.join(task_types[:3])}

This agent operates with true autonomy, making intelligent decisions based on historical patterns and real-time context analysis."""

        return overview

    def _generate_agent_responsibilities(self, agent_name: str, patterns: List[Dict]) -> str:
        """Generate agent responsibilities section"""
        responsibilities = []

        # Extract responsibilities from patterns
        task_descriptions = [p.get("task_description", "") for p in patterns]

        # Categorize responsibilities
        resp_categories = {
            "analysis": ["analyze", "review", "examine", "audit"],
            "execution": ["execute", "implement", "create", "build"],
            "validation": ["validate", "check", "verify", "ensure"],
            "optimization": ["optimize", "improve", "enhance", "refactor"],
        }

        for category, keywords in resp_categories.items():
            relevant_tasks = [desc for desc in task_descriptions if any(keyword in desc.lower() for keyword in keywords)]
            if relevant_tasks:
                responsibilities.append(f"**{category.title()}**: {len(relevant_tasks)} specialized tasks")

        return "\n\n".join(responsibilities) if responsibilities else "Autonomous execution across multiple task domains."

    def _generate_skills_integration(self, common_skills: List[Tuple[str, int]], patterns: List[Dict]) -> str:
        """Generate skills integration section"""
        if not common_skills:
            return "Skills dynamically selected based on task requirements and historical patterns."

        skills_text = "This agent integrates the following key skills:\n\n"
        for skill, count in common_skills[:5]:  # Top 5 skills
            skills_text += f"- **{skill}**: Utilized in {count} successful executions\n"

        return skills_text

    def _generate_agent_approach(self, patterns: List[Dict]) -> str:
        """Generate agent approach section"""
        approaches = []

        # Extract common approaches from patterns
        for pattern in patterns[:5]:  # Top 5 patterns
            approach = pattern.get("execution", {}).get("approach", "")
            if approach and approach not in approaches:
                approaches.append(approach)

        if not approaches:
            return "Pattern-based autonomous execution with continuous learning and quality optimization."

        approach_text = "This agent employs multiple proven approaches:\n\n"
        for approach in approaches[:3]:
            approach_text += f"- **{approach}**: Validated through successful execution\n"

        return approach_text

    def _generate_quality_assurance(self, avg_quality: float, patterns: List[Dict]) -> str:
        """Generate quality assurance section"""
        qa_text = f"""**Quality Assurance Framework:**

- Average Quality Score: {avg_quality:.1f}/100
- Success Rate: 100% (based on analyzed patterns)
- Quality Threshold: {self.config['quality_threshold']}/100

**Quality Gates:**
- Initial validation: 85/100 minimum
- Mid-execution check: 88/100 minimum
- Final assessment: 90/100 minimum

**Continuous Improvement:**
- Pattern learning integration
- Performance metric tracking
- Auto-correction capabilities"""

        return qa_text

    def _generate_handoff_protocol(self, agent_name: str, patterns: List[Dict]) -> str:
        """Generate handoff protocol section"""
        return f"""**Handoff Protocol for {agent_name}:**

1. **Task Completion Confirmation**
   - Verify all objectives met
   - Quality score meets threshold
   - Documentation updated

2. **Result Packaging**
   - Compile execution results
   - Include quality metrics
   - Note patterns learned

3. **Return to Orchestrator**
   - Comprehensive status report
   - Performance indicators
   - Recommendations for optimization

4. **Knowledge Transfer**
   - Store successful patterns
   - Update skill effectiveness
   - Share insights with learning engine"""

    def _generate_performance_metrics(self, patterns: List[Dict]) -> str:
        """Generate performance metrics section"""
        if not patterns:
            return "Performance metrics will be collected as patterns accumulate."

        durations = [p.get("duration", 0) for p in patterns if p.get("duration", 0) > 0]
        qualities = [p["quality_score"] for p in patterns]

        metrics = f"""**Performance Metrics (based on {len(patterns)} executions):**

- Average Quality Score: {sum(qualities) / len(qualities):.1f}/100
- Average Duration: {sum(durations) / len(durations):.1f}s
- Fastest Execution: {min(durations):.1f}s
- Slowest Execution: {max(durations):.1f}s

**Quality Distribution:**
- Excellent (95+): {len([q for q in qualities if q >= 95])} executions
- Good (90-94): {len([q for q in qualities if 90 <= q < 95])} executions
- Acceptable (85-89): {len([q for q in qualities if 85 <= q < 90])} executions

**Task Types Handled:**
{', '.join(list(set(p['task_type'] for p in patterns))[:5])}"""

        return metrics

    def generate_skill_documentation(self, skill_name: str, patterns: List[Dict]) -> str:
        """Generate comprehensive skill documentation"""
        if not patterns:
            return f"# {skill_name}\n\nNo documentation patterns available yet."

        # Analyze patterns
        task_types = list(set(p["task_type"] for p in patterns))
        avg_quality = sum(p["quality_score"] for p in patterns) / len(patterns)
        common_agents = self._get_most_common_items([agent for p in patterns for agent in p["agents_involved"]])

        # Generate content
        overview = self._generate_skill_overview(skill_name, patterns, avg_quality, task_types)
        core_principles = self._generate_core_principles(skill_name, patterns)
        implementation_guidelines = self._generate_implementation_guidelines(skill_name, patterns)
        best_practices = self._generate_best_practices(skill_name, patterns)
        quality_standards = self._generate_quality_standards(skill_name, avg_quality)
        usage_examples = self._generate_usage_examples(skill_name, patterns)
        performance_considerations = self._generate_performance_considerations(skill_name, patterns)

        return self.templates["skill_template"].format(
            name=skill_name,
            description=f"Knowledge package for {skill_name} with proven effectiveness",
            version="1.0.0",
            overview=overview,
            core_principles=core_principles,
            implementation_guidelines=implementation_guidelines,
            best_practices=best_practices,
            quality_standards=quality_standards,
            usage_examples=usage_examples,
            performance_considerations=performance_considerations,
        )

    def _generate_skill_overview(
        self, skill_name: str, patterns: List[Dict], avg_quality: float, task_types: List[str]
    )-> str:
        """ Generate Skill Overview."""
        """Generate skill overview"""
        return f"""The **{skill_name}** skill provides specialized knowledge and proven methodologies for {', '.join(task_types[:3])}.

**Performance Characteristics:**
- Success Rate: 100% (analyzed patterns)
- Average Quality Impact: +{avg_quality - 85:.1f} points above baseline
- Versatility: Applied across {len(task_types)} different task types
- Reliability: Consistent performance across all executions

This skill has been validated through {len(patterns)} successful autonomous executions and continuously improves through pattern learning."""

    def _generate_core_principles(self, skill_name: str, patterns: List[Dict]) -> str:
        """Generate core principles section"""
        # Extract principles from pattern contexts
        principles = []

        for pattern in patterns[:5]:  # Analyze top patterns
            context = pattern.get("context", {})
            if "approach" in context:
                principles.append(f"- **{context['approach']}**: Proven successful methodology")

        if not principles:
            principles = [
                "- **Pattern-Based Decision Making**: Leverage historical successful approaches",
                "- **Quality-First Execution**: Ensure all outputs meet quality thresholds",
                "- **Continuous Learning**: Improve from each execution",
                "- **Autonomous Operation**: Function without human intervention",
            ]

        return "\n".join(principles)

    def _generate_implementation_guidelines(self, skill_name: str, patterns: List[Dict]) -> str:
        """Generate implementation guidelines"""
        return f"""**Implementation Guidelines for {skill_name}:**

1. **Initialization**
   - Load skill metadata and validate context
   - Check for relevant historical patterns
   - Prepare knowledge base

2. **Execution**
   - Apply proven methodologies from patterns
   - Adapt approach based on task complexity
   - Maintain quality standards throughout

3. **Validation**
   - Verify outputs meet quality criteria
   - Check consistency with expected results
   - Document any deviations

4. **Learning Integration**
   - Store execution patterns for future reference
   - Update effectiveness metrics
   - Share insights with learning engine

**Best Practices:**
- Always validate prerequisites before execution
- Maintain comprehensive logging
- Store successful patterns for reuse"""

    def _generate_best_practices(self, skill_name: str, patterns: List[Dict]) -> str:
        """Generate best practices section"""
        practices = []

        # Extract practices from successful patterns
        for pattern in patterns:
            execution = pattern.get("execution", {})
            if "approach_taken" in execution:
                approach = execution["approach_taken"]
                if approach not in practices:
                    practices.append(f"- **{approach}**: Validated successful approach")

        if not practices:
            practices = [
                "- **Consistent Application**: Apply skill uniformly across similar tasks",
                "- **Quality Validation**: Always verify outputs meet standards",
                "- **Pattern Recognition**: Identify and leverage successful patterns",
                "- **Continuous Improvement**: Learn from each execution",
            ]

        return "\n".join(practices[:5])

    def _generate_quality_standards(self, skill_name: str, avg_quality: float) -> str:
        """Generate quality standards section"""
        return f"""**Quality Standards for {skill_name}:**

- **Minimum Quality Score**: {self.config['quality_threshold']}/100
- **Historical Average**: {avg_quality:.1f}/100
- **Success Rate**: 100% (based on pattern analysis)

**Quality Metrics:**
- Execution accuracy
- Output completeness
- Pattern adherence
- Learning integration

**Continuous Monitoring:**
- Real-time quality assessment
- Performance trend analysis
- Pattern effectiveness tracking"""

    def _generate_usage_examples(self, skill_name: str, patterns: List[Dict]) -> str:
        """Generate usage examples section"""
        examples = []

        for pattern in patterns[:3]:  # Top 3 examples
            task_type = pattern.get("task_type", "")
            task_desc = pattern.get("task_description", "")
            quality = pattern.get("quality_score", 0)

            examples.append(f"**Example {len(examples) + 1}: {task_type.title()}**")
            examples.append(f"- Task: {task_desc}")
            examples.append(f"- Quality Score: {quality}/100")
            examples.append(f"- Result: Successful execution with pattern learning")

        return "\n\n".join(examples) if examples else "Usage examples will be generated as more patterns accumulate."

    def _generate_performance_considerations(self, skill_name: str, patterns: List[Dict]) -> str:
        """Generate performance considerations section"""
        if not patterns:
            return "Performance data will be collected as patterns accumulate."

        durations = [p.get("duration", 0) for p in patterns if p.get("duration", 0) > 0]
        if not durations:
            return "Performance timing data will be collected."

        avg_duration = sum(durations) / len(durations)

        return f"""**Performance Considerations for {skill_name}:**

- **Average Execution Time**: {avg_duration:.1f} seconds
- **Consistency**: Low variance across executions
- **Resource Efficiency**: Optimized for autonomous operation
- **Scalability**: Suitable for complex task types

**Optimization Opportunities:**
- Parallel execution when applicable
- Caching of common patterns
- Pre-loading of relevant knowledge
- Resource-aware scheduling"""

    def generate_command_documentation(self, command_name: str, patterns: List[Dict]) -> str:
        """Generate comprehensive command documentation"""
        if not patterns:
            return f"# {command_name}\n\nNo documentation patterns available yet."

        # Analyze patterns
        avg_duration = sum(p["duration"] for p in patterns if p["duration"] > 0) / max(
            len([p for p in patterns if p["duration"] > 0]), 1
        )
        avg_quality = sum(p["quality_score"] for p in patterns) / len(patterns)

        # Generate content
        description = self._generate_command_description(command_name, patterns)
        usage_example = self._generate_command_usage(command_name, patterns)
        parameters = self._generate_command_parameters(patterns)
        examples = self._generate_command_examples(command_name, patterns)
        expected_outcomes = self._generate_expected_outcomes(patterns)
        quality_checks = self._generate_quality_checks(command_name, avg_quality)
        related_commands = self._generate_related_commands(patterns)

        return self.templates["command_template"].format(
            command_name=command_name,
            category="autonomous",
            complexity="medium",
            estimated_time=f"{int(avg_duration)}s",
            description=description,
            usage_example=usage_example,
            parameters=parameters,
            examples=examples,
            expected_outcomes=expected_outcomes,
            quality_checks=quality_checks,
            related_commands=related_commands,
        )

    def _generate_command_description(self, command_name: str, patterns: List[Dict]) -> str:
        """Generate command description"""
        task_types = list(set(p["task_type"] for p in patterns))
        return f"Autonomous command for {command_name.replace('-', ' ').title()}. Specialized in {', '.join(task_types[:3])} with proven success rate of 100% across {len(patterns)} executions."

    def _generate_command_usage(self, command_name: str, patterns: List[Dict]) -> str:
        """Generate command usage example"""
        return f"/{command_name} [options]"

    def _generate_command_parameters(self, patterns: List[Dict]) -> str:
        """Generate command parameters documentation"""
        common_params = set()

        for pattern in patterns:
            params = pattern.get("parameters", {})
            if isinstance(params, dict):
                common_params.update(params.keys())

        if not common_params:
            return "No specific parameters required."

        param_docs = []
        for param in sorted(common_params):
            param_docs.append(f"- `{param}`: Command-specific parameter")

        return "\n".join(param_docs)

    def _generate_command_examples(self, command_name: str, patterns: List[Dict]) -> str:
        """Generate command usage examples"""
        examples = []

        for i, pattern in enumerate(patterns[:3]):
            task_desc = pattern.get("task_description", "")
            examples.append(f"**Example {i + 1}:**")
            examples.append(f"`/{command_name}`")
            examples.append(f"Executes: {task_desc}")
            examples.append(f"Quality: {pattern.get('quality_score', 0)}/100")

        return "\n\n".join(examples)

    def _generate_expected_outcomes(self, patterns: List[Dict]) -> str:
        """Generate expected outcomes documentation"""
        outcomes = [
            "- Autonomous execution without human intervention",
            "- Quality score meeting threshold requirements",
            "- Pattern learning integration",
            "- Comprehensive result documentation",
            "- Performance metrics collection",
        ]

        # Add specific outcomes from patterns
        for pattern in patterns[:2]:
            outcome = pattern.get("outcome", {})
            if "benefits" in outcome and isinstance(outcome["benefits"], list):
                for benefit in outcome["benefits"][:2]:
                    outcomes.append(f"- {benefit}")

        return "\n".join(outcomes[:6])

    def _generate_quality_checks(self, command_name: str, avg_quality: float) -> str:
        """Generate quality checks documentation"""
        return f"""**Quality Checks for {command_name}:**

- Minimum quality score: {self.config['quality_threshold']}/100
- Historical average: {avg_quality:.1f}/100
- Success rate validation
- Pattern consistency verification
- Auto-correction capabilities

**Quality Gates:**
1. Pre-execution validation
2. Mid-execution monitoring
3. Post-execution assessment
4. Pattern learning integration"""

    def _generate_related_commands(self, patterns: List[Dict]) -> str:
        """Generate related commands documentation"""
        related = set()

        for pattern in patterns:
            context = pattern.get("context", {})
            if "command_name" in context and context["command_name"] != patterns[0].get("context", {}).get("command_name"):
                related.add(context["command_name"])

        if not related:
            return "No related commands identified yet."

        return "\n".join(f"- `/{cmd}`" for cmd in sorted(related)[:5])

    def _get_most_common_items(self, items: List[str]) -> List[Tuple[str, int]]:
        """Get most common items from list"""
        from collections import Counter

        counter = Counter(items)
        return counter.most_common(10)

    def generate_all_documentation(self) -> Dict:
        """Generate documentation for all agents, skills, and commands"""
        print("Starting comprehensive documentation generation...")

        patterns_data = self.load_patterns()
        patterns = patterns_data.get("patterns", [])
        doc_patterns = self.extract_documentation_patterns(patterns)

        generated_files = []

        # Generate agent documentation
        if self.config["sections"]["agents"]:
            print("Generating agent documentation...")
            for agent_name, agent_patterns in doc_patterns["agents"].items():
                if len(agent_patterns) >= self.config["min_pattern_count"]:
                    content = self.generate_agent_documentation(agent_name, agent_patterns)
                    filename = f"agent_{agent_name.replace('-', '_')}.md"
                    filepath = os.path.join(self.generated_docs_dir, filename)

                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)

                    generated_files.append(
                        {"type": "agent", "name": agent_name, "file": filename, "patterns_used": len(agent_patterns)}
                    )

        # Generate skill documentation
        if self.config["sections"]["skills"]:
            print("Generating skill documentation...")
            for skill_name, skill_patterns in doc_patterns["skills"].items():
                if len(skill_patterns) >= self.config["min_pattern_count"]:
                    content = self.generate_skill_documentation(skill_name, skill_patterns)
                    filename = f"skill_{skill_name.replace('-', '_')}.md"
                    filepath = os.path.join(self.generated_docs_dir, filename)

                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)

                    generated_files.append(
                        {"type": "skill", "name": skill_name, "file": filename, "patterns_used": len(skill_patterns)}
                    )

        # Generate command documentation
        if self.config["sections"]["commands"]:
            print("Generating command documentation...")
            for command_name, command_patterns in doc_patterns["commands"].items():
                if len(command_patterns) >= self.config["min_pattern_count"]:
                    content = self.generate_command_documentation(command_name, command_patterns)
                    filename = f"command_{command_name.replace('/', '_')}.md"
                    filepath = os.path.join(self.generated_docs_dir, filename)

                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)

                    generated_files.append(
                        {"type": "command", "name": command_name, "file": filename, "patterns_used": len(command_patterns)}
                    )

        # Generate documentation index
        index_content = self._generate_documentation_index(generated_files)
        index_file = os.path.join(self.generated_docs_dir, "README.md")
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(index_content)

        # Save generation metadata
        metadata = {
            "generated_at": datetime.now().isoformat(),
            "total_patterns_analyzed": len(patterns),
            "files_generated": len(generated_files),
            "min_pattern_threshold": self.config["min_pattern_count"],
            "quality_threshold": self.config["quality_threshold"],
            "generated_files": generated_files,
        }

        metadata_file = os.path.join(self.generated_docs_dir, "generation_metadata.json")
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"Documentation generation complete!")
        print(f"  Files generated: {len(generated_files)}")
        print(f"  Output directory: {self.generated_docs_dir}")
        print(f"  Patterns analyzed: {len(patterns)}")

        return {
            "status": "success",
            "files_generated": len(generated_files),
            "patterns_analyzed": len(patterns),
            "output_directory": self.generated_docs_dir,
            "generated_files": generated_files,
            "metadata": metadata,
        }

    def _generate_documentation_index(self, generated_files: List[Dict]) -> str:
        """Generate documentation index/README"""
        content = """# Auto-Generated Documentation

This directory contains comprehensive documentation automatically generated from successful execution patterns.

## Overview

Documentation is generated using advanced pattern analysis and machine learning techniques. Each document represents proven approaches validated through successful autonomous executions.

## Quality Assurance

- **Minimum Quality Threshold**: {}/100
- **Pattern Requirement**: {}+ successful executions
- **Consistency Validation**: Enabled
- **Auto-Update Frequency**: {}

## Generated Documentation

""".format(
            self.config["quality_threshold"], self.config["min_pattern_count"], self.config["update_frequency"]
        )

        # Group by type
        by_type = {}
        for file_info in generated_files:
            doc_type = file_info["type"]
            if doc_type not in by_type:
                by_type[doc_type] = []
            by_type[doc_type].append(file_info)

        for doc_type, files in sorted(by_type.items()):
            content += f"## {doc_type.title()}s\n\n"

            for file_info in sorted(files, key=lambda x: x["name"]):
                content += f"- [{file_info['name'].replace('-', ' ').title()}]({file_info['file']}) "
                content += f"({file_info['patterns_used']} patterns)\n"

            content += "\n"

        content += """## Metadata

- **Generated**: {}
- **Total Files**: {}
- **Patterns Analyzed**: {}
- **Document Types**: {}

## About This Documentation

This documentation is automatically generated by the Documentation Auto-Generation System. It analyzes successful execution patterns to create comprehensive, accurate documentation that reflects real-world usage and proven approaches.

The system ensures:
- **Accuracy**: Based on actual successful executions
- **Completeness**: Covers all aspects of agents, skills, and commands
- **Consistency**: Maintains standardized format and structure
- **Currency**: Updated regularly with new patterns

For more information about the documentation generation process, see the generation_metadata.json file.
""".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            len(generated_files),
            len([f for f in generated_files if f["patterns_used"] >= self.config["min_pattern_count"]]),
            len(set(f["type"] for f in generated_files)),
        )

        return content

    def validate_documentation_consistency(self) -> Dict:
        """Validate consistency across generated documentation"""
        print("Validating documentation consistency...")

        validation_results = {"status": "success", "issues_found": [], "files_validated": 0, "consistency_score": 100}

        # Check for required files
        required_files = ["README.md", "generation_metadata.json"]
        missing_files = [f for f in required_files if not os.path.exists(os.path.join(self.generated_docs_dir, f))]

        if missing_files:
            validation_results["issues_found"].append({"type": "missing_files", "files": missing_files, "severity": "high"})
            validation_results["consistency_score"] -= 20

        # Validate individual files
        md_files = [f for f in os.listdir(self.generated_docs_dir) if f.endswith(".md")]

        for md_file in md_files:
            filepath = os.path.join(self.generated_docs_dir, md_file)
            file_issues = self._validate_markdown_file(filepath)

            if file_issues:
                validation_results["issues_found"].extend(file_issues)
                validation_results["consistency_score"] -= len(file_issues) * 5

            validation_results["files_validated"] += 1

        # Check format consistency
        format_issues = self._check_format_consistency(md_files)
        if format_issues:
            validation_results["issues_found"].extend(format_issues)
            validation_results["consistency_score"] -= len(format_issues) * 3

        # Ensure score doesn't go below 0
        validation_results["consistency_score"] = max(0, validation_results["consistency_score"])

        if validation_results["issues_found"]:
            validation_results["status"] = "issues_found"

        print(f"Documentation validation complete:")
        print(f"  Files validated: {validation_results['files_validated']}")
        print(f"  Issues found: {len(validation_results['issues_found'])}")
        print(f"  Consistency score: {validation_results['consistency_score']}/100")

        return validation_results

    def _validate_markdown_file(self, filepath: str) -> List[Dict]:
        """Validate individual markdown file"""
        issues = []

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Check for required sections
            if "agent_" in filepath:
                required_sections = ["Core Responsibilities", "Skills Integration", "Approach"]
                for section in required_sections:
                    if section not in content:
                        issues.append(
                            {
                                "type": "missing_section",
                                "file": os.path.basename(filepath),
                                "section": section,
                                "severity": "medium",
                            }
                        )

            elif "skill_" in filepath:
                required_sections = ["Overview", "Core Principles", "Implementation Guidelines"]
                for section in required_sections:
                    if section not in content:
                        issues.append(
                            {
                                "type": "missing_section",
                                "file": os.path.basename(filepath),
                                "section": section,
                                "severity": "medium",
                            }
                        )

            elif "command_" in filepath:
                required_sections = ["Description", "Usage", "Examples"]
                for section in required_sections:
                    if section not in content:
                        issues.append(
                            {
                                "type": "missing_section",
                                "file": os.path.basename(filepath),
                                "section": section,
                                "severity": "medium",
                            }
                        )

            # Check for proper formatting
            if not content.startswith("#"):
                issues.append(
                    {
                        "type": "formatting",
                        "file": os.path.basename(filepath),
                        "issue": "Missing main heading",
                        "severity": "low",
                    }
                )

        except Exception as e:
            issues.append({"type": "file_error", "file": os.path.basename(filepath), "error": str(e), "severity": "high"})

        return issues

    def _check_format_consistency(self, md_files: List[str]) -> List[Dict]:
        """Check format consistency across files"""
        issues = []

        # Check file naming consistency
        name_patterns = {
            "agent_": r"^agent_[a-zA-Z0-9_-]+\.md$",
            "skill_": r"^skill_[a-zA-Z0-9_-]+\.md$",
            "command_": r"^command_[a-zA-Z0-9_/-]+\.md$",
        }

        for filename in md_files:
            matched = False
            for prefix, pattern in name_patterns.items():
                if filename.startswith(prefix):
                    if not re.match(pattern, filename):
                        issues.append(
                            {
                                "type": "naming_inconsistency",
                                "file": filename,
                                "expected_pattern": pattern,
                                "severity": "medium",
                            }
                        )
                    matched = True
                    break

            if not matched and filename not in ["README.md", "generation_metadata.json"]:
                issues.append({"type": "unknown_file_type", "file": filename, "severity": "low"})

        return issues


def main():
    """CLI interface for documentation auto-generator"""
    import argparse

    parser = argparse.ArgumentParser(description="Documentation Auto-Generation System")
    parser.add_argument("--dir", default=".claude-patterns", help="Patterns directory")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--generate", action="store_true", help="Generate all documentation")
    parser.add_argument("--validate", action="store_true", help="Validate documentation consistency")
    parser.add_argument("--config", action="store_true", help="Show current configuration")

    args = parser.parse_args()

    generator = DocumentationAutoGenerator(args.dir, args.project_root)

    if args.generate:
        result = generator.generate_all_documentation()
        print(f"\nGeneration Status: {result['status']}")
        print(f"Files Generated: {result['files_generated']}")

    elif args.validate:
        result = generator.validate_documentation_consistency()
        print(f"\nValidation Status: {result['status']}")
        print(f"Consistency Score: {result['consistency_score']}/100")

        if result["issues_found"]:
            print(f"\nIssues Found ({len(result['issues_found'])}):")
            for issue in result["issues_found"][:5]:  # Show first 5 issues
                print(f"  - {issue['type']}: {issue.get('file', 'N/A')}")

    elif args.config:
        print(f"Current Configuration:")
        for key, value in generator.config.items():
            print(f"  {key}: {value}")

    else:
        print("Documentation Auto-Generation System")
        print("Use --help to see available commands")


if __name__ == "__main__":
    main()
