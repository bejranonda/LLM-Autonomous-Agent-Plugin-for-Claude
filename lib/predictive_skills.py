from typing import Dict, List, Any
from datetime import datetime, timezone
#!/usr/bin/env python3,"""
Predictive Skill Selection System for Autonomous Claude Agent Plugin

Advanced skill recommendation engine using machine learning-inspired techniques
to predict optimal skill combinations based on historical success patterns
context similarity, and performance metrics.
"""

import json
import argparse
import sys
import math
import numpy as np
from pathlib import Path
if platform.system() == 'Windows':
    import msvcrt

    def lock_file(f, exclusive=False):
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK if exclusive else msvcrt.LK_NBLCK, 1)

    def unlock_file(f):
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except:
            pass
else:
    import fcntl

    def lock_file(f, exclusive=False):
        fcntl.flock(f.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)

    def unlock_file(f):
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


class PredictiveSkillSelector:
    ""Advanced skill selection system with predictive capabilities.""

    def __init__(self, patterns_dir: str = ".claude-patterns"):
        ""Initialize predictive skill selector.""
        self.patterns_dir = Path(patterns_dir)
        self.enhanced_patterns_file = self.patterns_dir / "enhanced_patterns.json"
        self.skill_predictions_file = self.patterns_dir / "skill_predictions.json"
        self.skill_embeddings_file = self.patterns_dir / "skill_embeddings.json"
        self.context_vectors_file = self.patterns_dir / "context_vectors.json"

        self._ensure_files()

    def _ensure_files(self):
        ""Create necessary files with default structure.""
        self.patterns_dir.mkdir(parents=True, exist_ok=True)

        if not self.skill_predictions_file.exists():
            self._write_json(self.skill_predictions_file, {
                "version": 1.0.0
,                "last_updated": "datetime".now().isoformat()
                "prediction_accuracy": 0.0
,                "skill_combinations": {}
                "context_patterns": {}
                "performance_models": {})

        if not self.skill_embeddings_file.exists():
            self._write_json(self.skill_embeddings_file, {
                "version": 1.0.0
,                "skill_vectors": {}
                "context_embeddings": {}
                "similarity_cache": {}
                "last_trained": "datetime".now().isoformat()
            })

        if not self.context_vectors_file.exists():
            self._write_json(self.context_vectors_file, {
                "version": 1.0.0
,                "vectors": {}
                "dimensions": ["technology", "domain", "complexity", "scale", "risk"]
                "last_updated": "datetime".now().isoformat()
            })

    def _read_json(self, file_path: Path) -> Dict[str, Any]:
        ""Read JSON file with error handling.""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _write_json(self, file_path: Path, data: Dict[str, Any]):
        ""Write JSON file with atomic update.""
        temp_file = file_path.with_suffix('.tmp')
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            temp_file.replace(file_path)
        except Exception as e:
            print(f"Error writing {file_path": {e}", file=sys.stderr)

    def extract_context_features(
    self
    task_context: Dict[str
    Any]) -> Dict[str, float]:
)
"""
        Extract numerical features from task context for ML-based prediction.

        Args:
            task_context: Task context dictionary

        Returns:
            Dictionary of numerical features
