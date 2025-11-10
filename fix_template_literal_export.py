#!/usr/bin/env python3
"""
Fix template literal issues in CSV export functionality causing JavaScript errors
"""

def fix_csv_template_literals():
    file_path = 'D:\\Git\\Werapol\\AutonomousAgent\\.claude-patterns\\dashboard.py'

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print("Fixing CSV export template literal issues...")

    original_content = content
    fixes_applied = 0

    # Fix 1: Replace unclosed template literals in CSV export (lines around 1827-1863)
    csv_patterns = [
        # Replace problematic template literals with string concatenation
        ("csvContent += `Token Savings,${document.getElementById('token-savings')?.textContent || '0'}\\n`",
         "csvContent += 'Token Savings,' + (document.getElementById('token-savings')?.textContent || '0') + '\\n';"),

        ("csvContent += `Compression Ratio,${document.getElementById('compression-ratio')?.textContent || '0%'}\\n`",
         "csvContent += 'Compression Ratio,' + (document.getElementById('compression-ratio')?.textContent || '0%') + '\\n';"),

        ("csvContent += `Cost Savings,${document.getElementById('cost-savings')?.textContent || '$0'}\\n`",
         "csvContent += 'Cost Savings,' + (document.getElementById('cost-savings')?.textContent || '$0') + '\\n';"),

        ("csvContent += `Cache Hit Rate,${document.getElementById('cache-hit-rate')?.textContent || '0%'}\\n`",
         "csvContent += 'Cache Hit Rate,' + (document.getElementById('cache-hit-rate')?.textContent || '0%') + '\\n';"),

        ("csvContent += `Performance,Overall Score,${document.getElementById('overall-score')?.textContent || '0'}\\n`",
         "csvContent += 'Performance,Overall Score,' + (document.getElementById('overall-score')?.textContent || '0') + '\\n';"),

        ("csvContent += `Performance,Quality Score,${document.getElementById('kpi-quality')?.textContent || '0'}\\n`",
         "csvContent += 'Performance,Quality Score,' + (document.getElementById('kpi-quality')?.textContent || '0') + '\\n';"),

        ("csvContent += `Performance,Success Rate,${document.getElementById('kpi-success')?.textContent || '0'}\\n`",
         "csvContent += 'Performance,Success Rate,' + (document.getElementById('kpi-success')?.textContent || '0') + '\\n';"),

        ("csvContent += `Performance,Efficiency,${document.getElementById('kpi-efficiency')?.textContent || '0'}\\n`",
         "csvContent += 'Performance,Efficiency,' + (document.getElementById('kpi-efficiency')?.textContent || '0') + '\\n';"),

        ("csvContent += `Business,Business Score,${document.getElementById('business-score')?.textContent || '0'}\\n`",
         "csvContent += 'Business,Business Score,' + (document.getElementById('business-score')?.textContent || '0') + '\\n';"),

        ("csvContent += `Data Integrity,Consistency Score,${document.getElementById('consistency-score')?.textContent || '0'}\\n`",
         "csvContent += 'Data Integrity,Consistency Score,' + (document.getElementById('consistency-score')?.textContent || '0') + '\\n';"),

        ("csvContent += `Data Integrity,Missing Records,${document.getElementById('missing-records')?.textContent || '0'}\\n`",
         "csvContent += 'Data Integrity,Missing Records,' + (document.getElementById('missing-records')?.textContent || '0') + '\\n';"),

        ("csvContent += `Data Integrity,Inconsistent Data,${document.getElementById('inconsistent-data')?.textContent || '0'}\\n`",
         "csvContent += 'Data Integrity,Inconsistent Data,' + (document.getElementById('inconsistent-data')?.textContent || '0') + '\\n';"),

        ("csvContent += `Data Integrity,Validation Errors,${document.getElementById('validation-errors')?.textContent || '0'}\\n`",
         "csvContent += 'Data Integrity,Validation Errors,' + (document.getElementById('validation-errors')?.textContent || '0') + '\\n';"),
    ]

    for old_pattern, new_pattern in csv_patterns:
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            fixes_applied += 1
            print(f"Fixed CSV template literal: {old_pattern[:50]}...")

    # Fix 2: Replace arrow functions with traditional functions
    arrow_fixes = [
        ("document.querySelectorAll('.dashboard-section').forEach(section => {",
         "document.querySelectorAll('.dashboard-section').forEach(function(section) {"),

        ("document.querySelectorAll('.tab-button').forEach(tab => {",
         "document.querySelectorAll('.tab-button').forEach(function(tab) {"),

        ("alerts.forEach(alert => {",
         "alerts.forEach(function(alert) {"),

        ("Object.keys(dataCache.lastUpdate).forEach(key => {",
         "Object.keys(dataCache.lastUpdate).forEach(function(key) {"),

        ("Object.keys(this.charts).forEach(canvasId => {",
         "Object.keys(this.charts).forEach(function(canvasId) {"),
    ]

    for old_arrow, new_arrow in arrow_fixes:
        if old_arrow in content:
            content = content.replace(old_arrow, new_arrow)
            fixes_applied += 1
            print(f"Fixed arrow function: {old_arrow[:50]}...")

    # Write back if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\nApplied {fixes_applied} fixes to dashboard.py")
        return True
    else:
        print("No fixes needed")
        return False

if __name__ == '__main__':
    fix_csv_template_literals()