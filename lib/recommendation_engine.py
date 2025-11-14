#!/usr/bin/env python3
"""
Smart Recommendation Engine for Autonomous Agent Plugin

Provides intelligent workflow and optimization recommendations based on learned patterns.
Lightweight alternative to complex agent delegation system.

Features:
- Pattern-based skill recommendations
- Success rate calculations
- Quality predictions
- Risk assessment
- Confidence scoring

Version: 1.0.0
Compatible with: v7.6.9+ architecture
"""

import json
import argparse
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict, Counter

# Import pattern storage
try:
    from pattern_storage import PatternStorage
except ImportError:
    print("Error: Could not import pattern_storage.py", file=sys.stderr)
    sys.exit(1)


class RecommendationEngine:
    """Lightweight recommendation engine using existing pattern data."""

    def __init__(self, patterns_dir: str = ".claude-patterns"):
        """Initialize recommendation engine."""
        self.storage = PatternStorage(patterns_dir)

    def analyze_task(self, task_description: str) -> Dict[str, Any]:
        """
        Enhanced task analysis with sophisticated classification and context detection.

        Args:
            task_description: User's task description

        Returns:
            Enhanced task analysis dictionary
        """
        if not task_description:
            return {
                "type": "general",
                "complexity": "medium",
                "keywords": [],
                "original": "",
                "domain": "general",
                "urgency": "normal",
                "specificity_score": 0,
            }

        # Extract keywords and normalize
        keywords = re.findall(r"\b\w+\b", task_description.lower())

        # Enhanced task type classification with scoring
        task_type_scores = {
            "security-authentication": ["auth", "login", "jwt", "token", "password", "session", "oauth", "2fa"],
            "feature-implementation": ["implement", "add", "create", "build", "feature", "functionality"],
            "bugfix": ["bug", "fix", "error", "issue", "crash", "broken", "failing", "exception"],
            "refactoring": ["refactor", "restructure", "reorganize", "clean", "optimize", "improve"],
            "testing": ["test", "testing", "spec", "coverage", "unit", "integration", "e2e"],
            "documentation": ["docs", "documentation", "readme", "guide", "manual", "wiki"],
            "performance": ["performance", "speed", "optimize", "memory", "cpu", "slow", "fast"],
            "database": ["database", "db", "sql", "query", "migration", "schema", "model"],
            "api": ["api", "endpoint", "rest", "graphql", "service", "controller", "route"],
            "ui-frontend": ["ui", "frontend", "component", "interface", "user", "design", "css"],
            "deployment": ["deploy", "deployment", "production", "staging", "release", "ci/cd"],
            "analysis": ["analyze", "analysis", "review", "audit", "investigate", "research"],
        }

        # Score each task type
        type_scores = {}
        for task_type, type_keywords in task_type_scores.items():
            score = sum(2 for keyword in keywords if keyword in type_keywords)
            # Bonus for exact phrase matches
            if any(type_keyword in task_description.lower() for type_keyword in type_keywords):
                score += 1
            type_scores[task_type] = score

        # Select highest scoring type
        task_type = max(type_scores.items(), key=lambda x: x[1])
        if task_type[1] == 0:
            task_type = ("general", 0)

        task_type = task_type[0]

        # Complexity analysis with multiple factors
        complexity_indicators = {
            "high": {
                "keywords": ["implement", "create", "build", "architecture", "system", "complex", "multiple"],
                "patterns": [r"\b(from\s+scratch|new\s+system|complete\s+rewrite|architecture)\b"],
                "weight": 3,
            },
            "medium-high": {
                "keywords": ["integrate", "migrate", "refactor", "optimize", "enhance"],
                "patterns": [r"\b(significant|major|substantial)\b"],
                "weight": 2,
            },
            "medium": {"keywords": ["update", "modify", "improve", "add", "extend"], "patterns": [], "weight": 1},
            "low": {
                "keywords": ["fix", "simple", "minor", "quick", "small", "trivial"],
                "patterns": [r"\b(just|simply|only|quick\s+fix)\b"],
                "weight": 0.5,
            },
        }

        complexity_score = 1  # Default to medium
        for level, indicators in complexity_indicators.items():
            score = 0
            # Keyword matching
            for keyword in indicators["keywords"]:
                if keyword in keywords:
                    score += indicators["weight"]
            # Pattern matching
            for pattern in indicators["patterns"]:
                if re.search(pattern, task_description.lower()):
                    score += indicators["weight"] * 1.5

            if score > complexity_score:
                complexity_score = score
                complexity = level

        # Domain detection
        domain_keywords = {
            "web": ["web", "website", "frontend", "backend", "http", "html", "css", "javascript"],
            "mobile": ["mobile", "ios", "android", "app", "react-native", "flutter"],
            "data": ["data", "analytics", "ml", "ai", "machine learning", "statistics"],
            "devops": ["deploy", "ci", "cd", "docker", "kubernetes", "infrastructure"],
            "security": ["security", "auth", "encryption", "vulnerability", "penetration"],
        }

        domain = "general"
        for d, d_keywords in domain_keywords.items():
            if any(keyword in keywords for keyword in d_keywords):
                domain = d
                break

        # Urgency detection
        urgency_keywords = {
            "urgent": ["urgent", "critical", "asap", "immediately", "emergency", "blocking"],
            "high": ["high", "priority", "soon", "quickly"],
            "normal": [],  # default
            "low": ["low", "when", "time", "eventually", "sometime"],
        }

        urgency = "normal"
        for u_level, u_keywords in urgency_keywords.items():
            if any(keyword in keywords for keyword in u_keywords):
                urgency = u_level
                break

        # Specificity score (how detailed the task description is)
        specificity_score = min(len(keywords) / 10, 1.0)  # 0-1 scale
        if any(qualifier in task_description.lower() for qualifier in ["etc", "and more", "various", "multiple"]):
            specificity_score *= 0.8  # Reduce for vague descriptions

        # Extract specific terms (filter out common words)
        common_words = {"the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "a", "an"}
        key_terms = [word for word in keywords if word not in common_words and len(word) > 2][:8]

        return {
            "type": task_type,
            "complexity": complexity,
            "keywords": keywords,
            "key_terms": key_terms,
            "original": task_description,
            "domain": domain,
            "urgency": urgency,
            "specificity_score": round(specificity_score, 2),
            "confidence_scores": type_scores,
        }

    def get_pattern_recommendations(self, task_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get recommendations based on similar patterns.

        Args:
            task_analysis: Task analysis dictionary

        Returns:
            List of pattern-based recommendations
        """
        # Search for similar patterns
        patterns = self.storage.get_similar_patterns(
            task_type=task_analysis["type"], context={"keywords": task_analysis["keywords"]}, limit=5
        )

        recommendations = []
        for pattern in patterns:
            # Calculate recommendation score
            score = self._calculate_recommendation_score(pattern, task_analysis)

            recommendations.append(
                {
                    "pattern_id": pattern.get("id", "unknown"),
                    "quality_score": pattern.get("quality_score", 0),
                    "success_rate": pattern.get("success_rate", 0),
                    "skills_used": pattern.get("skills_used", []),
                    "agents_delegated": pattern.get("agents_delegated", []),
                    "execution_time": pattern.get("execution_time", 0),
                    "recommendation_score": score,
                    "reuse_count": pattern.get("reuse_count", 0),
                }
            )

        # Sort by recommendation score
        recommendations.sort(key=lambda x: x["recommendation_score"], reverse=True)
        return recommendations

    def _calculate_recommendation_score(self, pattern: Dict[str, Any], task_analysis: Dict[str, Any]) -> float:
        """Calculate recommendation score for a pattern."""
        score = 0.0

        # Quality score contribution (30%)
        quality = pattern.get("quality_score", 0)
        score += (quality / 100) * 0.3

        # Success rate contribution (25%)
        success_rate = pattern.get("success_rate", 0)
        score += (success_rate / 100) * 0.25

        # Reuse count contribution (20%)
        reuse_count = pattern.get("reuse_count", 0)
        score += min(reuse_count / 10, 1.0) * 0.2

        # Execution time (15%) - faster is better
        exec_time = pattern.get("execution_time", 60)
        if exec_time > 0:
            time_score = max(0, 1 - (exec_time / 3600))  # 1 hour = 0 score
            score += time_score * 0.15

        # Skill diversity (10%)
        skills = pattern.get("skills_used", [])
        if skills:
            diversity_score = min(len(skills) / 5, 1.0)
            score += diversity_score * 0.1

        return score

    def generate_intelligent_skill_recommendations(
        self, task_analysis: Dict[str, Any], pattern_recommendations: List[Dict[str, Any]]
    )-> Dict[str, Any]:
        """Generate Intelligent Skill Recommendations."""
        """
        Generate intelligent skill recommendations based on task analysis and patterns.

        Args:
            task_analysis: Enhanced task analysis results
            pattern_recommendations: Pattern-based recommendations

        Returns:
            Comprehensive skill recommendations with reasoning
        """
        task_type = task_analysis["type"]
        complexity = task_analysis["complexity"]
        domain = task_analysis["domain"]
        urgency = task_analysis["urgency"]

        # Base skill mappings by task type and domain
        skill_mappings = {
            "security-authentication": {
                "core": ["security-patterns", "code-analysis", "testing-strategies"],
                "enhanced": ["quality-standards", "pattern-learning"],
                "domain_specific": [],
            },
            "feature-implementation": {
                "core": ["code-analysis", "pattern-learning", "quality-standards"],
                "enhanced": ["testing-strategies", "documentation-best-practices"],
                "domain_specific": [],
            },
            "bugfix": {
                "core": ["code-analysis", "testing-strategies", "quality-standards"],
                "enhanced": ["pattern-learning"],
                "domain_specific": [],
            },
            "refactoring": {
                "core": ["code-analysis", "quality-standards", "pattern-learning"],
                "enhanced": ["testing-strategies"],
                "domain_specific": [],
            },
            "testing": {
                "core": ["testing-strategies", "code-analysis"],
                "enhanced": ["quality-standards", "pattern-learning"],
                "domain_specific": [],
            },
            "performance": {
                "core": ["performance-scaling", "code-analysis", "pattern-learning"],
                "enhanced": ["quality-standards"],
                "domain_specific": [],
            },
            "api": {
                "core": ["code-analysis", "quality-standards", "testing-strategies"],
                "enhanced": ["pattern-learning"],
                "domain_specific": [],
            },
            "database": {
                "core": ["code-analysis", "quality-standards"],
                "enhanced": ["pattern-learning", "testing-strategies"],
                "domain_specific": [],
            },
            "ui-frontend": {
                "core": ["code-analysis", "quality-standards"],
                "enhanced": ["pattern-learning", "testing-strategies"],
                "domain_specific": [],
            },
            "deployment": {
                "core": ["quality-standards", "code-analysis"],
                "enhanced": ["pattern-learning", "testing-strategies"],
                "domain_specific": [],
            },
        }

        # Domain-specific skill additions
        domain_skills = {
            "web": ["web-validation", "api-contract-validator"],
            "mobile": ["mobile-validation", "testing-strategies"],
            "data": ["data-validation", "performance-scaling"],
            "devops": ["deployment-validation", "quality-standards"],
            "security": ["security-patterns", "testing-strategies"],
        }

        # Get base skills for task type
        base_skills = skill_mappings.get(task_type, skill_mappings["feature-implementation"])
        recommended_skills = []

        # Add core skills
        for skill in base_skills["core"]:
            recommended_skills.append(
                {"skill": skill, "priority": "HIGH", "reasoning": f"Core skill for {task_type} tasks", "confidence": 90}
            )

        # Add enhanced skills based on complexity
        if complexity in ["high", "medium-high"]:
            for skill in base_skills["enhanced"]:
                recommended_skills.append(
                    {
                        "skill": skill,
                        "priority": "MEDIUM",
                        "reasoning": f"Enhanced skill for high-complexity {task_type}",
                        "confidence": 80,
                    }
                )

        # Add domain-specific skills
        if domain in domain_skills:
            for skill in domain_skills[domain]:
                recommended_skills.append(
                    {
                        "skill": skill,
                        "priority": "MEDIUM",
                        "reasoning": f"Domain-specific skill for {domain} projects",
                        "confidence": 75,
                    }
                )

        # Add urgency-based skills
        if urgency in ["urgent", "high"]:
            recommended_skills.append(
                {
                    "skill": "validation-standards",
                    "priority": "HIGH",
                    "reasoning": "Critical for urgent tasks to prevent regressions",
                    "confidence": 85,
                }
            )

        # Incorporate pattern-based insights
        if pattern_recommendations:
            # Get skills from successful patterns
            successful_skills = []
            for pattern in pattern_recommendations:
                if pattern["success_rate"] >= 85:
                    successful_skills.extend(pattern["skills_used"])

            # Skill frequency analysis from patterns
            skill_frequency = {}
            for skill in successful_skills:
                skill_frequency[skill] = skill_frequency.get(skill, 0) + 1

            # Boost confidence for frequently successful skills
            for skill_rec in recommended_skills:
                skill_name = skill_rec["skill"]
                if skill_name in skill_frequency:
                    frequency_boost = min(skill_frequency[skill_name] * 5, 15)
                    skill_rec["confidence"] = min(95, skill_rec["confidence"] + frequency_boost)
                    skill_rec["reasoning"] += f" (proven in {skill_frequency[skill_name]} successful patterns)"

        # Add pattern-discovered skills not in base recommendations
        all_base_skills = [rec["skill"] for rec in recommended_skills]
        for pattern in pattern_recommendations:
            for skill in pattern["skills_used"]:
                if skill not in all_base_skills and pattern["success_rate"] >= 80:
                    recommended_skills.append(
                        {
                            "skill": skill,
                            "priority": "LOW",
                            "reasoning": f"Skill from successful pattern (quality: {pattern['quality_score']})",
                            "confidence": 70,
                        }
                    )

        # Sort by priority and confidence
        priority_order = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
        recommended_skills.sort(key=lambda x: (priority_order.get(x["priority"], 0), x["confidence"]), reverse=True)

        # Limit to top 8 skills
        recommended_skills = recommended_skills[:8]

        # Generate summary
        summary = {
            "total_skills": len(recommended_skills),
            "high_priority": len([s for s in recommended_skills if s["priority"] == "HIGH"]),
            "medium_priority": len([s for s in recommended_skills if s["priority"] == "MEDIUM"]),
            "low_priority": len([s for s in recommended_skills if s["priority"] == "LOW"]),
            "avg_confidence": (
                round(sum(s["confidence"] for s in recommended_skills) / len(recommended_skills), 1)
                if recommended_skills
                else 0
            ),
            "pattern_informed": len(pattern_recommendations) > 0,
        }

        return {
            "skills": recommended_skills,
            "summary": summary,
            "reasoning": f"Based on {task_type} task with {complexity} complexity in {domain} domain",
        }

    def assess_enhanced_risks(
        self,
        task_analysis: Dict[str, Any],
        pattern_recommendations: List[Dict[str, Any]],
        skill_recommendations: Dict[str, Any],
    )-> Dict[str, Any]:
        """Assess Enhanced Risks."""
        """
        Enhanced risk assessment with comprehensive analysis.

        Args:
            task_analysis: Enhanced task analysis results
            pattern_recommendations: Pattern-based recommendations
            skill_recommendations: Skill recommendation results

        Returns:
            Comprehensive risk assessment with actionable mitigations
        """
        risks = []
        risk_score = 0
        mitigations = []

        task_type = task_analysis["type"]
        complexity = task_analysis["complexity"]
        domain = task_analysis["domain"]
        urgency = task_analysis["urgency"]
        specificity = task_analysis["specificity_score"]

        # 1. COMPLEXITY RISKS
        if complexity == "high":
            risks.append(
                {
                    "category": "COMPLEXITY",
                    "level": "HIGH",
                    "description": "High complexity task with multiple interdependencies",
                    "impact": "May require 2-3x more time than estimated",
                    "mitigation": "Break into 3-5 smaller, manageable sub-tasks",
                    "time_adjustment": "+15-25 minutes",
                    "quality_adjustment": "-5-8 points",
                }
            )
            risk_score += 35
            mitigations.append("Create sub-task breakdown before starting")
        elif complexity == "medium-high":
            risks.append(
                {
                    "category": "COMPLEXITY",
                    "level": "MEDIUM",
                    "description": "Medium-high complexity with some challenges",
                    "impact": "May require additional testing and validation",
                    "mitigation": "Plan extra validation steps",
                    "time_adjustment": "+8-12 minutes",
                    "quality_adjustment": "-3-5 points",
                }
            )
            risk_score += 20
            mitigations.append("Add comprehensive testing")

        # 2. PATTERN DATA RISKS
        if not pattern_recommendations:
            risks.append(
                {
                    "category": "KNOWLEDGE",
                    "level": "HIGH",
                    "description": "No similar patterns found in learning database",
                    "impact": "No historical guidance available",
                    "mitigation": "Use comprehensive approach with all recommended skills",
                    "time_adjustment": "+10-15 minutes",
                    "quality_adjustment": "-5-7 points",
                }
            )
            risk_score += 40
            mitigations.append("Proceed with full skill set and extra validation")
        elif len(pattern_recommendations) < 2:
            risks.append(
                {
                    "category": "KNOWLEDGE",
                    "level": "MEDIUM",
                    "description": "Limited pattern data available",
                    "impact": "Lower confidence in recommendations",
                    "mitigation": "Validate results frequently during execution",
                    "time_adjustment": "+5-8 minutes",
                    "quality_adjustment": "-2-4 points",
                }
            )
            risk_score += 25
            mitigations.append("Frequent validation checkpoints")

        # 3. TASK TYPE-SPECIFIC RISKS
        if task_type == "security-authentication":
            risks.append(
                {
                    "category": "SECURITY",
                    "level": "HIGH",
                    "description": "Security-critical authentication implementation",
                    "impact": "Security vulnerabilities could have severe consequences",
                    "mitigation": "Use security-patterns skill, conduct thorough testing",
                    "time_adjustment": "+12-18 minutes",
                    "quality_adjustment": "N/A (security threshold is absolute)",
                }
            )
            risk_score += 30
            mitigations.append("Mandatory security review before deployment")
        elif task_type == "performance":
            risks.append(
                {
                    "category": "PERFORMANCE",
                    "level": "MEDIUM",
                    "description": "Performance optimization may have unintended side effects",
                    "impact": "Could introduce new bugs or regressions",
                    "mitigation": "Benchmark before and after, comprehensive regression testing",
                    "time_adjustment": "+10-15 minutes",
                    "quality_adjustment": "-3-5 points if not tested",
                }
            )
            risk_score += 20
            mitigations.append("Performance benchmarking and regression testing")
        elif task_type == "database":
            risks.append(
                {
                    "category": "DATA_INTEGRITY",
                    "level": "HIGH",
                    "description": "Database changes risk data corruption or loss",
                    "impact": "Potential data loss or corruption",
                    "mitigation": "Backup data, test on non-production environment first",
                    "time_adjustment": "+15-20 minutes",
                    "quality_adjustment": "Critical - must ensure data integrity",
                }
            )
            risk_score += 35
            mitigations.append("Database backup and isolated testing environment")

        # 4. URGENCY RISKS
        if urgency == "urgent":
            risks.append(
                {
                    "category": "TIME_PRESSURE",
                    "level": "HIGH",
                    "description": "Urgent timeline increases risk of errors",
                    "impact": "Higher likelihood of mistakes or oversights",
                    "mitigation": "Prioritize critical testing, consider phased approach",
                    "time_adjustment": "Time pressure already accounted for",
                    "quality_adjustment": "-8-12 points",
                }
            )
            risk_score += 30
            mitigations.append("Focus on critical path testing only")
        elif urgency == "high":
            risks.append(
                {
                    "category": "TIME_PRESSURE",
                    "level": "MEDIUM",
                    "description": "High priority may require compromises",
                    "impact": "May need to skip some validation steps",
                    "mitigation": "Maintain essential quality gates",
                    "time_adjustment": "+5 minutes",
                    "quality_adjustment": "-4-6 points",
                }
            )
            risk_score += 15
            mitigations.append("Maintain minimum quality standards")

        # 5. SPECIFICITY RISKS
        if specificity < 0.3:
            risks.append(
                {
                    "category": "CLARITY",
                    "level": "HIGH",
                    "description": "Vague task description may lead to scope creep",
                    "impact": "Task may expand beyond initial scope",
                    "mitigation": "Clarify requirements before starting, define acceptance criteria",
                    "time_adjustment": "+8-12 minutes for clarification",
                    "quality_adjustment": "-5-7 points",
                }
            )
            risk_score += 25
            mitigations.append("Requirements clarification before implementation")
        elif specificity < 0.6:
            risks.append(
                {
                    "category": "CLARITY",
                    "level": "MEDIUM",
                    "description": "Some ambiguity in task requirements",
                    "impact": "May need clarification during implementation",
                    "mitigation": "Define specific success criteria",
                    "time_adjustment": "+3-5 minutes",
                    "quality_adjustment": "-2-4 points",
                }
            )
            risk_score += 15
            mitigations.append("Define clear success criteria")

        # 6. DOMAIN-SPECIFIC RISKS
        domain_risks = {
            "security": {
                "level": "HIGH",
                "description": "Security domain requires extra validation",
                "mitigation": "Security audit, penetration testing if critical",
                "time_adjustment": "+10-15 minutes",
            },
            "devops": {
                "level": "MEDIUM",
                "description": "DevOps changes affect production infrastructure",
                "mitigation": "Staging environment testing, rollback plan",
                "time_adjustment": "+8-12 minutes",
            },
        }

        if domain in domain_risks:
            domain_risk = domain_risks[domain]
            risks.append(
                {
                    "category": "DOMAIN",
                    "level": domain_risk["level"],
                    "description": domain_risk["description"],
                    "impact": "Domain-specific considerations required",
                    "mitigation": domain_risk["mitigation"],
                    "time_adjustment": domain_risk["time_adjustment"],
                    "quality_adjustment": "-3-5 points",
                }
            )
            risk_score += 20 if domain_risk["level"] == "HIGH" else 10
            mitigations.append(domain_risk["mitigation"])

        # 7. SKILL AVAILABILITY RISKS
        skill_summary = skill_recommendations.get("summary", {})
        if skill_summary.get("avg_confidence", 0) < 75:
            risks.append(
                {
                    "category": "RESOURCES",
                    "level": "MEDIUM",
                    "description": "Lower confidence in recommended skill effectiveness",
                    "impact": "Skills may not perform as expected",
                    "mitigation": "Monitor skill performance closely, have alternatives ready",
                    "time_adjustment": "+5-8 minutes",
                    "quality_adjustment": "-4-6 points",
                }
            )
            risk_score += 15
            mitigations.append("Monitor skill effectiveness and adjust as needed")

        # Determine overall risk level
        if risk_score >= 60:
            risk_level = "CRITICAL"
            color = "RED"
        elif risk_score >= 40:
            risk_level = "HIGH"
            color = "ORANGE"
        elif risk_score >= 20:
            risk_level = "MEDIUM"
            color = "YELLOW"
        else:
            risk_level = "LOW"
            color = "GREEN"

        # Calculate adjusted estimates
        total_time_adjustment = sum(
            int(r.get("time_adjustment", "0").split("+")[-1].split("-")[0])
            for r in risks
            if "+" in r.get("time_adjustment", "")
        )
        quality_impact = sum(
            int(r.get("quality_adjustment", "0").split("-")[-1].split(" ")[0])
            for r in risks
            if "-" in r.get("quality_adjustment", "")
        )

        return {
            "overall_level": risk_level,
            "overall_score": min(100, risk_score),
            "color_indicator": color,
            "total_risks": len(risks),
            "risks_by_category": {
                category: [r for r in risks if r["category"] == category] for category in set(r["category"] for r in risks)
            },
            "detailed_risks": risks,
            "primary_mitigations": mitigations[:5],  # Top 5 mitigations
            "estimated_impact": {
                "time_adjustment": f"+{total_time_adjustment} minutes",
                "quality_adjustment": f"-{quality_impact} points" if quality_impact > 0 else "No impact",
            },
            "risk_summary": f"{risk_level} risk ({risk_score}/100) with {len(risks)} identified risk factors",
        }

    def generate_enhanced_recommendations(self, task_description: str = "") -> Dict[str, Any]:
        """
        Generate enhanced, comprehensive recommendations with improved analysis.

        Args:
            task_description: User's task description

        Returns:
            Complete enhanced recommendation report
        """
        # Enhanced task analysis
        task_analysis = self.analyze_task(task_description)

        # Get pattern recommendations
        pattern_recommendations = self.get_pattern_recommendations(task_analysis)

        # Generate intelligent skill recommendations
        skill_recommendations = self.generate_intelligent_skill_recommendations(task_analysis, pattern_recommendations)

        # Enhanced risk assessment
        risk_assessment = self.assess_enhanced_risks(task_analysis, pattern_recommendations, skill_recommendations)

        # Generate enhanced predictions
        predictions = self._generate_enhanced_predictions(task_analysis, pattern_recommendations, risk_assessment)

        # Generate actionable alternatives
        alternatives = self._generate_actionable_alternatives(task_analysis, skill_recommendations, risk_assessment)

        # Calculate overall confidence and recommendations
        overall_confidence = self._calculate_overall_confidence(pattern_recommendations, risk_assessment)

        return {
            "task_analysis": task_analysis,
            "primary_recommendation": {
                "approach": "pattern-informed" if pattern_recommendations else "baseline",
                "skills": skill_recommendations["skills"][:5],  # Top 5 skills
                "predictions": predictions,
                "confidence": overall_confidence,
                "reasoning": skill_recommendations.get("reasoning", "Based on task analysis"),
            },
            "skill_recommendations": skill_recommendations,
            "risk_assessment": risk_assessment,
            "pattern_insights": {
                "similar_patterns_found": len(pattern_recommendations),
                "best_pattern_quality": max([p["quality_score"] for p in pattern_recommendations], default=0),
                "avg_success_rate": (
                    round(sum([p["success_rate"] for p in pattern_recommendations]) / len(pattern_recommendations), 1)
                    if pattern_recommendations
                    else 0
                ),
            },
            "alternatives": alternatives,
            "action_plan": self._generate_action_plan(task_analysis, skill_recommendations, risk_assessment),
            "generated_at": datetime.now().isoformat(),
        }

    def _generate_predictions(self, recommendations: List[Dict[str, Any]], risks: Dict[str, Any]) -> Dict[str, Any]:
        """Generate quality and time predictions."""
        if not recommendations:
            return {"quality_score": 75, "confidence": 50, "estimated_time": "15-20 minutes", "success_probability": 70}

        # Use top recommendation as baseline
        top_rec = recommendations[0]
        base_quality = top_rec["quality_score"]
        base_time = top_rec["execution_time"]

        # Adjust for risks
        risk_penalty = risks["score"] * 0.1  # 10% penalty per risk point
        adjusted_quality = max(70, base_quality - risk_penalty)

        # Adjust time for complexity
        time_multiplier = 1.0
        if risks["level"] == "HIGH":
            time_multiplier = 1.3
        elif risks["level"] == "MEDIUM":
            time_multiplier = 1.15

        adjusted_time = int(base_time * time_multiplier)

        # Calculate confidence based on pattern data
        confidence = min(95, len(recommendations) * 15 + top_rec["success_rate"] * 0.5)

        return {
            "quality_score": round(adjusted_quality, 1),
            "confidence": round(confidence, 1),
            "estimated_time": f"{adjusted_time}-{int(adjusted_time * 1.2)} minutes",
            "success_probability": round(adjusted_quality * 0.9, 1),
        }

    def _generate_enhanced_predictions(
        self, task_analysis: Dict[str, Any], pattern_recommendations: List[Dict[str, Any]], risk_assessment: Dict[str, Any]
    )-> Dict[str, Any]:
        """ Generate Enhanced Predictions."""
        """Generate enhanced quality and time predictions."""
        complexity = task_analysis["complexity"]
        urgency = task_analysis["urgency"]

        # Base predictions by complexity
        base_predictions = {
            "high": {"quality": 85, "time": 30, "confidence": 75},
            "medium-high": {"quality": 82, "time": 22, "confidence": 78},
            "medium": {"quality": 80, "time": 18, "confidence": 82},
            "low": {"quality": 88, "time": 12, "confidence": 85},
        }

        base = base_predictions.get(complexity, base_predictions["medium"])

        # Adjust for pattern data
        if pattern_recommendations:
            best_pattern = max(pattern_recommendations, key=lambda x: x["quality_score"])
            base["quality"] = (base["quality"] + best_pattern["quality_score"]) / 2
            base["confidence"] = min(95, base["confidence"] + len(pattern_recommendations) * 5)

        # Adjust for risk
        risk_impact = risk_assessment.get("estimated_impact", {})
        quality_adjustment = (
            int(risk_impact.get("quality_adjustment", "0").replace(" points", "").replace("-", ""))
            if "points" in risk_impact.get("quality_adjustment", "")
            else 0
        )
        time_adjustment = (
            int(risk_impact.get("time_adjustment", "0").replace(" minutes", "").replace("+", ""))
            if "minutes" in risk_impact.get("time_adjustment", "")
            else 0
        )

        # Adjust for urgency
        urgency_adjustment = {"urgent": -10, "high": -5, "normal": 0, "low": 5}
        base["quality"] += urgency_adjustment.get(urgency, 0)

        # Final calculations
        final_quality = max(65, min(95, base["quality"] - quality_adjustment))
        final_time = max(5, base["time"] + time_adjustment)
        final_confidence = max(50, min(95, base["confidence"] - (risk_assessment.get("overall_score", 0) * 0.2)))

        return {
            "quality_score": round(final_quality, 1),
            "estimated_time": f"{final_time}-{int(final_time * 1.3)} minutes",
            "confidence": round(final_confidence, 1),
            "success_probability": round(final_quality * 0.92, 1),
            "risk_adjusted": True,
        }

    def _generate_actionable_alternatives(
        self, task_analysis: Dict[str, Any], skill_recommendations: Dict[str, Any], risk_assessment: Dict[str, Any]
    )-> List[Dict[str, Any]]:
        """ Generate Actionable Alternatives."""
        """Generate actionable alternative approaches."""
        alternatives = []
        risk_level = risk_assessment.get("overall_level", "MEDIUM")

        # Fast approach
        alternatives.append(
            {
                "name": "Fast Track",
                "description": "Quick implementation with essential skills only",
                "skills": [s["skill"] for s in skill_recommendations["skills"][:2]],  # Top 2 only
                "time_impact": "-40% time",
                "quality_impact": "-8-12 points",
                "best_for": "When time is more critical than quality",
                "confidence": max(60, skill_recommendations["summary"]["avg_confidence"] - 15),
                "risks": "Higher chance of missing edge cases",
            }
        )

        # Comprehensive approach
        all_skills = [s["skill"] for s in skill_recommendations["skills"]]
        alternatives.append(
            {
                "name": "Comprehensive",
                "description": "Thorough implementation with all recommended skills and extra validation",
                "skills": all_skills + ["quality-standards", "testing-strategies"],
                "time_impact": "+60% time",
                "quality_impact": "+8-15 points",
                "best_for": "Critical production features",
                "confidence": min(95, skill_recommendations["summary"]["avg_confidence"] + 10),
                "risks": "May be overkill for simple tasks",
            }
        )

        # Risk-focused approach
        if risk_level in ["HIGH", "CRITICAL"]:
            alternatives.append(
                {
                    "name": "Risk-Mitigated",
                    "description": "Prioritize risk reduction over speed",
                    "skills": [s["skill"] for s in skill_recommendations["skills"] if s["priority"] in ["HIGH", "MEDIUM"]],
                    "time_impact": "+25% time",
                    "quality_impact": "+5-8 points",
                    "best_for": "High-risk or security-critical tasks",
                    "confidence": min(92, skill_recommendations["summary"]["avg_confidence"] + 8),
                    "risks": "Slower but safer implementation",
                }
            )

        return alternatives

    def _calculate_overall_confidence(
        self, pattern_recommendations: List[Dict[str, Any]], risk_assessment: Dict[str, Any]
    )-> Dict[str, Any]:
        """ Calculate Overall Confidence."""
        """Calculate overall confidence in recommendations."""
        pattern_confidence = min(90, len(pattern_recommendations) * 20)  # Up to 90% from patterns
        risk_penalty = risk_assessment.get("overall_score", 0) * 0.3  # Penalty for risk

        base_confidence = pattern_confidence - risk_penalty
        final_confidence = max(50, min(95, base_confidence + 30))  # Base 30% + adjustments

        # Determine confidence level
        if final_confidence >= 85:
            level = "VERY HIGH"
            recommendation = "Proceed with confidence"
        elif final_confidence >= 75:
            level = "HIGH"
            recommendation = "Recommended approach with minor monitoring"
        elif final_confidence >= 65:
            level = "MEDIUM"
            recommendation = "Proceed with caution, validate frequently"
        else:
            level = "LOW"
            recommendation = "Consider alternatives or seek clarification"

        return {
            "score": round(final_confidence, 1),
            "level": level,
            "recommendation": recommendation,
            "based_on": f"{len(pattern_recommendations)} patterns, {risk_assessment['total_risks']} risk factors",
        }

    def _generate_action_plan(
        self, task_analysis: Dict[str, Any], skill_recommendations: Dict[str, Any], risk_assessment: Dict[str, Any]
    )-> Dict[str, Any]:
        """ Generate Action Plan."""
        """Generate actionable next steps."""
        steps = []

        # Step 1: Preparation
        if task_analysis["specificity_score"] < 0.6:
            steps.append(
                {
                    "step": 1,
                    "action": "Clarify requirements",
                    "description": "Define specific success criteria and acceptance tests",
                    "estimated_time": "5-10 minutes",
                    "priority": "HIGH",
                }
            )

        # Step 2: Skill loading
        skills = [s for s in skill_recommendations["skills"] if s["priority"] == "HIGH"]
        steps.append(
            {
                "step": len(steps) + 1,
                "action": "Load core skills",
                "description": f"Load essential skills: {', '.join([s['skill'] for s in skills[:3]])}",
                "estimated_time": "1-2 minutes",
                "priority": "HIGH",
            }
        )

        # Step 3: Risk mitigation
        primary_mitigations = risk_assessment.get("primary_mitigations", [])
        if primary_mitigations:
            steps.append(
                {
                    "step": len(steps) + 1,
                    "action": "Implement risk mitigations",
                    "description": f"Focus on: {', '.join(primary_mitigations[:2])}",
                    "estimated_time": "3-8 minutes",
                    "priority": "HIGH" if risk_assessment.get("overall_level") in ["HIGH", "CRITICAL"] else "MEDIUM",
                }
            )

        # Step 4: Execution
        steps.append(
            {
                "step": len(steps) + 1,
                "action": "Execute task implementation",
                "description": "Proceed with main implementation using recommended skills",
                "estimated_time": "Primary execution time",
                "priority": "HIGH",
            }
        )

        # Step 5: Validation
        if risk_assessment.get("overall_level") in ["HIGH", "CRITICAL"]:
            steps.append(
                {
                    "step": len(steps) + 1,
                    "action": "Comprehensive validation",
                    "description": "Thorough testing and quality checks",
                    "estimated_time": "5-10 minutes",
                    "priority": "HIGH",
                }
            )

        return {
            "total_steps": len(steps),
            "estimated_total_time": "15-45 minutes",
            "steps": steps,
            "critical_path": [s for s in steps if s["priority"] == "HIGH"],
        }

    def format_enhanced_recommendations(self, recommendations: Dict[str, Any]) -> str:
        """Format enhanced recommendations for user-friendly display."""
        task = recommendations["task_analysis"]["original"]
        task_analysis = recommendations["task_analysis"]
        primary = recommendations["primary_recommendation"]
        skills = recommendations["skill_recommendations"]
        risks = recommendations["risk_assessment"]
        patterns = recommendations["pattern_insights"]
        alternatives = recommendations["alternatives"]
        action_plan = recommendations["action_plan"]

        output = []
        output.append("=" * 70)
        output.append("  ENHANCED SMART RECOMMENDATIONS")
        output.append("=" * 70)
        output.append("")

        # Task Analysis
        output.append(f"Task: {task}")
        output.append(
            f"Classification: {task_analysis['type']} | Complexity: {task_analysis['complexity'].upper()} | Domain: {task_analysis['domain']}"
        )
        output.append(
            f"Urgency: {task_analysis['urgency'].upper()} | Specificity: {int(task_analysis['specificity_score'] * 100)}%"
        )
        output.append("")

        # Primary Recommendation
        confidence = primary["confidence"]
        output.append(f"[RECOMMENDED] APPROACH ({confidence['score']}% confidence - {confidence['level']})")
        output.append(f"Strategy: {primary['approach'].title()}")
        output.append(f"Expected Quality: {primary['predictions']['quality_score']}/100")
        output.append(f"Estimated Time: {primary['predictions']['estimated_time']}")
        output.append(f"Reasoning: {primary['reasoning']}")
        output.append("")

        # Top Skills
        output.append("[RECOMMENDED] SKILLS:")
        for i, skill in enumerate(primary["skills"][:5], 1):
            status = "[PASS]" if skill["priority"] == "HIGH" else "[WARN]"
            output.append(f"  {i}. {status} {skill['skill']} ({skill['confidence']}% confidence)")
            output.append(f"     -> {skill['reasoning']}")
        output.append("")

        # Pattern Insights
        if patterns["similar_patterns_found"] > 0:
            output.append("[PATTERN] INSIGHTS:")
            output.append(f"  Similar patterns found: {patterns['similar_patterns_found']}")
            output.append(f"  Best historical quality: {patterns['best_pattern_quality']}/100")
            output.append(f"  Average success rate: {patterns['avg_success_rate']}%")
            output.append("")

        # Risk Assessment
        risk_level = risks["overall_level"]
        risk_score = risks["overall_score"]
        output.append(f"[RISK] ASSESSMENT: {risk_level} ({risk_score}/100)")

        # Show top 3 risks
        top_risks = sorted(risks["detailed_risks"], key=lambda x: x.get("level", "LOW") == "HIGH", reverse=True)[:3]
        for risk in top_risks:
            output.append(f"  • {risk['level']}: {risk['description']}")
            output.append(f"    -> Mitigation: {risk['mitigation']}")

        if risks["estimated_impact"]["time_adjustment"] != "No impact":
            output.append(
                f"  Impact: {risks['estimated_impact']['time_adjustment']}, {risks['estimated_impact']['quality_adjustment']}"
            )
        output.append("")

        # Action Plan
        output.append(f"[ACTION] PLAN ({action_plan['total_steps']} steps):")
        for step in action_plan["steps"]:
            priority_icon = "[CRITICAL]" if step["priority"] == "HIGH" else "[STANDARD]"
            output.append(f"  {priority_icon} Step {step['step']}: {step['action']}")
            output.append(f"     -> {step['description']} (~{step['estimated_time']})")
        output.append("")

        # Alternatives
        if alternatives:
            output.append("[ALTERNATIVE] APPROACHES:")
            for i, alt in enumerate(alternatives, 2):
                output.append(f"  {i}. {alt['name']} ({alt['confidence']}% confidence)")
                output.append(f"     Impact: {alt['time_impact']}, {alt['quality_impact']}")
                output.append(f"     Best for: {alt['best_for']}")
            output.append("")

        # Final Recommendation
        if confidence["score"] >= 80:
            output.append("[SUCCESS] FINAL RECOMMENDATION: Proceed with recommended approach")
        else:
            output.append("[WARNING] FINAL RECOMMENDATION: Consider alternatives or seek clarification")

        output.append(f"[INFO] {confidence['recommendation']}")
        output.append("")
        output.append("=" * 70)

        return "\n".join(output)


def main():
    """Enhanced command line interface."""
    parser = argparse.ArgumentParser(description="Generate enhanced smart recommendations")
    parser.add_argument("--task", type=str, help="Task description", default="")
    parser.add_argument("--dir", type=str, help="Patterns directory", default=".claude-patterns")
    parser.add_argument("--format", type=str, choices=["text", "json"], default="text", help="Output format")

    args = parser.parse_args()

    # Initialize engine
    engine = RecommendationEngine(args.dir)

    # Generate enhanced recommendations
    recommendations = engine.generate_enhanced_recommendations(args.task)

    # Output results
    if args.format == "json":
        print(json.dumps(recommendations, indent=2))
    else:
        print(engine.format_enhanced_recommendations(recommendations))


def format_recommendations_text(recs: Dict[str, Any]) -> str:
    """Format recommendations as text (similar to original design)."""
    task = recs["task"]
    predictions = recs["predictions"]
    risks = recs["risks"]

    output = []
    output.append("=" * 56)
    output.append("  SMART RECOMMENDATIONS")
    output.append("=" * 56)
    output.append("")

    if task["original"]:
        output.append(f"Task: \"{task['original']}\"")
        output.append(f"Analyzed as: {task['type']}, {task['complexity']} complexity")
    else:
        output.append("Task: General analysis")
        output.append(f"Analyzed as: {task['type']}, {task['complexity']} complexity")

    output.append("")

    # Top recommendation
    if recs["recommendations"]:
        top = recs["recommendations"][0]
        output.append("+- [RECOMMENDED] APPROACH ({}% confidence) -------------+".format(int(predictions["confidence"])))
        output.append("|                                                         |")
        output.append(
            f"| Expected Quality: {int(predictions['quality_score'])}/100 (+{int(predictions['quality_score'] - 75)} from baseline)          |"
        )
        output.append(f"| Estimated Time:   {predictions['estimated_time']}                        |")
        output.append("|                                                         |")
        output.append("| Recommended Skills:                                     |")

        for skill in recs["skills"][:3]:
            status = skill["recommendation"]
            output.append(
                f"| {status}. [{status}] {skill['skill']} ({int(skill['success_rate'])}% success rate)".ljust(57) + " |"
            )

        output.append("|                                                         |")
        output.append("| Based on: {} similar successful patterns                |".format(len(recs["recommendations"])))
        output.append("|                                                         |")
        output.append("+---------------------------------------------------------+")
    else:
        output.append("+- [RECOMMENDED] APPROACH (50% confidence) -------------+")
        output.append("|                                                         |")
        output.append("| Expected Quality: 75/100 (baseline)                   |")
        output.append("| Estimated Time:   15-20 minutes                       |")
        output.append("|                                                         |")
        output.append("| Recommended Skills:                                     |")
        output.append("| 1. [PASS] code-analysis (baseline skill)               |")
        output.append("| 2. [PASS] quality-standards (recommended)              |")
        output.append("|                                                         |")
        output.append("| Based on: General best practices                       |")
        output.append("|                                                         |")
        output.append("+---------------------------------------------------------+")

    output.append("")

    # Alternative approaches
    output.append("+- [ALTERNATIVE] APPROACHES ------------------------------+")
    output.append("|                                                         |")

    if len(recs["recommendations"]) > 1:
        for i, rec in enumerate(recs["recommendations"][1:3], 2):
            quality = rec["quality_score"]
            time_est = f"{rec['execution_time']}-{int(rec['execution_time'] * 1.2)} min"
            output.append(
                f"| {i}. Pattern-Based Approach ({int(rec['recommendation_score'] * 100)}% confidence)".ljust(57) + " |"
            )
            output.append(f"|    Quality: {int(quality)}/100 | Time: {time_est}".ljust(57) + " |")
            output.append(f"|    Skills: {', '.join(rec['skills_used'][:2])}".ljust(57) + " |")
            output.append("|                                                         |")
    else:
        output.append("| 2. Minimal Approach (60% confidence)                   |")
        output.append("|    Quality: 70/100 | Time: 10-12 min                 |")
        output.append("|    Skills: code-analysis only                          |")
        output.append("|    [WARN] Lower quality but faster                     |")
        output.append("|                                                         |")

    output.append("+---------------------------------------------------------+")
    output.append("")

    # Risk assessment
    output.append("+- [{}] RISK ASSESSMENT ------------------------------------+".format(risks["level"]))
    output.append("|                                                         |")
    output.append(f"| Overall Risk: {risks['level']} ({risks['score']}/100)".ljust(57) + " |")
    output.append("|                                                         |")

    if risks["risks"]:
        for i, risk in enumerate(risks["risks"], 1):
            output.append(f"| {i}. [{risk['type']}] {risk['description']}".ljust(57) + " |")
            output.append(f"|    -> Mitigation: {risk['mitigation']}".ljust(57) + " |")
            if "time_impact" in risk:
                output.append(f"|    -> {risk['time_impact']}".ljust(57) + " |")
            output.append("|                                                         |")
    else:
        output.append("| [PASS] No significant risks identified                 |")
        output.append("|                                                         |")

    output.append("+---------------------------------------------------------+")
    output.append("")

    # Key insights
    output.append("+- [KEY] INSIGHTS ----------------------------------------+")
    output.append("|                                                         |")

    if recs["recommendations"]:
        output.append("| [PASS] Pattern-based approach available                     |")
        output.append(f"| [PASS] Expected success rate: {int(predictions['success_probability'])}%              |")
        output.append(f"| [PASS] Quality improvement: +{int(predictions['quality_score'] - 75)} points         |")
        if len(recs["skills"]) >= 3:
            output.append("| [PASS] Multi-skill approach recommended                |")
    else:
        output.append("| [WARN] No similar patterns found                         |")
        output.append("| [PASS] Using general best practices                      |")
        output.append("| [WARN] Consider breaking task into smaller steps         |")

    output.append("|                                                         |")
    output.append("+---------------------------------------------------------+")
    output.append("")

    # Final recommendation
    output.append("=" * 56)
    output.append("  RECOMMENDATION: Proceed with recommended approach")
    if predictions["confidence"] >= 80:
        output.append("  High confidence - expected excellent results")
    elif predictions["confidence"] >= 60:
        output.append("  Good confidence - recommended approach")
    else:
        output.append("  Moderate confidence - validate frequently")
    output.append("=" * 56)

    return "\n".join(output)


if __name__ == "__main__":
    main()