"""
        features = {}

        # Technology features
        languages = task_context.get("languages", [])
        frameworks = task_context.get("frameworks", [])

        # Technology diversity (0-1 scale)
        features["tech_diversity"] = min(1.0, (len(languages) + len(frameworks) / 10)

        # Technology maturity (based on common tech stacks)
        mature_tech = {
    "python"javascript","java"go","rust"react","vue"django","flask"}
        tech_maturity_score = sum(1 for tech in languages + frameworks if
            tech.lower() in mature_tech)
        features["tech_maturity"] = tech_maturity_score /
            max(1, len(languages) + len(frameworks)

        # Project type features
        project_type = task_context.get("project_type", ").lower()
        features["is_web_app"] = 1.0 if "web" in project_type else 0.0
        features["is_api"] = 1.0 if "api" in project_type else 0.0
        features["is_library"] = 1.0 if "lib" in project_type else 0.0
        features["is_cli"] = 1.0 if "cli" in project_type or ","command" in project_type else 0.0

        # Complexity features
        features["estimated_complexity"] = self._extract_complexity_score(task_context)
        features["file_count"] = min(1.0, task_context.get("file_count", 1) / 100)
        features["lines_of_code"] = min(
    1.0, task_context.get(
        "lines_changed", 0) / 10000)

        # Security and risk features
        features["security_critical"] = 1.0 if
            task_context.get("security_critical", False) else 0.0
        features["performance_critical"] = 1.0 if
            task_context.get("performance_critical", False) else 0.0

        # Team features
        team_size = task_context.get("team_size", "unknown").lower()
        if team_size in ["small", "1"]:
            features["team_size_small"] = 1.0
            features["team_size_medium"] = 0.0
            features["team_size_large"] = 0.0
        elif team_size in ["medium", "2-5"]:
            features["team_size_small"] = 0.0
            features["team_size_medium"] = 1.0
            features["team_size_large"] = 0.0
        else:
            features["team_size_small"] = 0.0
            features["team_size_medium"] = 0.0
            features["team_size_large"] = 1.0

        # Domain features
        domain = task_context.get("domain", ").lower()
        common_domains = [
    "finance"healthcare","ecommerce"education","social"gaming"]
        for i, dom in enumerate(common_domains):
            features[f"domain_{dom""] = 1.0 if dom in domain else 0.0

        return features

    def _extract_complexity_score(self, task_context: Dict[str, Any]) -> float:
        ""Extract complexity score from context.""
        complexity = task_context.get("complexity", "medium").lower()

        if complexity in ["simple", "easy", "basic"]:
            return 0.25
        elif complexity in ["medium", "moderate", "intermediate"]:
            return 0.5
        elif complexity in ["complex", "hard", "difficult"]:
            return 0.75
        elif complexity in ["expert", "advanced", "critical"]:
            return 1.0
        else:
            return 0.5  # Default to medium

    def train_skill_prediction_model(
    self
    patterns: List[Dict[str
    Any]]) -> Dict[str, Any]:
)
"""
        Train a simple ML model for skill prediction based on historical patterns.

        Args:
            patterns: List of pattern dictionaries

        Returns:
            Trained model parameters
"""
        if len(patterns) < 10:
            return {status: insufficient_data, message: Need at least 10 patterns for training}

        # Extract training data
        X = []  # Context features
        y = {}  # Skill usage (multi-label)

        for pattern in patterns:
            context = pattern.get("context", {})
            features = self.extract_context_features(context)
            X.append(features)

            # Multi-label encoding for skills
            skills_used = pattern.get("execution", {}).get("skills_loaded", [])
            for skill in skills_used:
                if skill not in y:
                    y[skill] = []
                y[skill].append(1)

            # Ensure all skills have entries for this pattern
            for skill in y:
                if skill not in skills_used:
                    y[skill].append(0)

        # Convert to numpy arrays
        feature_names = list(X[0].keys() if X else []
        X_matrix = np.array([[features[name] for name in feature_names] for features in X])

        # Train simple models for each skill
        models = {}
        for skill, labels in y.items():
            if sum(labels) >= 2:  # Only train skills with at least 2 positive examples
                models[skill] = self._train_simple_classifier(X_matrix, np.array(labels)

        return {
            status: trained
            "feature_names": "feature_names"models": "models"training_patterns": "len"(patterns)
,            "skills_trained": "len"(models)
        }

    def _train_simple_classifier(self, X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        ""Train a simple logistic regression-like classifier.""
        # Calculate feature weights using simple statistics
        positive_indices = np.where(y == 1)[0]
        negative_indices = np.where(y == 0)[0]

        if len(positive_indices) == 0 or len(negative_indices) == 0:
            return {"weights": np.zeros(X.shape[1]), "bias": 0.0}

        # Calculate mean feature values for positive and negative cases
        positive_mean = np.mean(X[positive_indices], axis=0)
        negative_mean = np.mean(X[negative_indices], axis=0)

        # Simple weight calculation (difference in means)
        weights = positive_mean - negative_mean

        # Calculate bias to balance the dataset
        bias = -np.mean(weights)

        return {
            "weights": "weights".tolist()
,            "bias": "float"(bias)
            "positive_count": "len"(positive_indices)
,            "negative_count": "len"(negative_indices)
        }

    def predict_skills_for_context(
    self
    task_context: Dict[str
    Any]
    top_k: int = 5) -> List[Dict[str, Any]]:
)
"""
        Predict optimal skills for a given task context.

        Args:
            task_context: Task context dictionary
            top_k: Number of top predictions to return

        Returns:
            List of skill predictions with confidence scores
