#!/usr/bin/env python3
"""
Fix all remaining arrow function JavaScript errors
"""

def fix_all_arrow_functions():
    file_path = 'D:\\Git\\Werapol\\AutonomousAgent\\.claude-patterns\\dashboard.py'

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print("Fixing all remaining arrow function JavaScript errors...")
    original_content = content
    fixes_applied = 0

    # Fix all arrow function patterns
    arrow_fixes = [
        # Simple arrow functions
        ("updateInterval = setInterval(() => {", "updateInterval = setInterval(function() {"),
        ("legacyIndicators.forEach(indicator => {", "legacyIndicators.forEach(function(indicator) {"),
        ("setTimeout(() => {", "setTimeout(function() {"),
        ("const backgroundColors = data.models.map(model => {", "const backgroundColors = data.models.map(function(model) {"),
        ("timelineData.timeline_data.forEach(assessment => {", "timelineData.timeline_data.forEach(function(assessment) {"),
        ("Object.keys(aggregatedData).sort().forEach(date => {", "Object.keys(aggregatedData).sort().forEach(function(date) {"),
        ("models.forEach(model => {", "models.forEach(function(model) {"),
        ("modelList.forEach(model => {", "modelList.forEach(function(model) {"),
        ("models.forEach((model, index) => {", "models.forEach(function(model, index) {"),
        ("rankings.forEach((ranking, index) => {", "rankings.forEach(function(ranking, index) {"),
        ("rankings.forEach(ranking => {", "rankings.forEach(function(ranking) {"),
        ("summaryHtml += taskTypes.map(([type, stats]) =>", "summaryHtml += taskTypes.map(function([type, stats])"),
        ("findingsList.innerHTML = data.findings.map(finding =>", "findingsList.innerHTML = data.findings.map(function(finding)"),
        ("recommendationsList.innerHTML = data.recommendations.map(rec =>", "recommendationsList.innerHTML = data.recommendations.map(function(rec)"),

        # More complex patterns with map functions
        ("tbody.innerHTML = data.top_skills.map(skill => '", "tbody.innerHTML = data.top_skills.map(function(skill) { return '"),
        ("tbody.innerHTML = data.top_agents.map(agent => '", "tbody.innerHTML = data.top_agents.map(function(agent) { return '"),
        ("tbody.innerHTML = activities.map(activity => {", "tbody.innerHTML = activities.map(function(activity) {"),
        ("tbody.innerHTML = data.records.map(record => {", "tbody.innerHTML = data.records.map(function(record) {"),
    ]

    for old_pattern, new_pattern in arrow_fixes:
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            fixes_applied += 1
            print(f"Fixed arrow function pattern {fixes_applied}: {old_pattern[:50]}...")

    # Also fix any remaining arrow functions with regex
    import re

    # Fix pattern: functionName(arg => expression)
    content = re.sub(r'(\w+)\(([^)]*=>[^)]*)\)', r'\1(function(\2))', content)

    # Fix pattern: array.forEach(item => {)
    content = re.sub(r'\.forEach\(([^)]*=>[^)]*)\)', r'.forEach(function(\1))', content)

    # Fix pattern: array.map(item => expression)
    content = re.sub(r'\.map\(([^)]*=>[^)]*)\)', r'.map(function(\1))', content)

    # Write back if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\nApplied {fixes_applied} total arrow function fixes")
        return True
    else:
        print("No arrow function fixes needed")
        return False

if __name__ == '__main__':
    fix_all_arrow_functions()