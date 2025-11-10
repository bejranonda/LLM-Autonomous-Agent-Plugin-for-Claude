#!/usr/bin/env python3
"""
Fix the remaining arrow functions with more targeted patterns
"""

def fix_remaining_arrows():
    file_path = '.claude-patterns/dashboard.py'

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print('Fixing remaining arrow functions in .claude-patterns/dashboard.py')
    original_count = content.count('=>')
    print(f'Before fix - Arrow functions: {original_count}')

    original_content = content
    fixes_applied = 0

    # More specific arrow function patterns
    arrow_patterns = [
        # document.querySelectorAll pattern
        ("document.querySelectorAll('.dashboard-section').forEach(section => {",
         "document.querySelectorAll('.dashboard-section').forEach(function(section) {"),

        ("document.querySelectorAll('.tab-button').forEach(tab => {",
         "document.querySelectorAll('.tab-button').forEach(function(tab) {"),

        # Object.keys pattern
        ("Object.keys(dataCache.lastUpdate).forEach(key => {",
         "Object.keys(dataCache.lastUpdate).forEach(function(key) {"),

        ("Object.keys(this.charts).forEach(canvasId => {",
         "Object.keys(this.charts).forEach(function(canvasId) {"),

        # Simple array methods
        ("alerts.forEach(alert => {",
         "alerts.forEach(function(alert) {"),

        ("legacyIndicators.forEach(indicator => {",
         "legacyIndicators.forEach(function(indicator) {"),

        ("timelineData.timeline_data.forEach(assessment => {",
         "timelineData.timeline_data.forEach(function(assessment) {"),

        ("Object.keys(aggregatedData).sort().forEach(date => {",
         "Object.keys(aggregatedData).sort().forEach(function(date) {"),

        ("models.forEach(model => {",
         "models.forEach(function(model) {"),

        ("modelList.forEach(model => {",
         "modelList.forEach(function(model) {"),

        ("rankings.forEach(ranking => {",
         "rankings.forEach(function(ranking) {"),

        # setTimeout/setInterval patterns
        ("updateInterval = setInterval(() => {",
         "updateInterval = setInterval(function() {"),

        ("setTimeout(() => {",
         "setTimeout(function() {"),

        # Map functions
        ("const backgroundColors = data.models.map(model => {",
         "const backgroundColors = data.models.map(function(model) {"),

        ("models.forEach((model, index) => {",
         "models.forEach(function(model, index) {"),

        ("rankings.forEach((ranking, index) => {",
         "rankings.forEach(function(ranking, index) {"),

        # Template literal map functions
        ("tbody.innerHTML = data.top_skills.map(skill => '",
         "tbody.innerHTML = data.top_skills.map(function(skill) { return '"),

        ("tbody.innerHTML = data.top_agents.map(agent => '",
         "tbody.innerHTML = data.top_agents.map(function(agent) { return '"),

        ("tbody.innerHTML = activities.map(activity => {",
         "tbody.innerHTML = activities.map(function(activity) {"),

        ("tbody.innerHTML = data.records.map(record => {",
         "tbody.innerHTML = data.records.map(function(record) {"),

        # Summary functions
        ("summaryHtml += taskTypes.map(([type, stats]) =>",
         "summaryHtml += taskTypes.map(function([type, stats])"),

        ("findingsList.innerHTML = data.findings.map(finding =>",
         "findingsList.innerHTML = data.findings.map(function(finding)"),

        ("recommendationsList.innerHTML = data.recommendations.map(rec =>",
         "recommendationsList.innerHTML = data.recommendations.map(function(rec)"),

        # Chart data patterns
        ("labels: data.trend_data.map(function(d => d.display_time))",
         "labels: data.trend_data.map(function(d) { return d.display_time })"),

        ("labels: data.distribution.map(function(d => d.task_type))",
         "labels: data.distribution.map(function(d) { return d.task_type })"),
    ]

    for old_pattern, new_pattern in arrow_patterns:
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            fixes_applied += 1
            print(f"Applied fix {fixes_applied}: {old_pattern[:50]}...")

    # Generic regex replacements for any remaining arrow functions
    import re

    # Replace pattern: (param) => { expression }
    content = re.sub(r'\(([^)]+)\)\s*=>\s*\{([^}]*)\}', r'function(\1) { \2 }', content)

    # Replace pattern: param => { expression }
    content = re.sub(r'(\w+)\s*=>\s*\{([^}]*)\}', r'function(\1) { \2 }', content)

    # Replace pattern: (param) => expression
    content = re.sub(r'\(([^)]+)\)\s*=>\s*([^,\n\}]+)', r'function(\1) { return \2; }', content)

    # Replace pattern: param => expression
    content = re.sub(r'(\w+)\s*=>\s*([^,\n\}]+)', r'function(\1) { return \2; }', content)

    # Write the fixed content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    final_count = content.count('=>')
    print(f'After fix  - Arrow functions: {final_count}')
    print(f'Applied {fixes_applied} specific fixes')

    if final_count == 0:
        print('SUCCESS: All arrow functions have been resolved!')
    else:
        print(f'WARNING: {final_count} arrow functions remain')

    return content != original_content

if __name__ == '__main__':
    fix_remaining_arrows()