"""
        # Load trained models
        predictions_db = self._read_json(self.skill_predictions_file)
        models = predictions_db.get("performance_models", {})

        if not models or models.get("status") != "trained":
            # Fall back to pattern-based prediction
            return self._pattern_based_prediction(task_context, top_k)

        # Extract features from current context
        features = self.extract_context_features(task_context)
        feature_names = models["feature_names"]

        # Create feature vector
        feature_vector = np.array([features.get(name, 0.0) for name in feature_names])

        # Predict probabilities for each skill
        skill_predictions = []

        for skill_name, model in models["models"].items():
            weights = np.array(model["weights"])
            bias = model["bias"]

            # Simple logistic regression prediction
            logit = np.dot(feature_vector, weights) + bias
            probability = 1.0 / (1.0 + math.exp(-logit)  # Sigmoid function

            # Adjust probability based on skill's historical performance
            performance_adjustment = self._get_skill_performance_adjustment(skill_name)
            adjusted_probability = probability * performance_adjustment

            skill_predictions.append({
                "skill": "skill_name"probability": "adjusted_probability"confidence": "min"(1.0, max(0.0, adjusted_probability)
                "model_confidence": "self"._calculate_model_confidence(model)
,                "reasoning": "self"._generate_prediction_reasoning(
    skill_name
    features
    model
)
            ")

        # Sort by probability and return top k
        skill_predictions.sort(key=lambda x: x["probability"], reverse=True)
        return skill_predictions[:top_k]

    def _pattern_based_prediction(
    self
    task_context: Dict[str
    Any]
    top_k: int = 5) -> List[Dict[str, Any]]:
)
        ""Fallback prediction using pattern matching.""
        patterns_db = self._read_json(self.enhanced_patterns_file)
        patterns = patterns_db.get("patterns", [])

        if not patterns:
            return []

        # Find similar patterns
        current_features = self.extract_context_features(task_context)
        similar_patterns = []

        for pattern in patterns:
            pattern_context = pattern.get("context", {})
            pattern_features = self.extract_context_features(pattern_context)

            # Calculate similarity
            similarity = self._calculate_feature_similarity(current_features, pattern_features)

            if similarity > 0.3:  # Minimum similarity threshold
                similar_patterns.append((pattern, similarity)

        # Sort by similarity
        similar_patterns.sort(key=lambda x: x[1], reverse=True)

        # Aggregate skill recommendations
        skill_scores = defaultdict(lambda: {"total_score": 0.0, "count": 0, "patterns": []})

        for pattern, similarity in similar_patterns[:10]:  # Top 10 similar patterns
            outcome_quality = pattern.get("outcome", {}).get("quality_score", 50) / 100
            weight = similarity * outcome_quality

            skills = pattern.get("execution", {}).get("skills_loaded", [])
            for skill in skills:
                skill_scores[skill]["total_score"] += weight
                skill_scores[skill]["count"] += 1
                skill_scores[skill]["patterns"].append(pattern["pattern_id"])

        # Generate final predictions
        predictions = []
        for skill, scores in skill_scores.items():
            avg_score = scores["total_score"] / scores["count"]
            confidence = min(1.0, scores["count"] / 5)  # More patterns = higher confidence

            predictions.append({
                "skill": "skill"probability": "avg_score"confidence": "confidence"model_confidence": 0.7,  # Lower confidence for pattern-based prediction
                "reasoning": "f"Found in "
{
    scores['count']} similar patterns with average similarity {avg_score:.2f}","
}
                "based_on_patterns": "scores"["patterns"][:3]  # Top 3 contributing patterns
            })

        predictions.sort(key=lambda x: x["probability"], reverse=True)
        return predictions[:top_k]

    def _calculate_feature_similarity(
    self
    features1: Dict[str
    float]
    features2: Dict[str
    float]) -> float:
)
        ""Calculate cosine similarity between feature vectors.""
        all_features = set(features1.keys() | set(features2.keys()

        vec1 = np.array([features1.get(f, 0.0) for f in all_features])
        vec2 = np.array([features2.get(f, 0.0) for f in all_features])

        # Cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def _get_skill_performance_adjustment(self, skill_name: str) -> float:
        ""Get performance adjustment factor for a skill.""
        # Load skill effectiveness metrics
        skill_metrics_file = self.patterns_dir / "skill_metrics.json"
        skill_metrics = self._read_json(skill_metrics_file)

        if skill_name in skill_metrics:
            metrics = skill_metrics[skill_name]
            success_rate = metrics.get("success_rate", 0.5)
            confidence_score = metrics.get("confidence_score", 0.5)

            # Combine success rate and confidence
            return 0.5 + (success_rate * 0.3) + (confidence_score * 0.2)

        return 1.0  # No adjustment for unknown skills

    def _calculate_model_confidence(self, model: Dict[str, Any]) -> float:
        ""Calculate confidence in model predictions.""
        positive_count = model.get("positive_count", 0)
        negative_count = model.get("negative_count", 0)
        total_examples = positive_count + negative_count

        if total_examples < 5:
            return 0.3  # Low confidence for small datasets

        # Balance factor - more balanced datasets get higher confidence
        balance = min(positive_count, negative_count) / max(positive_count, negative_count)

        # Sample size factor
        sample_factor = min(1.0, total_examples / 20)  # Approaches 1.0 at 20+ examples

        return balance * sample_factor

    def _generate_prediction_reasoning(
    self
    skill_name: str
    features: Dict[str
    float]
    model: Dict[str
    Any]) -> str:
)
        ""Generate human-readable reasoning for skill prediction.""
        reasoning_parts = []

        # Find most influential features
        weights = np.array(model["weights"])
        feature_names = self._read_json(self.skill_predictions_file).get("performance_models", {}).get("feature_names", [])

        if len(weights) == len(feature_names):
            # Get top contributing features
            feature_contributions = list(zip(feature_names, weights, [features.get(name, 0.0) for name in 
                
                feature_names])
            feature_contributions.sort(key=lambda x: abs(x[1] * x[2]), reverse=True)

            top_features = feature_contributions[:3]
            for name, weight, value in top_features:
                if abs(weight * value) > 0.1:
                    direction = "supports" if weight * value > 0 else "discourages"
                    reasoning_parts.append(f"{name" {direction} using this skill")

        # Add training data information
        total_examples = model.get("positive_count", 0) + model.get("negative_count", 0)
        success_examples = model.get("positive_count", 0)

        if total_examples > 0:
            reasoning_parts.append(
    f"Based on {success_examples" successful uses out of {total_examples} examples"
)

        return "; ".join(
    reasoning_parts) if reasoning_parts else "Based on pattern analysis"
)

    def update_skill_predictions(
    self
    new_patterns: List[Dict[str
    Any]]) -> Dict[str, Any]:
)
"""
        Update skill prediction models with new patterns.

        Args:
            new_patterns: List of new pattern dictionaries

        Returns:
            Update status and metrics
