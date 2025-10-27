#!/usr/bin/env python3
"""
Enhanced Learning Engine for Autonomous Claude Agent Plugin

Advanced pattern learning system with contextual understanding, confidence scoring,
skill effectiveness tracking, and cross-project pattern transfer capabilities.
"""

import json
import argparse
import sys
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
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


class EnhancedLearningEngine:
    """Advanced learning engine with contextual pattern recognition and predictive capabilities."""

    def __init__(self, patterns_dir: str = ".claude-patterns"):
        """
        Initialize enhanced learning engine.

        Args:
            patterns_dir: Directory path for storing patterns (
    default: .claude-patterns,
)
        """
        self.patterns_dir = Path(patterns_dir)
        self.patterns_file = self.patterns_dir / "enhanced_patterns.json"
        self.skill_metrics_file = self.patterns_dir / "skill_metrics.json"
        self.agent_metrics_file = self.patterns_dir / "agent_metrics.json"
        self.cross_project_file = self.patterns_dir / "cross_project_patterns.json"
        self._ensure_directories()

    def _ensure_directories(self):
        """Create necessary directories and files."""
        self.patterns_dir.mkdir(parents=True, exist_ok=True)

        # Initialize enhanced patterns schema
        if not self.patterns_file.exists():
            self._write_enhanced_patterns({
                "version": "3.0.0",
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat(),
                    "total_patterns": 0,
                    "learning_effectiveness": 0.0,
                    "prediction_accuracy": 0.0
                },
                "project_fingerprint": {},
                "patterns": [],
                "skill_effectiveness": {},
                "agent_performance": {},
                "trends": {},
                "predictions": {}
            })

        # Initialize skill metrics
        if not self.skill_metrics_file.exists():
            self._write_skill_metrics({})

        # Initialize agent metrics
        if not self.agent_metrics_file.exists():
            self._write_agent_metrics({})

        # Initialize cross-project patterns
        if not self.cross_project_file.exists():
            self._write_cross_project_patterns({
                "version": "1.0.0",
                "universal_patterns": [],
                "project_contributions": {},
                "last_sync": datetime.now().isoformat()
            })

    def _read_json_file(self, file_path: Path) -> Dict[str, Any]:
        """Read JSON file with locking."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lock_file(f, exclusive=False)
                try:
                    content = f.read()
                    if not content.strip():
                        return {}
                    return json.loads(content)
                finally:
                    unlock_file(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _write_json_file(self, file_path: Path, data: Dict[str, Any]):
        """Write JSON file with locking."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                lock_file(f, exclusive=True)
                try:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                finally:
                    unlock_file(f)
        except Exception as e:
            print(f"Error writing {file_path}: {e}", file=sys.stderr)
            raise

    def _read_enhanced_patterns(self) -> Dict[str, Any]:
        """Read enhanced patterns database."""
        return self._read_json_file(self.patterns_file)

    def _write_enhanced_patterns(self, data: Dict[str, Any]):
        """Write enhanced patterns database."""
        data["metadata"]["last_updated"] = datetime.now().isoformat()
        self._write_json_file(self.patterns_file, data)

    def _read_skill_metrics(self) -> Dict[str, Any]:
        """Read skill effectiveness metrics."""
        return self._read_json_file(self.skill_metrics_file)

    def _write_skill_metrics(self, data: Dict[str, Any]):
        """Write skill effectiveness metrics."""
        self._write_json_file(self.skill_metrics_file, data)

    def _read_agent_metrics(self) -> Dict[str, Any]:
        """Read agent performance metrics."""
        return self._read_json_file(self.agent_metrics_file)

    def _write_agent_metrics(self, data: Dict[str, Any]):
        """Write agent performance metrics."""
        self._write_json_file(self.agent_metrics_file, data)

    def _read_cross_project_patterns(self) -> Dict[str, Any]:
        """Read cross-project patterns."""
        return self._read_json_file(self.cross_project_file)

    def _write_cross_project_patterns(self, data: Dict[str, Any]):
        """Write cross-project patterns."""
        data["last_sync"] = datetime.now().isoformat()
        self._write_json_file(self.cross_project_file, data)

    def generate_project_fingerprint(self, project_context: Dict[str, Any]) -> str:
        """
        Generate unique project fingerprint for pattern matching.

        Args:
            project_context: Dictionary containing project information

        Returns:
            SHA256 hash representing project fingerprint
        """
        fingerprint_data = {
            "languages": sorted(project_context.get("languages", [])),
            "frameworks": sorted(project_context.get("frameworks", [])),
            "project_type": project_context.get("project_type", ""),
            "package_managers": sorted(project_context.get("package_managers", [])),
            "file_structure_patterns": project_context.get(
    "file_structure_patterns",
    []),,
)
            "dependencies": sorted(project_context.get("top_dependencies", []))
        }

        fingerprint_str = json.dumps(fingerprint_data, sort_keys=True)
        return hashlib.sha256(fingerprint_str.encode()).hexdigest()[:16]

    def enhance_project_context_for_modern_stacks(
    self,
    project_context: Dict[str,
    Any],
    project_path: str = ".") -> Dict[str, Any]:,
)
        """
        Enhance project context with specific detection for NextJS, Supabase, and 
            other modern stacks.

        Args:
            project_context: Existing project context
            project_path: Path to the project root

        Returns:
            Enhanced project context with modern framework detection
        """
        enhanced_context = project_context.copy()
        path = Path(project_path)

        # NextJS Detection
        nextjs_indicators = [
            "next.config.js", "next.config.mjs", "next.config.ts",
            "pages/", "app/", ".next/"
        ]

        if any((path / indicator).exists() for indicator in nextjs_indicators):
            enhanced_context.setdefault("frameworks", []).append("nextjs")

            # Detect NextJS features
            if (path / "app").exists():
                enhanced_context.setdefault("features", []).append("nextjs-app-router")
            if (path / "pages").exists():
                enhanced_context.setdefault(
    "features",
    []).append("nextjs-pages-router",
)
            if (path / "next.config.js").exists():
                enhanced_context.setdefault(
    "features",
    []).append("nextjs-configuration",
)

        # Supabase Detection
        supabase_indicators = [
            "supabase/", "lib/supabase", "utils/supabase",
            "supabase.js", "supabase.ts"
        ]

        if any((path / indicator).exists() for indicator in supabase_indicators):
            enhanced_context.setdefault("frameworks", []).append("supabase")
            enhanced_context.setdefault("features", []).append("database-as-a-service")

            # Detect Supabase configuration
            if (path / "supabase/migrations").exists():
                enhanced_context.setdefault(
    "features",
    []).append("supabase-migrations",
)
            if (path / "supabase/functions").exists():
                enhanced_context.setdefault(
    "features",
    []).append("supabase-edge-functions",
)

        # Modern React Stack Detection
        package_json_path = path / "package.json"
        if package_json_path.exists():
            try:
                import json as json_module
                with open(package_json_path, 'r') as f:
                    package_data = json_module.load(f)

                dependencies = {**package_data.get("dependencies", {}),
                              **package_data.get("devDependencies", {})}

                # React ecosystem detection
                if "react" in dependencies:
                    enhanced_context.setdefault("frameworks", []).append("react")

                    if "next" in dependencies:
                        enhanced_context.setdefault("frameworks", []).append("nextjs")
                    if "@supabase/supabase-js" in dependencies:
                        enhanced_context.setdefault("frameworks", []).append("supabase")
                    if "tailwindcss" in dependencies:
                        enhanced_context.setdefault(
    "frameworks",
    []).append("tailwindcss",
)
                    if "typescript" in dependencies:
                        enhanced_context.setdefault(
    "languages",
    []).append("typescript",
)

            except Exception:
                pass  # Ignore JSON parsing errors

        # Swift/iOS Detection (Enhanced v3.2.0)
        swift_indicators = [
            "Package.swift", "Package.resolved", "Sources/", "Tests/",
            "*.xcodeproj", "*.xcworkspace", "Info.plist", "ContentView.swift"
        ]

        if any((path / indicator).exists() for indicator in swift_indicators) or \
           any(path.glob("*.swift")):
            enhanced_context.setdefault("languages", []).append("swift")

            # Detect Swift frameworks
            if (path / "Package.swift").exists():
                enhanced_context.setdefault(
    "frameworks",
    []).append("swift-package-manager",
)
                enhanced_context.setdefault("features", []).append("swiftpm-project")

            if (path / "*.xcodeproj").exists() or (path / "*.xcworkspace").exists():
                enhanced_context.setdefault("frameworks", []).append("xcode")
                enhanced_context.setdefault("features", []).append("ios-project")

            # Detect iOS-specific features
            if any(path.glob("*.storyboard")) or any(path.glob("*.xib")):
                enhanced_context.setdefault(
    "features",
    []).append("ios-interface-builder",
)
            if (path / "Info.plist").exists():
                enhanced_context.setdefault(
    "features",
    []).append("ios-app-configuration",
)

        # Kotlin/Android Detection (Enhanced v3.2.0)
        kotlin_indicators = [
            "build.gradle.kts", "build.gradle", "settings.gradle.kts",
            "src/main/kotlin", "src/test/kotlin", "gradle.properties"
        ]

        if any((path / indicator).exists() for indicator in kotlin_indicators) or \
           any(path.glob("**/*.kt")):
            enhanced_context.setdefault("languages", []).append("kotlin")

            # Detect Kotlin frameworks
            if (path / "build.gradle.kts").exists() or (path / "build.gradle").exists():
                enhanced_context.setdefault("frameworks", []).append("gradle")

            # Check for Android-specific files
            android_indicators = ["AndroidManifest.xml", "app/src/main", "res/layout"]
            if any((path / indicator).exists() for indicator in android_indicators):
                enhanced_context.setdefault("frameworks", []).append("android")
                enhanced_context.setdefault("features", []).append("android-app")

            # Check for Spring Boot with Kotlin
            if (path / "build.gradle.kts").exists():
                try:
                    with open(path / "build.gradle.kts", 'r') as f:
                        gradle_content = f.read()
                        if "spring-boot" in gradle_content or 
                            "org.springframework.boot" in gradle_content:
                            enhanced_context.setdefault(
    "frameworks",
    []).append("spring-boot",
)
                            enhanced_context.setdefault(
    "features",
    []).append("kotlin-spring-boot",
)
                except Exception:
                    pass

            # Check for Ktor
            if (path / "build.gradle.kts").exists():
                try:
                    with open(path / "build.gradle.kts", 'r') as f:
                        gradle_content = f.read()
                        if "ktor" in gradle_content or "io.ktor" in gradle_content:
                            enhanced_context.setdefault("frameworks", []).append("ktor")
                            enhanced_context.setdefault(
    "features").append("kotlin-web-framework",
)
                except Exception:
                    pass

        # Scala Detection (Enhanced v3.2.0)
        scala_indicators = [
            "build.sbt", "project/", "src/main/scala", "src/test/scala",
            "pom.xml", "*.scala"
        ]

        if any((path / indicator).exists() for indicator in scala_indicators) or \
           any(path.glob("**/*.scala")):
            enhanced_context.setdefault("languages", []).append("scala")

            # Detect Scala frameworks
            if (path / "build.sbt").exists():
                enhanced_context.setdefault("frameworks", []).append("sbt")

            # Check for Play Framework
            if (path / "app").exists() and (path / "conf").exists():
                enhanced_context.setdefault("frameworks", []).append("play")
                enhanced_context.setdefault("features", []).append("play-web-framework")

            # Check for Akka
            if (path / "build.sbt").exists():
                try:
                    with open(path / "build.sbt", 'r') as f:
                        sbt_content = f.read()
                        if "akka" in sbt_content or "com.typesafe.akka" in sbt_content:
                            enhanced_context.setdefault("frameworks", []).append("akka")
                            enhanced_context.setdefault(
    "features").append("akka-actor-system",
)
                except Exception:
                    pass

            # Check for Apache Spark
            if (path / "build.sbt").exists():
                try:
                    with open(path / "build.sbt", 'r') as f:
                        sbt_content = f.read()
                        if "spark" in sbt_content or "org.apache.spark" in sbt_content:
                            enhanced_context.setdefault(
    "frameworks",
    []).append("spark",
)
                            enhanced_context.setdefault(
    "features").append("big-data-processing",
)
                except Exception:
                    pass

        # Remove duplicates and sort
        enhanced_context["frameworks"] = sorted(list(set(enhanced_context.get("frameworks", []))))
        enhanced_context["languages"] = sorted(list(set(enhanced_context.get("languages", []))))
        enhanced_context["features"] = sorted(list(set(enhanced_context.get("features", []))))

        return enhanced_context

    def calculate_context_similarity(
    self,
    context1: Dict[str,
    Any],
    context2: Dict[str,
    Any]) -> float:,
)
        """
        Calculate similarity between two contexts (0.0 to 1.0).

        Args:
            context1, context2: Context dictionaries

        Returns:
            Similarity score
        """
        # Language similarity (40% weight)
        langs1, langs2 = set(context1.get("languages", [])), set(context2.get("languages", []))
        lang_similarity = len(langs1 & langs2) / max(len(langs1 | langs2), 1)

        # Framework similarity (30% weight)
        frameworks1, frameworks2 = set(context1.get("frameworks", [])), set(context2.get("frameworks", []))
        framework_similarity = len(frameworks1 & frameworks2) / max(len(frameworks1 | frameworks2), 1)

        # Project type similarity (20% weight)
        type_similarity = 1.0 if 
            context1.get("project_type") == context2.get("project_type") else 0.0

        # File structure similarity (10% weight)
        structure1, structure2 = set(context1.get("file_patterns", [])), set(context2.get("file_patterns", []))
        structure_similarity = len(structure1 & structure2) / max(len(structure1 | structure2), 1)

        return (lang_similarity * 0.4 + framework_similarity * 0.3 +
                type_similarity * 0.2 + structure_similarity * 0.1)

    def capture_enhanced_pattern(self, pattern_data: Dict[str, Any]) -> str:
        """
        Capture an enhanced learning pattern with rich context.

        Args:
            pattern_data: Comprehensive pattern data dictionary

        Returns:
            Pattern ID of stored pattern
        """
        # Generate unique pattern ID
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
        pattern_id = f"enhanced_pattern_{timestamp}"

        # Enhanced pattern structure
        enhanced_pattern = {
            "pattern_id": pattern_id,
            "timestamp": datetime.now().isoformat(),

            # Task Classification
            "task_classification": {
                "type": pattern_data.get("task_type", "unknown"),
                "complexity": pattern_data.get("complexity", "medium"),
                "domain": pattern_data.get("domain", "general"),
                "security_critical": pattern_data.get("security_critical", False),
                "estimated_duration": pattern_data.get("duration_seconds", 0)
            },

            # Contextual Understanding
            "context": {
                "project_fingerprint": self.generate_project_fingerprint(
    pattern_data.get("project_context", {})),,
)
                "languages": pattern_data.get("languages", []),
                "frameworks": pattern_data.get("frameworks", []),
                "project_type": pattern_data.get("project_type", ""),
                "file_patterns": pattern_data.get("file_patterns", []),
                "module_type": pattern_data.get("module_type", ""),
                "team_size": pattern_data.get("team_size", "unknown"),
                "development_stage": pattern_data.get("development_stage", "active")
            },

            # Execution Details
            "execution": {
                "skills_loaded": pattern_data.get("skills_used", []),
                "skill_loading_strategy": pattern_data.get(
    "skill_loading_strategy",
    "auto"),,
)
                "agents_delegated": pattern_data.get("agents_delegated", []),
                "delegation_reasoning": pattern_data.get("delegation_reasoning", ""),
                "approach_taken": pattern_data.get("approach", ""),
                "tools_used": pattern_data.get("tools_used", []),
                "model_detected": pattern_data.get("model_detected", "unknown"),
                "model_confidence": pattern_data.get("model_confidence", 0.0)
            },

            # Outcome Metrics
            "outcome": {
                "success": pattern_data.get("success", True),
                "quality_score": pattern_data.get("quality_score", 0.0),
                "tests_passing": pattern_data.get("tests_passing", 0),
                "test_coverage_change": pattern_data.get("test_coverage_change", 0),
                "standards_compliance": pattern_data.get("standards_score", 0.0),
                "documentation_coverage": pattern_data.get("docs_coverage", 0.0),
                "user_satisfaction": pattern_data.get("user_satisfaction", 0),
                "errors_encountered": pattern_data.get("errors", []),
                "performance_impact": pattern_data.get("performance_impact", "neutral")
            },

            # Learning Insights
            "insights": {
                "what_worked": pattern_data.get("what_worked", []),
                "what_failed": pattern_data.get("what_failed", []),
                "bottlenecks": pattern_data.get("bottlenecks", []),
                "optimization_opportunities": pattern_data.get(
    "optimization_opportunities",
    []),,
)
                "lessons_learned": pattern_data.get("lessons_learned", []),
                "unexpected_discoveries": pattern_data.get("unexpected_discoveries", [])
            },

            # Reuse Analytics
            "reuse_analytics": {
                "reuse_count": 0,
                "last_reused": None,
                "reuse_success_rate": 1.0,
                "confidence_boost": 0.0,
                "adaptation_notes": []
            },

            # Prediction Data
            "prediction_data": {
                "predicted_quality": pattern_data.get("predicted_quality", 0.0),
                "prediction_accuracy": 0.0,
                "skill_effectiveness_scores": {},
                "context_similarity_scores": {}
            }
        }

        # Store pattern
        patterns_db = self._read_enhanced_patterns()
        patterns_db["patterns"].append(enhanced_pattern)
        patterns_db["metadata"]["total_patterns"] += 1

        # Update skill effectiveness
        self._update_skill_effectiveness(enhanced_pattern)

        # Update agent performance
        self._update_agent_performance(enhanced_pattern)

        # Update project fingerprint
        patterns_db["project_fingerprint"] = enhanced_pattern["context"]["project_fingerprint"]

        self._write_enhanced_patterns(patterns_db)

        # Contribute to cross-project learning
        self._contribute_to_cross_project(enhanced_pattern)

        return pattern_id

    def _update_skill_effectiveness(self, pattern: Dict[str, Any]):
        """Update skill effectiveness metrics based on pattern outcome."""
        skills_db = self._read_skill_metrics()
        task_type = pattern["task_classification"]["type"]
        outcome = pattern["outcome"]
        execution = pattern["execution"]

        for skill in execution["skills_loaded"]:
            if skill not in skills_db:
                skills_db[skill] = {
                    "total_uses": 0,
                    "successful_uses": 0,
                    "success_rate": 0.0,
                    "avg_quality_contribution": 0.0,
                    "quality_scores": [],
                    "by_task_type": {},
                    "recommended_for": [],
                    "not_recommended_for": [],
                    "confidence_score": 0.5,
                    "last_updated": datetime.now().isoformat(),
                    "performance_trend": "stable",
                    "synergy_skills": {}
                }

            skill_metrics = skills_db[skill]

            # Update basic metrics
            skill_metrics["total_uses"] += 1
            if outcome["success"]:
                skill_metrics["successful_uses"] += 1

            skill_metrics["success_rate"] = skill_metrics["successful_uses"] / skill_metrics["total_uses"]

            # Update quality contribution
            skill_metrics["quality_scores"].append(outcome["quality_score"])
            if len(skill_metrics["quality_scores"]) > 100:  # Keep last 100 scores
                skill_metrics["quality_scores"] = skill_metrics["quality_scores"][-100:]

            skill_metrics["avg_quality_contribution"] = sum(skill_metrics["quality_scores"]) / len(skill_metrics["quality_scores"])

            # Update task type specific metrics
            if task_type not in skill_metrics["by_task_type"]:
                skill_metrics["by_task_type"][task_type] = {
                    "uses": 0,
                    "successes": 0,
                    "avg_quality": 0.0,
                    "success_rate": 0.0
                }

            task_metrics = skill_metrics["by_task_type"][task_type]
            task_metrics["uses"] += 1
            if outcome["success"]:
                task_metrics["successes"] += 1

            task_metrics["success_rate"] = task_metrics["successes"] / task_metrics["uses"]

            # Calculate average quality for this task type
            type_patterns = [p for p in self._read_enhanced_patterns()["patterns"]
                           if skill in p["execution"]["skills_loaded"] and
                           p["task_classification"]["type"] == task_type]
            if type_patterns:
                task_metrics["avg_quality"] = sum(p["outcome"]["quality_score"] for p in 
                    
                    type_patterns) / len(type_patterns)

            # Update confidence score based on consistency
            recent_scores = skill_metrics["quality_scores"][-20:]  # Last 20 uses
            if len(recent_scores) >= 10:
                variance = sum((x - sum(recent_scores)/len(recent_scores))**2 for x in 
                    recent_scores) / len(recent_scores)
                skill_metrics["confidence_score"] = max(0.1, 1.0 - variance / 100)  # Normalize variance

            # Update recommendations
            skill_metrics["recommended_for"] = [
                t for t, metrics in skill_metrics["by_task_type"].items()
                if metrics["success_rate"] >= 0.8 and metrics["uses"] >= 3
            ]

            skill_metrics["not_recommended_for"] = [
                t for t, metrics in skill_metrics["by_task_type"].items()
                if metrics["success_rate"] < 0.5 and metrics["uses"] >= 5
            ]

            # Update performance trend
            if len(recent_scores) >= 10:
                recent_avg = sum(recent_scores[-10:]) / 10
                older_avg = sum(recent_scores[-20:-10]) / 10 if 
                    len(recent_scores) >= 20 else recent_avg

                if recent_avg > older_avg + 5:
                    skill_metrics["performance_trend"] = "improving"
                elif recent_avg < older_avg - 5:
                    skill_metrics["performance_trend"] = "declining"
                else:
                    skill_metrics["performance_trend"] = "stable"

            skill_metrics["last_updated"] = datetime.now().isoformat()

        self._write_skill_metrics(skills_db)

    def _update_agent_performance(self, pattern: Dict[str, Any]):
        """Update agent performance metrics based on pattern outcome."""
        agents_db = self._read_agent_metrics()
        task_type = pattern["task_classification"]["type"]
        outcome = pattern["outcome"]
        execution = pattern["execution"]

        for agent in execution["agents_delegated"]:
            if agent not in agents_db:
                agents_db[agent] = {
                    "total_delegations": 0,
                    "successful_completions": 0,
                    "success_rate": 0.0,
                    "execution_times": [],
                    "avg_execution_time": 0.0,
                    "quality_scores": [],
                    "avg_quality_score": 0.0,
                    "by_task_type": {},
                    "common_errors": {},
                    "reliability_score": 0.5,
                    "efficiency_rating": 0.5,
                    "last_updated": datetime.now().isoformat(),
                    "performance_trend": "stable"
                }

            agent_metrics = agents_db[agent]

            # Update basic metrics
            agent_metrics["total_delegations"] += 1
            if outcome["success"]:
                agent_metrics["successful_completions"] += 1

            agent_metrics["success_rate"] = agent_metrics["successful_completions"] / agent_metrics["total_delegations"]

            # Update execution time
            duration = pattern["task_classification"]["estimated_duration"]
            agent_metrics["execution_times"].append(duration)
            if len(agent_metrics["execution_times"]) > 50:  # Keep last 50
                agent_metrics["execution_times"] = agent_metrics["execution_times"][-50:]

            agent_metrics["avg_execution_time"] = sum(agent_metrics["execution_times"]) / len(agent_metrics["execution_times"])

            # Update quality scores
            agent_metrics["quality_scores"].append(outcome["quality_score"])
            if len(agent_metrics["quality_scores"]) > 50:
                agent_metrics["quality_scores"] = agent_metrics["quality_scores"][-50:]

            agent_metrics["avg_quality_score"] = sum(agent_metrics["quality_scores"]) / len(agent_metrics["quality_scores"])

            # Update task type specific metrics
            if task_type not in agent_metrics["by_task_type"]:
                agent_metrics["by_task_type"][task_type] = {
                    "delegations": 0,
                    "successes": 0,
                    "avg_duration": 0.0,
                    "avg_quality": 0.0
                }

            task_metrics = agent_metrics["by_task_type"][task_type]
            task_metrics["delegations"] += 1
            if outcome["success"]:
                task_metrics["successes"] += 1

            # Calculate averages for this task type
            type_patterns = [p for p in self._read_enhanced_patterns()["patterns"]
                           if agent in p["execution"]["agents_delegated"] and
                           p["task_classification"]["type"] == task_type]
            if type_patterns:
                task_metrics["avg_duration"] = sum(p["task_classification"]["estimated_duration"] for p in 
                    
                    type_patterns) / len(type_patterns)
                task_metrics["avg_quality"] = sum(p["outcome"]["quality_score"] for p in 
                    
                    type_patterns) / len(type_patterns)

            # Track common errors
            for error in outcome.get("errors_encountered", []):
                error_type = error.get("type", "unknown")
                agent_metrics["common_errors"][error_type] = agent_metrics["common_errors"].get(error_type, 0) + 1

            # Calculate reliability score
            reliability_factors = [
                agent_metrics["success_rate"],
                min(1.0, agent_metrics["avg_quality_score"] / 100),
                1.0 - min(
    1.0,
    len(agent_metrics["common_errors"]) / 10)  # Penalize many error types,
)
            ]
            agent_metrics["reliability_score"] = sum(reliability_factors) / len(reliability_factors)

            # Calculate efficiency rating (quality per time)
            if agent_metrics["avg_execution_time"] > 0:
                agent_metrics["efficiency_rating"] = (agent_metrics["avg_quality_score"] / agent_metrics["avg_execution_time"]) * 10

            # Update performance trend
            recent_quality = agent_metrics["quality_scores"][-10:] if 
                len(
    agent_metrics["quality_scores"]) >= 10 else agent_metrics["quality_scores"],
)
            if len(recent_quality) >= 5:
                recent_avg = sum(recent_quality[-5:]) / 5
                older_avg = sum(recent_quality[-10:-5]) / 5 if 
                    len(recent_quality) >= 10 else recent_avg

                if recent_avg > older_avg + 3:
                    agent_metrics["performance_trend"] = "improving"
                elif recent_avg < older_avg - 3:
                    agent_metrics["performance_trend"] = "declining"
                else:
                    agent_metrics["performance_trend"] = "stable"

            agent_metrics["last_updated"] = datetime.now().isoformat()

        self._write_agent_metrics(agents_db)

    def _contribute_to_cross_project(self, pattern: Dict[str, Any]):
        """Contribute pattern to cross-project learning (anonymized)."""
        cross_project_db = self._read_cross_project_patterns()

        # Create anonymized pattern for cross-project sharing
        universal_pattern = {
            "pattern_id": f"universal_{pattern['pattern_id']}",
            "timestamp": pattern["timestamp"],
            "task_classification": pattern["task_classification"],
            "context_categories": {
                "languages": pattern["context"]["languages"],
                "frameworks": pattern["context"]["frameworks"],
                "project_type": pattern["context"]["project_type"]
            },
            "execution": {
                "skills_loaded": pattern["execution"]["skills_loaded"],
                "agents_delegated": pattern["execution"]["agents_delegated"],
                "approach_category": self._categorize_approach(
    pattern["execution"]["approach_taken"],
)
            },
            "outcome": {
                "success": pattern["outcome"]["success"],
                "quality_score": pattern["outcome"]["quality_score"],
                "performance_impact": pattern["outcome"]["performance_impact"]
            },
            "effectiveness_metrics": {
                "skill_combination_success": self._calculate_skill_combination_success(
    pattern),,
)
                "agent_effectiveness": self._calculate_agent_effectiveness(pattern),
                "context_transferability": self._calculate_transferability(pattern)
            }
        }

        cross_project_db["universal_patterns"].append(universal_pattern)

        # Keep only last 1000 universal patterns
        if len(cross_project_db["universal_patterns"]) > 1000:
            cross_project_db["universal_patterns"] = cross_project_db["universal_patterns"][-1000:]

        self._write_cross_project_patterns(cross_project_db)

    def _categorize_approach(self, approach: str) -> str:
        """Categorize approach type for pattern matching."""
        approach_lower = approach.lower()

        if any(
    word in approach_lower for word in ["refactor",
    "extract",
    "restructure"]):,
)
            return "refactoring"
        elif any(word in approach_lower for word in ["test", "spec", "verify"]):
            return "testing"
        elif any(word in approach_lower for word in ["fix", "debug", "resolve"]):
            return "debugging"
        elif any(word in approach_lower for word in ["implement", "add", "create"]):
            return "implementation"
        elif any(word in approach_lower for word in ["optimize", "improve", "enhance"]):
            return "optimization"
        elif any(word in approach_lower for word in ["security", "secure", "protect"]):
            return "security"
        else:
            return "general"

    def _calculate_skill_combination_success(self, pattern: Dict[str, Any]) -> float:
        """Calculate success rate for the skill combination used."""
        skills = tuple(sorted(pattern["execution"]["skills_loaded"]))
        patterns_db = self._read_enhanced_patterns()

        similar_patterns = [p for p in patterns_db["patterns"]
                          if tuple(sorted(p["execution"]["skills_loaded"])) == skills]

        if not similar_patterns:
            return 0.5  # Neutral score for new combinations

        success_count = sum(1 for p in similar_patterns if p["outcome"]["success"])
        return success_count / len(similar_patterns)

    def _calculate_agent_effectiveness(self, pattern: Dict[str, Any]) -> float:
        """Calculate effectiveness score for agents used."""
        agents = pattern["execution"]["agents_delegated"]
        agents_db = self._read_agent_metrics()

        if not agents:
            return 0.5

        total_reliability = 0.0
        for agent in agents:
            if agent in agents_db:
                total_reliability += agents_db[agent].get("reliability_score", 0.5)
            else:
                total_reliability += 0.5  # Default for unknown agents

        return total_reliability / len(agents)

    def _calculate_transferability(self, pattern: Dict[str, Any]) -> float:
        """Calculate how transferable this pattern is to other projects."""
        # Higher transferability for:
        # - Common languages/frameworks
        # - General project types
        # - Successful outcomes
        # - Standard approaches

        languages = pattern["context"]["languages"]
        frameworks = pattern["context"]["frameworks"]
        project_type = pattern["context"]["project_type"]
        quality = pattern["outcome"]["quality_score"]

        # Common tech stacks get higher transferability (enhanced v3.2.0)
        common_languages = {"python", "javascript", "typescript", "java", "go", "rust", "swift", "kotlin", "scala"}
        common_frameworks = {"react", "vue", "angular", "nextjs", "nuxt", "flask", "django", "express", "fastapi", "supabase",
                            "spring", "spring-boot", "vapor", "ktor", "play", "akka", "spark", "android", "ios"}

        language_score = len([l for l in languages if 
            l in common_languages]) / max(len(languages), 1)
        framework_score = len([f for f in frameworks if 
            f in common_frameworks]) / max(len(frameworks), 1)

        # General project types are more transferable
        general_types = {"web-application", "api", "library", "cli-tool"}
        type_score = 1.0 if project_type in general_types else 0.5

        # High quality patterns are more transferable
        quality_score = min(1.0, quality / 85)  # 85+ is considered high quality

        return (
    language_score * 0.3 + framework_score * 0.3 + type_score * 0.2 + quality_score * 0.2,
)

    def predict_optimal_skills(
    self,
    task_context: Dict[str,
    Any],
    limit: int = 5) -> List[Dict[str, Any]]:,
)
        """
        Predict optimal skills for a given task context.

        Args:
            task_context: Dictionary containing task information
            limit: Maximum number of skill recommendations

        Returns:
            List of skill recommendations with confidence scores
        """
        patterns_db = self._read_enhanced_patterns()
        skills_db = self._read_skill_metrics()
        cross_project_db = self._read_cross_project_patterns()

        task_type = task_context.get("task_type", "unknown")
        project_fingerprint = self.generate_project_fingerprint(task_context.get("project_context", {}))

        # Find similar patterns in local project
        local_matches = []
        for pattern in patterns_db["patterns"]:
            similarity = self.calculate_context_similarity(
                task_context.get("project_context", {}),
                pattern["context"]
            )

            if similarity >= 0.3 and 
                pattern["task_classification"]["type"] == task_type:
                local_matches.append((pattern, similarity))

        # Sort by similarity and quality
        local_matches.sort(
    key=lambda x: (x[1], x[0]["outcome"]["quality_score"]),
    reverse=True,
)

        # Find matches in cross-project patterns
        cross_matches = []
        for pattern in cross_project_db["universal_patterns"]:
            if pattern["task_classification"]["type"] == task_type:
                # Simple context matching for cross-project
                context_match = 0
                if 
                    pattern["context_categories"]["project_type"] == 
                        task_context.get("project_context", {}).get("project_type"):
                    context_match += 0.5
                if set(
    pattern["context_categories"]["languages"]) & set(
    task_context.get("project_context", {}).get("languages", [])):,,
)
)
                    context_match += 0.3
                if set(
    pattern["context_categories"]["frameworks"]) & set(
    task_context.get("project_context", {}).get("frameworks", [])):,,
)
)
                    context_match += 0.2

                if context_match > 0:
                    cross_matches.append((pattern, context_match))

        cross_matches.sort(key=lambda x: x[1], reverse=True)

        # Aggregate skill recommendations
        skill_scores = {}

        # Weight local matches higher
        for pattern, similarity in local_matches[:10]:  # Top 10 local matches
            weight = similarity * (pattern["outcome"]["quality_score"] / 100)
            for skill in pattern["execution"]["skills_loaded"]:
                if skill not in skill_scores:
                    skill_scores[skill] = {
                        "total_score": 0.0,
                        "local_matches": 0,
                        "cross_matches": 0,
                        "avg_quality": 0.0,
                        "confidence": 0.0
                    }

                skill_scores[skill]["total_score"] += weight
                skill_scores[skill]["local_matches"] += 1
                skill_scores[skill]["avg_quality"] += pattern["outcome"]["quality_score"]

        # Add cross-project matches with lower weight
        for pattern, similarity in cross_matches[:5]:  # Top 5 cross matches
            weight = similarity * 0.5 * (pattern["outcome"]["quality_score"] / 100)
            for skill in pattern["execution"]["skills_loaded"]:
                if skill not in skill_scores:
                    skill_scores[skill] = {
                        "total_score": 0.0,
                        "local_matches": 0,
                        "cross_matches": 0,
                        "avg_quality": 0.0,
                        "confidence": 0.0
                    }

                skill_scores[skill]["total_score"] += weight
                skill_scores[skill]["cross_matches"] += 1
                skill_scores[skill]["avg_quality"] += pattern["outcome"]["quality_score"]

        # Calculate final scores and confidence
        recommendations = []
        for skill, scores in skill_scores.items():
            # Get skill effectiveness metrics
            skill_metrics = skills_db.get(skill, {})

            # Base score from pattern matching
            pattern_score = scores["total_score"]

            # Boost from skill effectiveness
            effectiveness_boost = skill_metrics.get("success_rate", 0.5) * 0.3
            confidence_boost = skill_metrics.get("confidence_score", 0.5) * 0.2

            # Task type specific boost
            task_type_boost = 0.0
            if task_type in skill_metrics.get("recommended_for", []):
                task_type_boost = 0.3
            elif task_type in skill_metrics.get("not_recommended_for", []):
                task_type_boost = -0.5

            # Final score
            final_score = pattern_score + effectiveness_boost + confidence_boost + task_type_boost

            # Calculate confidence
            total_matches = scores["local_matches"] + scores["cross_matches"]
            confidence = min(1.0, (total_matches / 5) * skill_metrics.get("confidence_score", 0.5))

            # Average quality of patterns using this skill
            avg_quality = scores["avg_quality"] / max(1, total_matches)

            recommendations.append({
                "skill": skill,
                "score": final_score,
                "confidence": confidence,
                "local_matches": scores["local_matches"],
                "cross_matches": scores["cross_matches"],
                "avg_quality": avg_quality,
                "effectiveness": skill_metrics.get("success_rate", 0.5),
                "reasoning": self._generate_skill_reasoning(
    skill,
    scores,
    skill_metrics,
    task_type,
)
            })

        # Sort by score and return top recommendations
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        return recommendations[:limit]

    def _generate_skill_reasoning(
    self,
    skill: str,
    scores: Dict,
    skill_metrics: Dict,
    task_type: str) -> str:,
)
        """Generate reasoning for skill recommendation."""
        reasons = []

        if scores["local_matches"] > 0:
            reasons.append(f"Found in {scores['local_matches']} similar local patterns")

        if scores["cross_matches"] > 0:
            reasons.append(
    f"Successful in {scores['cross_matches']} cross-project patterns",
)

        if skill_metrics.get("success_rate", 0) >= 0.8:
            reasons.append(f"High success rate ({skill_metrics['success_rate']:.1%})")

        if task_type in skill_metrics.get("recommended_for", []):
            reasons.append(f"Recommended for {task_type} tasks")

        if skill_metrics.get("performance_trend") == "improving":
            reasons.append("Showing improving performance trend")

        if scores["avg_quality"] >= 85:
            reasons.append(
    f"Associated with high-quality outcomes ({scores['avg_quality']:.1f})",
)

        return "; ".join(reasons) if reasons else "Based on pattern analysis"

    def update_pattern_reuse(
    self,
    pattern_id: str,
    success: bool,
    adaptation_notes: Optional[str] = None) -> bool:,
)
        """
        Update pattern reuse analytics.

        Args:
            pattern_id: ID of the reused pattern
            success: Whether the reuse was successful
            adaptation_notes: Notes about adaptations made

        Returns:
            True if pattern was found and updated
        """
        patterns_db = self._read_enhanced_patterns()

        for pattern in patterns_db["patterns"]:
            if pattern["pattern_id"] == pattern_id:
                reuse = pattern["reuse_analytics"]
                reuse["reuse_count"] += 1
                reuse["last_reused"] = datetime.now().isoformat()

                # Update success rate
                current_rate = reuse["reuse_success_rate"]
                current_count = reuse["reuse_count"]

                if success:
                    reuse["reuse_success_rate"] = (current_rate * (current_count - 1) + 1.0) / current_count
                    reuse["confidence_boost"] = min(1.0, reuse["confidence_boost"] + 0.1)
                else:
                    reuse["reuse_success_rate"] = (current_rate * (current_count - 1)) / current_count
                    reuse["confidence_boost"] = max(0.0, reuse["confidence_boost"] - 0.05)

                if adaptation_notes:
                    reuse["adaptation_notes"].append({
                        "timestamp": datetime.now().isoformat(),
                        "notes": adaptation_notes,
                        "successful": success
                    })

                self._write_enhanced_patterns(patterns_db)
                return True

        return False

    def get_learning_analytics(self) -> Dict[str, Any]:
        """
        Get comprehensive learning analytics.

        Returns:
            Dictionary containing learning metrics and insights
        """
        patterns_db = self._read_enhanced_patterns()
        skills_db = self._read_skill_metrics()
        agents_db = self._read_agent_metrics()
        cross_project_db = self._read_cross_project_patterns()

        # Pattern analytics
        total_patterns = len(patterns_db["patterns"])
        if total_patterns == 0:
            return {"status": "no_data", "message": "No patterns found"}

        # Quality trends
        recent_patterns = sorted(patterns_db["patterns"], key=lambda x: x["timestamp"], reverse=True)[:50]
        older_patterns = sorted(patterns_db["patterns"], key=lambda x: x["timestamp"], reverse=True)[50:100]

        recent_avg_quality = sum(p["outcome"]["quality_score"] for p in 
            recent_patterns) / len(recent_patterns)
        older_avg_quality = sum(p["outcome"]["quality_score"] for p in older_patterns) / len(older_patterns) if 
            
            older_patterns else recent_avg_quality

        quality_trend = "improving" if recent_avg_quality > older_avg_quality + 2 else "declining" if recent_avg_quality < older_avg_quality - 2 else "stable"

        # Success rate by task type
        task_type_stats = {}
        for pattern in patterns_db["patterns"]:
            task_type = pattern["task_classification"]["type"]
            if task_type not in task_type_stats:
                task_type_stats[task_type] = {"successes": 0, "total": 0}

            task_type_stats[task_type]["total"] += 1
            if pattern["outcome"]["success"]:
                task_type_stats[task_type]["successes"] += 1

        # Skill effectiveness
        top_skills = sorted(
            [(
    name,
    metrics.get("success_rate", 0),
    metrics.get("avg_quality_contribution", 0),
)
             for name, metrics in skills_db.items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]

        # Agent performance
        top_agents = sorted(
            [(
    name,
    metrics.get("reliability_score", 0),
    metrics.get("efficiency_rating", 0),
)
             for name, metrics in agents_db.items()],
            key=lambda x: x[1],
            reverse=True
        )[:5]

        # Learning velocity (patterns per week)
        patterns_by_week = {}
        for pattern in patterns_db["patterns"]:
            week = datetime.fromisoformat(pattern["timestamp"]).strftime("%Y-W%U")
            patterns_by_week[week] = patterns_by_week.get(week, 0) + 1

        recent_weeks = sorted(patterns_by_week.keys())[-8:]  # Last 8 weeks
        avg_patterns_per_week = sum(patterns_by_week[week] for week in recent_weeks) / len(recent_weeks) if 
            
            recent_weeks else 0

        # Prediction accuracy
        predictions_with_outcomes = [
            p for p in patterns_db["patterns"]
            if p.get("prediction_data", {}).get("predicted_quality", 0) > 0
        ]

        prediction_accuracy = 0.0
        if predictions_with_outcomes:
            accuracies = []
            for pattern in predictions_with_outcomes:
                predicted = pattern["prediction_data"]["predicted_quality"]
                actual = pattern["outcome"]["quality_score"]
                accuracy = 1.0 - abs(predicted - actual) / 100  # Accuracy as percentage
                accuracies.append(max(0.0, accuracy))

            prediction_accuracy = sum(accuracies) / len(accuracies)

        return {
            "overview": {
                "total_patterns": total_patterns,
                "learning_effectiveness": patterns_db["metadata"].get(
    "learning_effectiveness",
    0.0),,
)
                "prediction_accuracy": prediction_accuracy,
                "patterns_per_week": avg_patterns_per_week
            },
            "quality_metrics": {
                "current_average": recent_avg_quality,
                "trend": quality_trend,
                "trend_magnitude": abs(recent_avg_quality - older_avg_quality)
            },
            "task_type_effectiveness": {
                task_type: {
                    "success_rate": stats["successes"] / stats["total"],
                    "total_tasks": stats["total"]
                }
                for task_type, stats in task_type_stats.items()
            },
            "top_skills": [
                {
                    "name": name,
                    "success_rate": rate,
                    "avg_quality": quality,
                    "confidence": skills_db[name].get("confidence_score", 0.5),
                    "trend": skills_db[name].get("performance_trend", "stable")
                }
                for name, rate, quality in top_skills
            ],
            "top_agents": [
                {
                    "name": name,
                    "reliability": reliability,
                    "efficiency": efficiency,
                    "success_rate": agents_db[name].get("success_rate", 0.5),
                    "trend": agents_db[name].get("performance_trend", "stable")
                }
                for name, reliability, efficiency in top_agents
            ],
            "cross_project_learning": {
                "universal_patterns": len(cross_project_db["universal_patterns"]),
                "transferability_score": sum(p["effectiveness_metrics"]["context_transferability"]
                                           for p in cross_project_db["universal_patterns"]) / max(
)
    1,
    len(cross_project_db["universal_patterns"]),
)
            },
            "insights": self._generate_learning_insights(
    patterns_db,
    skills_db,
    agents_db,
)
        }

    def _generate_learning_insights(
    self,
    patterns_db: Dict,
    skills_db: Dict,
    agents_db: Dict) -> List[str]:,
)
        """Generate actionable insights from learning data."""
        insights = []

        # Quality insights
        patterns = patterns_db["patterns"]
        if patterns:
            high_quality_patterns = [p for p in patterns if 
                p["outcome"]["quality_score"] >= 90]
            if len(high_quality_patterns) / len(patterns) > 0.3:
                insights.append(
    "Strong quality performance - 30%+ patterns achieving 90+ quality scores",
)

            # Skill combination insights
            skill_combos = {}
            for pattern in high_quality_patterns:
                combo = tuple(sorted(pattern["execution"]["skills_loaded"]))
                skill_combos[combo] = skill_combos.get(combo, 0) + 1

            if skill_combos:
                best_combo = max(skill_combos.items(), key=lambda x: x[1])
                if best_combo[1] >= 3:
                    insights.append(
    f"High-performing skill combination: {',
    '.join(best_combo[0])} (used in {best_combo[1]} successful patterns)",
)

        # Skill insights
        improving_skills = [name for name, metrics in skills_db.items()
                          if metrics.get(
    "performance_trend") == "improving" and metrics.get("total_uses",
    0) >= 5],
)

        if improving_skills:
            insights.append(
    f"Skills showing improvement: {',
    '.join(improving_skills[:3])}",
)

        # Agent insights
        reliable_agents = [name for name, metrics in agents_db.items()
                         if metrics.get(
    "reliability_score",
    0) >= 0.9 and metrics.get("total_delegations",
    0) >= 3],
)

        if reliable_agents:
            insights.append(f"Highly reliable agents: {', '.join(reliable_agents)}")

        # Learning velocity insights
        recent_patterns = [p for p in patterns if 
            datetime.fromisoformat(p["timestamp"]) > datetime.now() - timedelta(days=7)]
        if len(recent_patterns) > 20:
            insights.append(
    "High learning velocity - 20+ patterns captured in last week",
)
        elif len(recent_patterns) < 5:
            insights.append(
    "Low learning activity - consider increasing pattern capture frequency",
)

        return insights

    def find_similar_patterns(
    self,
    task_context: Dict[str,
    Any],
    limit: int = 5) -> List[Dict[str, Any]]:,
)
        """
        Find patterns similar to the given task context.

        Args:
            task_context: Task context dictionary
            limit: Maximum number of patterns to return

        Returns:
            List of similar patterns with similarity scores
        """
        patterns_db = self._read_enhanced_patterns()
        cross_project_db = self._read_cross_project_patterns()

        project_context = task_context.get("project_context", {})
        task_type = task_context.get("task_type", "unknown")

        similar_patterns = []

        # Find similar local patterns
        for pattern in patterns_db["patterns"]:
            if pattern["task_classification"]["type"] != task_type:
                continue

            similarity = self.calculate_context_similarity(project_context, pattern["context"])

            if similarity >= 0.3:  # Minimum similarity threshold
                similar_patterns.append({
                    "pattern": pattern,
                    "similarity_score": similarity,
                    "source": "local",
                    "reuse_success_rate": pattern["reuse_analytics"]["reuse_success_rate"],
                    "quality_score": pattern["outcome"]["quality_score"]
                })

        # Add cross-project patterns if needed
        if len(similar_patterns) < limit:
            for pattern in cross_project_db["universal_patterns"]:
                if pattern["task_classification"]["type"] != task_type:
                    continue

                # Simple similarity for cross-project
                similarity = 0.0
                if 
                    pattern["context_categories"]["project_type"] == 
                        project_context.get("project_type"):
                    similarity += 0.4
                if set(
    pattern["context_categories"]["languages"]) & set(
    project_context.get("languages", [])):,,
)
)
                    similarity += 0.3
                if set(
    pattern["context_categories"]["frameworks"]) & set(
    project_context.get("frameworks", [])):,,
)
)
                    similarity += 0.3

                if similarity >= 0.4:
                    similar_patterns.append({
                        "pattern": pattern,
                        "similarity_score": similarity,
                        "source": "cross_project",
                        "reuse_success_rate": 1.0,  # Default for cross-project
                        "quality_score": pattern["outcome"]["quality_score"]
                    })

        # Sort by similarity, then by quality and reuse success
        similar_patterns.sort(
            key=lambda x: (x["similarity_score"], x["quality_score"], x["reuse_success_rate"]),
            reverse=True
        )

        return similar_patterns[:limit]


