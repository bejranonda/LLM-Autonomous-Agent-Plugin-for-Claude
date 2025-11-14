#!/usr/bin/env python3
"""Multi-Project Learning System"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import hashlib


class MultiProjectLearningSystem:
    def __init__(self, base_dir: str = ".claude-patterns"):
        """  Init  ."""
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.shared_knowledge_file = self.base_dir / "shared_knowledge.json"
        self._ensure_data_structure()

    def _ensure_data_structure(self):
        """ Ensure Data Structure."""
        if not self.shared_knowledge_file.exists():
            default = {"universal_patterns": [], "cross_project_insights": [], "last_updated": datetime.now().isoformat()}
            with open(self.shared_knowledge_file, "w") as f:
                json.dump(default, f, indent=2)

    def extract_project_patterns(self, project_path: str) -> Dict[str, Any]:
        """Extract Project Patterns."""
        project_path = Path(project_path)
        patterns = {
            "project_id": hashlib.md5(str(project_path).encode()).hexdigest()[:12],
            "detected_languages": self._detect_languages(project_path),
            "frameworks": self._detect_frameworks(project_path),
            "timestamp": datetime.now().isoformat(),
        }
        self._update_shared_knowledge(patterns)
        return patterns

    def _detect_languages(self, project_path: Path) -> List[str]:
        """ Detect Languages."""
        languages = []
        if list(project_path.rglob("*.py")):
            languages.append("python")
        if list(project_path.rglob("*.js")):
            languages.append("javascript")
        if list(project_path.rglob("*.java")):
            languages.append("java")
        return languages

    def _detect_frameworks(self, project_path: Path) -> List[str]:
        """ Detect Frameworks."""
        frameworks = []
        if (project_path / "requirements.txt").exists():
            try:
                with open(project_path / "requirements.txt") as f:
                    content = f.read().lower()
                    if "django" in content:
                        frameworks.append("django")
                    if "flask" in content:
                        frameworks.append("flask")
            except:
                pass
        if (project_path / "package.json").exists():
            try:
                with open(project_path / "package.json") as f:
                    content = f.read().lower()
                    if "react" in content:
                        frameworks.append("react")
                    if "vue" in content:
                        frameworks.append("vue")
            except:
                pass
        return frameworks

    def _update_shared_knowledge(self, patterns: Dict[str, Any]):
        """ Update Shared Knowledge."""
        try:
            with open(self.shared_knowledge_file, "r") as f:
                shared_data = json.load(f)
        except:
            shared_data = {"universal_patterns": [], "cross_project_insights": []}

        universal_patterns = shared_data.get("universal_patterns", [])

        # Track framework combinations
        framework_combo = sorted(patterns.get("frameworks", []))
        if len(framework_combo) > 1:
            pattern_entry = {
                "pattern_type": "framework_combination",
                "pattern_value": framework_combo,
                "frequency": 1,
                "projects": [patterns["project_id"]],
            }

            # Check if pattern exists
            found = False
            for existing in universal_patterns:
                if existing["pattern_type"] == "framework_combination" and existing["pattern_value"] == framework_combo:
                    existing["frequency"] += 1
                    existing["projects"].append(patterns["project_id"])
                    found = True
                    break

            if not found:
                universal_patterns.append(pattern_entry)

        shared_data["universal_patterns"] = universal_patterns
        shared_data["last_updated"] = datetime.now().isoformat()

        with open(self.shared_knowledge_file, "w") as f:
            json.dump(shared_data, f, indent=2)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project-path", required=True)
    args = parser.parse_args()

    mpls = MultiProjectLearningSystem()
    result = mpls.extract_project_patterns(args.project_path)
    print(json.dumps(result, indent=2))