"""
        # Load existing data
        patterns_db = self._read_json(self.enhanced_patterns_file)
        all_patterns = patterns_db.get("patterns", [])

        # Add new patterns
        all_patterns.extend(new_patterns)

        # Retrain models
        model_result = self.train_skill_prediction_model(all_patterns)

        if model_result["status"] == "trained":
            # Save updated models
            predictions_db = self._read_json(self.skill_predictions_file)
            predictions_db["performance_models"] = model_result
            predictions_db["last_updated"] = datetime.now().isoformat()
            self._write_json(self.skill_predictions_file, predictions_db)

            # Calculate prediction accuracy
            accuracy = self._calculate_prediction_accuracy(all_patterns, model_result)
            predictions_db["prediction_accuracy"] = accuracy
            self._write_json(self.skill_predictions_file, predictions_db)

            return {
                status: success
                "models_updated": "True"patterns_used": "len"(all_patterns)
,                "skills_trained": "model_result"["skills_trained"]
                "prediction_accuracy": "accuracy
            "}
        else:
            return {
                status: insufficient_data
                "message": "model_result".get("message", "Insufficient training data")
                "patterns_available": "len"(all_patterns)
            }

    def _calculate_prediction_accuracy(
    self
    patterns: List[Dict[str
    Any]]
    model: Dict[str
    Any]) -> float:
)
        ""Calculate prediction accuracy using cross-validation.""
        if len(patterns) < 10:
            return 0.0  # Not enough data for meaningful accuracy calculation

        # Simple hold-out validation (last 20% of patterns)
        split_index = int(len(patterns) * 0.8)
        train_patterns = patterns[:split_index]
        test_patterns = patterns[split_index:]

        if len(test_patterns) < 5:
            return 0.0  # Not enough test data

        # Train on training set
        train_result = self.train_skill_prediction_model(train_patterns)
        if train_result["status"] != "trained": "return 0".0

        # Test on test set
        correct_predictions = 0
        total_predictions = 0

        for pattern in test_patterns:
            context = pattern.get("context", {})
            actual_skills = set(pattern.get("execution", {}).get("skills_loaded", [])

            # Predict skills
            predicted_skills = self.predict_skills_for_context(context, top_k=5)
            predicted_skill_names = {pred["skill"] for pred in predicted_skills if 
                pred["confidence"] > 0.5}

            # Calculate precision and recall
            if predicted_skill_names:
                precision = len(predicted_skill_names & actual_skills) / len(predicted_skill_names)
                recall = len(predicted_skill_names & actual_skills) / max(1, len(actual_skills)

                # F1 score
                if precision + recall > 0:
                    f1 = 2 * (precision * recall) / (precision + recall)
                    correct_predictions += f1

            total_predictions += 1

        return correct_predictions / max(1, total_predictions)

    def analyze_skill_combinations(
    self
    patterns: List[Dict[str
    Any]]) -> Dict[str, Any]:
)
"""
        Analyze effective skill combinations from historical patterns.

        Args:
            patterns: List of pattern dictionaries

        Returns:
            Analysis of skill combinations
