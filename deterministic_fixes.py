def _deterministic_score(
    self,
    base_score: float,
    variance: float,
    seed_data: str) -> float:,
)
    """Generate deterministic scores based on seed data."""
    hash_obj = hashlib.md5(seed_data.encode())
    seed_value = int(hash_obj.hexdigest()[:8], 16) / 0xFFFFFFFF
    return base_score + (seed_value - 0.5) * variance * 2

def _deterministic_contribution(
    self,
    score: float,
    base_contribution: float,
    seed_data: str) -> float:,
)
    """Generate deterministic contribution based on score and seed."""
    hash_obj = hashlib.md5(f"{score}-{seed_data}".encode())
    seed_value = int(hash_obj.hexdigest()[:8], 16) / 0xFFFFFFFF
    return (score / 100) * base_contribution + (seed_value - 0.5) * 0.2

def _load_historical_model_performance(self) -> Dict[str, Any]:
    """Load actual historical model performance data from available sources."""
    model_data = {}
    
    # Load from quality_history.json
    quality_history = self._load_json_file("quality_history.json", "quality")
    model_scores = {}
    
    for assessment in quality_history.get("quality_assessments", []):
        timestamp = assessment.get("timestamp")
        model_used = assessment.get("details", {}).get("model_used", "Unknown")
        quality_score = assessment.get("overall_score")
        
        if timestamp and quality_score is not None and model_used != "Unknown":
            if model_used not in model_scores:
                model_scores[model_used] = []
            model_scores[model_used].append({
                "timestamp": timestamp,
                "score": quality_score
            })
    
    # Convert to dashboard format
    for model_name, scores in model_scores.items():
        if len(scores) > 0:
            # Calculate metrics
            avg_score = sum(s["score"] for s in scores) / len(scores)
            success_rate = len([s for s in scores if s["score"] >= 70]) / len(scores)
            
            model_data[model_name] = {
                "recent_scores": scores,
                "total_tasks": len(scores),
                "success_rate": round(success_rate, 2),
                "contribution_to_project": round(
    avg_score * 0.25,
    1)  # Estimate contribution,
)
            }
    
    return model_data if model_data else None
