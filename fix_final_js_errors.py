#!/usr/bin/env python3
"""
Fix the final 6 JavaScript errors identified by the debugger
"""

def fix_final_errors():
    file_path = 'D:\\Git\\Werapol\\AutonomousAgent\\.claude-patterns\\dashboard.py'

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    fixes_applied = 0

    print("Fixing final JavaScript errors...")

    # Fix the remaining 6 arrow function errors
    final_fixes = [
        # Fix 1: models.forEach with parameters
        ("models.forEach((model, index) => {",
         "models.forEach(function(model, index) {"),

        # Fix 2: data.top_skills.map (line 3434)
        ("tbody.innerHTML = data.top_skills.map(skill => '",
         "tbody.innerHTML = data.top_skills.map(function(skill) { return '"),

        # Fix 3: data.top_agents.map (line 3446)
        ("tbody.innerHTML = data.top_agents.map(agent => '",
         "tbody.innerHTML = data.top_agents.map(function(agent) { return '"),

        # Fix 4: taskTypes.map with destructuring (line 3617)
        ("summaryHtml += taskTypes.map(([type, stats]) =>",
         "summaryHtml += taskTypes.map(function(arr) { const [type, stats] = arr; return"),

        # Fix 5: data.findings.map (line 3669)
        ("findingsList.innerHTML = data.findings.map(finding =>",
         "findingsList.innerHTML = data.findings.map(function(finding) { return"),

        # Fix 6: data.recommendations.map (line 3678)
        ("recommendationsList.innerHTML = data.recommendations.map(rec =>",
         "recommendationsList.innerHTML = data.recommendations.map(function(rec) { return"),
    ]

    for old_pattern, new_pattern in final_fixes:
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            fixes_applied += 1
            print(f"Fixed: {old_pattern[:50]}...")

    # Write back if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\nApplied {fixes_applied} final fixes to dashboard.py")
        return True
    else:
        print("No final fixes needed")
        return False

if __name__ == '__main__':
    fix_final_errors()