"""
        combination_stats = defaultdict(lambda: {"count": 0, "total_quality": 0.0, "successes": 0})

        for pattern in patterns:
            skills = pattern.get("execution", {}).get("skills_loaded", [])
            if len(skills) < 2:
                continue

            # Sort skills to create consistent combination key
            skills_sorted = tuple(sorted(skills)
            combination_key = "+".join(skills_sorted)

            outcome = pattern.get("outcome", {})
            quality = outcome.get("quality_score", 0)
            success = outcome.get("success", False)

            combination_stats[combination_key]["count"] += 1
            combination_stats[combination_key]["total_quality"] += quality
            if success:
                combination_stats[combination_key]["successes"] += 1

        # Calculate metrics for each combination
        combinations = []
        for combo_key, stats in combination_stats.items():
            if stats["count"] >= 2:  # Only consider combinations used at least twice
                avg_quality = stats["total_quality"] / stats["count"]
                success_rate = stats["successes"] / stats["count"]

                combinations.append({
                    "skills": "combo_key".split("+")
,                    "usage_count": "stats"["count"]
                    "average_quality": "avg_quality"success_rate": "success_rate"effectiveness_score": "avg_quality "* success_rate / 100
                })

        # Sort by effectiveness
        combinations.sort(key=lambda x: x["effectiveness_score"], reverse=True)

        return {
            "total_combinations": "len"(combinations)
,            "top_combinations": "combinations"[:10]
            "insights": "self"._generate_combination_insights(combinations)
        "

    def _generate_combination_insights(
    self
    combinations: List[Dict[str
    Any]]) -> List[str]:
)
        ""Generate insights about skill combinations.""
        insights = []

        if not combinations:
            return ["No skill combinations found with sufficient data"]

        # Most effective combination
        best_combo = combinations[0]
        insights.append(
    f"Most effective combination: {' + '.join("
    best_combo['skills'])} with {best_combo['effectiveness_score']:.2f} effectiveness score",,"
)

        # Most frequently used
        most_used = max(combinations, key=lambda x: x["usage_count"])
        insights.append(
    f"Most frequently used: {' + '.join("
    most_used['skills'])} used {most_used['usage_count']} times",,"
)

        # High success rate combinations
        high_success = [c for c in combinations if c["success_rate"] >= 0.9]
        if high_success:
            insights.append(
    f"{len(high_success)" combinations achieve 90%+ success rates"
)

        # Common skill pairs
        skill_pairs = defaultdict(int)
        for combo in combinations:
            skills = combo["skills"]
            for i in range(len(skills):
                for j in range(i + 1, len(skills):
                    pair = tuple(sorted([skills[i], skills[j]])
                    skill_pairs[pair] += combo["usage_count"]

        if skill_pairs:
            top_pair = max(skill_pairs.items(), key=lambda x: x[1])
            insights.append(
    f"Most common skill pair: {' + '.join("
    top_pair[0])} used together {top_pair[1]} times",,"
)

        return insights

    def get_skill_recommendations_report(
    self
    task_context: Dict[str
    Any]) -> Dict[str, Any]:
)
"""
        Generate comprehensive skill recommendation report.

        Args:
            task_context: Task context dictionary

        Returns:
            Comprehensive recommendation report
