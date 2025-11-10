#!/usr/bin/env python3
"""
Fix the specific template literal error at line 1827
"""

def fix_line_1827():
    file_path = 'D:\\Git\\Werapol\\AutonomousAgent\\.claude-patterns\\dashboard.py'

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print("Fixing template literal error at line 1827...")
    original_content = content
    fixes_applied = 0

    # Fix the specific CSV export template literal issues
    # These are causing the JavaScript syntax errors around line 1827
    csv_fixes = [
        # Replace problematic template literals with regular strings
        ("csvContent += `Token Savings,", "csvContent += 'Token Savings,' + (document.getElementById('token-savings')?.textContent || '0') + '\\n';"),
        ("csvContent += `Compression Ratio,", "csvContent += 'Compression Ratio,' + (document.getElementById('compression-ratio')?.textContent || '0%') + '\\n';"),
        ("csvContent += `Cost Savings,", "csvContent += 'Cost Savings,' + (document.getElementById('cost-savings')?.textContent || '$0') + '\\n';"),
        ("csvContent += `Cache Hit Rate,", "csvContent += 'Cache Hit Rate,' + (document.getElementById('cache-hit-rate')?.textContent || '0%') + '\\n';"),
        ("csvContent += `Performance,Overall Score,", "csvContent += 'Performance,Overall Score,' + (document.getElementById('overall-score')?.textContent || '0') + '\\n';"),
        ("csvContent += `Performance,Quality Score,", "csvContent += 'Performance,Quality Score,' + (document.getElementById('kpi-quality')?.textContent || '0') + '\\n';"),
        ("csvContent += `Performance,Success Rate,", "csvContent += 'Performance,Success Rate,' + (document.getElementById('kpi-success')?.textContent || '0') + '\\n';"),
        ("csvContent += `Performance,Efficiency,", "csvContent += 'Performance,Efficiency,' + (document.getElementById('kpi-efficiency')?.textContent || '0') + '\\n';"),
        ("csvContent += `Business,Business Score,", "csvContent += 'Business,Business Score,' + (document.getElementById('business-score')?.textContent || '0') + '\\n';"),
        ("csvContent += `Data Integrity,Consistency Score,", "csvContent += 'Data Integrity,Consistency Score,' + (document.getElementById('consistency-score')?.textContent || '0') + '\\n';"),
        ("csvContent += `Data Integrity,Missing Records,", "csvContent += 'Data Integrity,Missing Records,' + (document.getElementById('missing-records')?.textContent || '0') + '\\n';"),
        ("csvContent += `Data Integrity,Inconsistent Data,", "csvContent += 'Data Integrity,Inconsistent Data,' + (document.getElementById('inconsistent-data')?.textContent || '0') + '\\n';"),
        ("csvContent += `Data Integrity,Validation Errors,", "csvContent += 'Data Integrity,Validation Errors,' + (document.getElementById('validation-errors')?.textContent || '0') + '\\n';"),
    ]

    for start_pattern, replacement in csv_fixes:
        # Find lines starting with the pattern and replace the entire problematic line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if start_pattern in line and '`' in line:
                # This line likely has an unclosed template literal
                lines[i] = replacement
                fixes_applied += 1
                print(f"Fixed line {i+1}: {line[:50]}...")
                break
        content = '\n'.join(lines)

    # Write back if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\nApplied {fixes_applied} fixes for line 1827 template literal errors")
        return True
    else:
        print("No template literal fixes needed")
        return False

if __name__ == '__main__':
    fix_line_1827()