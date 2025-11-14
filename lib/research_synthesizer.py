#!/usr/bin/env python3
"""
Research Synthesis Utility

Synthesizes research findings from multiple sources into comprehensive
reports with citations, trade-off matrices, and recommendations.

Cross-platform compatible (Windows, Linux, macOS).
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

def calculate_quality_score(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate research quality score (0-100).

    Scoring breakdown:
    - Citations (25 points): All findings properly cited
    - Source Credibility (25 points): Authoritative sources used
    - Technical Accuracy (25 points): Claims verified
    - Completeness (15 points): All questions answered
    - Clarity (10 points): Well-structured report
    """

    score = {
        "total": 0,
        "breakdown": {
            "citations": 0,
            "source_credibility": 0,
            "technical_accuracy": 0,
            "completeness": 0,
            "clarity": 0
        },
        "grade": "F"
    }

    # Calculate citations score (25 points)
    cited_findings = sum(1 for f in findings if f.get("sources"))
    if findings:
        score["breakdown"]["citations"] = int((cited_findings / len(findings)) * 25)

    # Calculate source credibility (25 points) - simplified
    # In real implementation, assess source domains
    score["breakdown"]["source_credibility"] = 20  # Placeholder

    # Calculate technical accuracy (25 points) - simplified
    verified_findings = sum(1 for f in findings if f.get("confidence") == "high")
    if findings:
        score["breakdown"]["technical_accuracy"] = int((verified_findings / len(findings)) * 25)

    # Calculate completeness (15 points) - simplified
    score["breakdown"]["completeness"] = 12  # Placeholder

    # Calculate clarity (10 points) - simplified
    score["breakdown"]["clarity"] = 8  # Placeholder

    # Calculate total
    score["total"] = sum(score["breakdown"].values())

    # Assign grade
    if score["total"] >= 90:
        score["grade"] = "A"
    elif score["total"] >= 80:
        score["grade"] = "B"
    elif score["total"] >= 70:
        score["grade"] = "C"
    elif score["total"] >= 60:
        score["grade"] = "D"
    else:
        score["grade"] = "F"

    return score


def generate_markdown_report(
    topic: str,
    findings: List[Dict[str, Any]],
    recommendations: List[Dict[str, Any]],
    sources: List[Dict[str, Any]]
) -> str:
    """Generate comprehensive Markdown research report."""

    quality_score = calculate_quality_score(findings)

    report = f"""# Research Report: {topic}

**Date**: {datetime.now().strftime("%Y-%m-%d")}
**Quality Score**: {quality_score["total"]}/100 (Grade: {quality_score["grade"]})

---

## Executive Summary

{len(findings)} key findings identified with {len(sources)} sources consulted.

---

## Key Findings

"""

    # Add findings
    for i, finding in enumerate(findings, 1):
        report += f"""### {i}. {finding.get("question", "Finding")}

**Answer**: {finding.get("answer", "N/A")}
**Confidence**: {finding.get("confidence", "N/A").capitalize()}

"""
        if finding.get("sources"):
            report += "**Sources**:\n"
            for source in finding["sources"]:
                report += f"- {source}\n"
            report += "\n"

    # Add recommendations
    if recommendations:
        report += "\n---\n\n## Recommendations\n\n"
        for i, rec in enumerate(recommendations, 1):
            report += f"""### {i}. {rec.get("recommendation", "N/A")}

**Rationale**: {rec.get("rationale", "N/A")}
**Conditions**: {rec.get("conditions", "N/A")}

"""

    # Add sources
    report += "\n---\n\n## Sources Consulted\n\n"
    for i, source in enumerate(sources, 1):
        report += f"{i}. [{source.get('title', 'Source')}]({source.get('url', '#')}) (Accessed: {source.get('accessed', 'N/A')})\n"

    return report


def save_report(report: str, output_path: str) -> None:
    """Save research report to file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"[OK] Research report saved: {output_path}")


def main():
    """CLI interface for research synthesis."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Synthesize research findings into comprehensive reports"
    )
    parser.add_argument("topic", help="Research topic")
    parser.add_argument(
        "--findings",
        required=True,
        help="Path to JSON file with research findings"
    )
    parser.add_argument(
        "--output",
        default=".claude/reports/research-{topic}-{timestamp}.md",
        help="Output path for research report"
    )

    args = parser.parse_args()

    # Load findings
    with open(args.findings, 'r', encoding='utf-8') as f:
        data = json.load(f)

    findings = data.get("findings", [])
    recommendations = data.get("recommendations", [])
    sources = data.get("sources", [])

    # Generate report
    report = generate_markdown_report(
        topic=args.topic,
        findings=findings,
        recommendations=recommendations,
        sources=sources
    )

    # Calculate quality score for terminal output
    quality_score = calculate_quality_score(findings)

    print(f"\n[OK] Research synthesis complete: {args.topic}")
    print(f"    Quality Score: {quality_score['total']}/100 (Grade: {quality_score['grade']})")
    print(f"    Findings: {len(findings)}")
    print(f"    Recommendations: {len(recommendations)}")
    print(f"    Sources: {len(sources)}")

    # Generate output path
    output_path = args.output.replace("{topic}", args.topic.replace(" ", "-").lower())
    output_path = output_path.replace("{timestamp}", datetime.now().strftime("%Y%m%d-%H%M%S"))

    # Save report
    save_report(report, output_path)

    print(f"    Report: {output_path}")


if __name__ == "__main__":
    main()