def main():
    """Command-line interface for enhanced learning engine."""
    parser = argparse.ArgumentParser(description='Enhanced Learning Engine')
    parser.add_argument(
    '--dir',
    default='.claude-patterns',
    help='Patterns directory path',
)

    subparsers = parser.add_subparsers(dest='action', help='Action to perform')

    # Capture pattern action
    capture_parser = subparsers.add_parser('capture', help='Capture an enhanced pattern')
    capture_parser.add_argument('--pattern', required=True, help='Pattern JSON string')

    # Predict skills action
    predict_parser = subparsers.add_parser('predict', help='Predict optimal skills')
    predict_parser.add_argument(
    '--context',
    required=True,
    help='Task context JSON string',
)
    predict_parser.add_argument(
    '--limit',
    type=int,
    default=5,
    help='Maximum recommendations',
)

    # Find similar patterns action
    find_parser = subparsers.add_parser('find-similar', help='Find similar patterns')
    find_parser.add_argument(
    '--context',
    required=True,
    help='Task context JSON string',
)
    find_parser.add_argument('--limit', type=int, default=5, help='Maximum results')

    # Update reuse action
    update_parser = subparsers.add_parser('update-reuse', help='Update pattern reuse analytics')
    update_parser.add_argument('--pattern-id', required=True, help='Pattern ID')
    update_parser.add_argument(
    '--success',
    action='store_true',
    help='Mark as successful reuse',
)
    update_parser.add_argument(
    '--failure',
    dest='success',
    action='store_false',
    help='Mark as failed reuse',
)
    update_parser.add_argument('--notes', help='Adaptation notes')

    # Analytics action
    subparsers.add_parser('analytics', help='Show learning analytics')

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    engine = EnhancedLearningEngine(args.dir)

    try:
        if args.action == 'capture':
            pattern_data = json.loads(args.pattern)
            pattern_id = engine.capture_enhanced_pattern(pattern_data)
            print(json.dumps({'success': True, 'pattern_id': pattern_id}, indent=2))

        elif args.action == 'predict':
            context = json.loads(args.context)
            predictions = engine.predict_optimal_skills(context, args.limit)
            print(json.dumps(predictions, indent=2))

        elif args.action == 'find-similar':
            context = json.loads(args.context)
            similar = engine.find_similar_patterns(context, args.limit)
            print(json.dumps(similar, indent=2))

        elif args.action == 'update-reuse':
            success = engine.update_pattern_reuse(args.pattern_id, args.success, args.notes)
            print(json.dumps({'success': success}, indent=2))

        elif args.action == 'analytics':
            analytics = engine.get_learning_analytics()
            print(json.dumps(analytics, indent=2))

    except Exception as e:
        print(
    json.dumps({'success': False, 'error': str(e)}, indent=2),
    file=sys.stderr,
)
        sys.exit(1)


if __name__ == '__main__':
    main()