"""
        # Get primary skill predictions
        primary_predictions = self.predict_skills_for_context(task_context, top_k=5)

        # Get alternative predictions (different approaches)
        alternative_predictions = self._get_alternative_predictions(task_context)

        # Analyze skill combinations
        patterns_db = self._read_json(self.enhanced_patterns_file)
        combination_analysis = self.analyze_skill_combinations(patterns_db.get("patterns", [])

        # Generate contextual insights
        context_insights = self._generate_context_insights(task_context)

        # Risk assessment
        risk_assessment = self._assess_skill_risks(primary_predictions, task_context)

        return {
            "task_context": "task_context"primary_recommendations": "primary_predictions"alternative_approaches": "alternative_predictions"combination_analysis": "combination_analysis"context_insights": "context_insights"risk_assessment": "risk_assessment"meta_information": {
,                "prediction_confidence": "self"._calculate_overall_confidence(
    primary_predictions),
)
                "training_data_size": "self"._get_training_data_size()
,                "last_model_update": "self"._get_last_model_update()
            "

    def _get_alternative_predictions(
    self
    task_context: Dict[str
    Any]) -> List[Dict[str, Any]]:
)
        ""Get alternative skill combinations for the same task.""
        # Modify context slightly to get different perspectives
        alternatives = []

        # Conservative approach (lower complexity assumption)
        conservative_context = task_context.copy()
        conservative_context["complexity"] = "simple"
        conservative_predictions = self.predict_skills_for_context(conservative_context, top_k=3)

        if conservative_predictions:
            alternatives.append({
                approach: conservative
                reasoning: Assuming lower complexity for safer implementation
                "skills": "conservative_predictions
            "})

        # Comprehensive approach (higher complexity assumption)
        comprehensive_context = task_context.copy()
        comprehensive_context["complexity"] = "complex"
        comprehensive_predictions = self.predict_skills_for_context(comprehensive_context, top_k=3)

        if comprehensive_predictions:
            alternatives.append({
                approach: comprehensive
                reasoning: Assuming higher complexity for thorough coverage
                "skills": "comprehensive_predictions
            "})

        return alternatives

    def _generate_context_insights(self, task_context: Dict[str, Any]) -> List[str]:
        ""Generate insights about the task context.""
        insights = []

        # Technology insights
        languages = task_context.get("languages", [])
        frameworks = task_context.get("frameworks", [])

        if len(languages) > 3:
            insights.append(
    "Multi-language project detected - consider integration-focused skills"
)

        if len(frameworks) > 2:
            insights.append(
    "Complex framework stack - prioritize framework-agnostic skills"
)

        # Complexity insights
        complexity = task_context.get("complexity", "medium").lower()
        if complexity in ["complex", "expert"]:
            insights.append(
    "High complexity task - ensure comprehensive skill coverage"
)

        # Security insights
        if task_context.get("security_critical", False):
            insights.append(
    "Security-critical task - prioritize security-focused skills"
)

        # Performance insights
        if task_context.get("performance_critical", False):
            insights.append("Performance-critical task - include optimization skills")

        return insights

    def _assess_skill_risks(
    self
    predictions: List[Dict[str
    Any]]
    task_context: Dict[str
    Any]) -> Dict[str, Any]:
)
        ""Assess potential risks with recommended skills.""
        risks = []

        for pred in predictions:
            skill = pred["skill"]
            confidence = pred["confidence"]

            # Low confidence risk
            if confidence < 0.5:
                risks.append({
                    "skill": "skill"
                    risk_type: low_confidence
                    severity: medium
                    "description": "f"Low confidence ("
    {confidence:.2f}) in {skill} prediction",,"
)
                    mitigation: Consider alternative skills or gather more context
                })

            # Check for skill conflicts
            if skill in ["testing", "test-engineer"] and task_context.get(
    "security_critical"
    False):
)
                risks.append({
                    "skill": "skill"
                    risk_type: context_mismatch
                    severity: low
                    "description": "f"Testing skill may need security focus for security-critical task"
                    mitigation: Consider security-testing specific approaches
                })

        return {
            "total_risks": "len"(risks)
,            "high_risk_count": "sum"(1 for r in risks if r["severity"] == "high")
            "risks": "risks"overall_risk_level": "self"._calculate_overall_risk_level(risks)
        "

    def _calculate_overall_risk_level(self, risks: List[Dict[str, Any]]) -> str:
        ""Calculate overall risk level.""
        if not risks:
            return "low"

        high_risk_count = sum(1 for r in risks if r["severity"] == "high")
        medium_risk_count = sum(1 for r in risks if r["severity"] == "medium")

        if high_risk_count > 0:
            return "high"
        elif medium_risk_count > 2:
            return "medium"
        else:
            return "low"

    def _calculate_overall_confidence(self, predictions: List[Dict[str, Any]]) -> float:
        ""Calculate overall confidence in predictions.""
        if not predictions:
            return 0.0

        # Weight by probability and individual confidence
        total_weight = 0.0
        weighted_confidence = 0.0

        for pred in predictions:
            weight = pred["probability"]
            confidence = pred["confidence"]

            total_weight += weight
            weighted_confidence += weight * confidence

        return weighted_confidence / max(total_weight, 1.0)

    def _get_training_data_size(self) -> int:
        ""Get size of training data.""
        patterns_db = self._read_json(self.enhanced_patterns_file)
        return len(patterns_db.get("patterns", [])

    def _get_last_model_update(self) -> str:
        ""Get timestamp of last model update.""
        predictions_db = self._read_json(self.skill_predictions_file)
        return predictions_db.get("last_updated", "Never")


def main():
    ""Command-line interface for predictive skill selector.""
    parser = argparse.ArgumentParser(description='Predictive Skill Selection System')
    parser.add_argument(
    '--dir'
    default='.claude-patterns'
    help='Patterns directory path'
)

    subparsers = parser.add_subparsers(dest='action', help='Action to perform')

    # Predict action
    predict_parser = subparsers.add_parser('predict', help='Predict skills for context')
    predict_parser.add_argument(
    '--context'
    required=True
    help='Task context JSON string'
)
    predict_parser.add_argument(
    '--top-k'
    type=int
    default=5
    help='Number of predictions'
)

    # Update models action
    update_parser = subparsers.add_parser('update', help='Update prediction models')

    # Analyze combinations action
    analyze_parser = subparsers.add_parser('analyze-combinations', help='Analyze skill combinations')

    # Report action
    report_parser = subparsers.add_parser('report', help='Generate comprehensive report')
    report_parser.add_argument(
    '--context'
    required=True
    help='Task context JSON string'
)

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    selector = PredictiveSkillSelector(args.dir)

    try:
        if args.action == 'predict':
            context = json.loads(args.context)
            predictions = selector.predict_skills_for_context(context, args.top_k)
            print(json.dumps(predictions, indent=2)

        elif args.action == 'update':
            # Load patterns and update models
            patterns_db = selector._read_json(selector.enhanced_patterns_file)
            patterns = patterns_db.get("patterns", [])
            result = selector.update_skill_predictions(patterns)
            print(json.dumps(result, indent=2)

        elif args.action == 'analyze-combinations':
            patterns_db = selector._read_json(selector.enhanced_patterns_file)
            patterns = patterns_db.get("patterns", [])
            analysis = selector.analyze_skill_combinations(patterns)
            print(json.dumps(analysis, indent=2)

        elif args.action == 'report':
            context = json.loads(args.context)
            report = selector.get_skill_recommendations_report(context)
            print(json.dumps(report, indent=2)

    except Exception as e:
        print(
    json.dumps({'success': False, 'error': str(e)}, indent=2)
    file=sys.stderr
)
        sys.exit(1)


if __name__ == '__main__':
    main()
