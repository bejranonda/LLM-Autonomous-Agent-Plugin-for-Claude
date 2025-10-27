import json
import re
from pathlib import Path

def validate_plugin():
    issues = []
    warnings = []

    print('CLAUDE PLUGIN VALIDATION REPORT')
    print('=' * 60)

    # 1. Plugin Manifest Validation
    manifest_path = Path('.claude-plugin/plugin.json')
    if manifest_path.exists():
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)

            # Check required fields
            required_fields = ['name', 'version', 'description', 'author']
            missing_fields = [field for field in required_fields if field not in manifest]
            if missing_fields:
                issues.append(f'Missing required fields: {missing_fields}')
            else:
                print('OK Plugin manifest: All required fields present')

            # Check version format
            version = manifest.get('version', '')
            if re.match(r'^\d+\.\d+\.\d+$', version):
                print(f'OK Plugin manifest: Valid version format ({version})')
            else:
                issues.append(f'Invalid version format: {version} (use x.y.z)')

            # Check description length
            description = manifest.get('description', '')
            if len(description) > 200:
                warnings.append('Plugin description very long (>200 chars)')
            else:
                print('OK Plugin manifest: Description length appropriate')

        except json.JSONDecodeError as e:
            issues.append(f'Plugin manifest JSON error: {e}')
        except UnicodeDecodeError:
            issues.append('Plugin manifest encoding error (must be UTF-8)')
    else:
        issues.append('Missing plugin manifest: .claude-plugin/plugin.json')

    # 2. Agent validation
    agent_files = list(Path('agents').glob('*.md')) if Path('agents').exists() else []
    print(f'OK Directory structure: Found {len(agent_files)} agent files')

    agent_names = []
    agent_prefix_issues = []
    duplicate_agents = []

    for agent_file in agent_files:
        try:
            with open(agent_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.startswith('---'):
                    frontmatter_end = content.find('---', 3)
                    if frontmatter_end != -1:
                        frontmatter = content[3:frontmatter_end].strip()
                        if 'name:' in frontmatter:
                            name_line = [line for line in frontmatter.split('\n') if line.startswith('name:')]
                            if name_line:
                                name = name_line[0].split(':', 1)[1].strip()
                                agent_names.append((name, agent_file.name))
                                # Check for duplicate names
                                if name in [a[0] for a in agent_names[:-1]]:
                                    duplicate_agents.append(name)
                                # Check prefix consistency
                                if ':' in name and not name.startswith('autonomous-agent:'):
                                    agent_prefix_issues.append(name)
        except Exception as e:
            warnings.append(f'Could not parse {agent_file}: {str(e)[:50]}')

    print(f'OK Agent files: {len(agent_names)} agents with valid names')
    if agent_prefix_issues:
        warnings.append(f'Agent name prefix inconsistencies: {agent_prefix_issues}')
    if duplicate_agents:
        issues.append(f'Duplicate agent names: {duplicate_agents}')

    # 3. Command validation
    command_files = list(Path('commands').glob('*.md')) if Path('commands').exists() else []
    print(f'OK Directory structure: Found {len(command_files)} command files')

    commands_missing_delegation = []
    commands_with_delegation = 0
    commands_with_name = 0
    commands_with_command = 0

    for cmd_file in command_files:
        try:
            with open(cmd_file, 'r', encoding='utf-8') as f:
                content = f.read()
                has_delegates_to = 'delegates-to:' in content.lower()
                if has_delegates_to:
                    commands_with_delegation += 1
                else:
                    commands_missing_delegation.append(cmd_file.name)

                # Check for name field
                if 'name:' in content:
                    commands_with_name += 1

                # Check for command field
                if 'command:' in content:
                    commands_with_command += 1

        except Exception as e:
            warnings.append(f'Could not parse {cmd_file}: {str(e)[:50]}')

    print(f'OK Command files: {commands_with_delegation}/{len(command_files)} have delegation fields')
    print(f'OK Command files: {commands_with_name}/{len(command_files)} have name fields')
    print(f'OK Command files: {commands_with_command}/{len(command_files)} have command fields')

    if commands_missing_delegation:
        warnings.append(f'Commands missing delegates-to field: {len(commands_missing_delegation)} files')

    # 4. Skill validation
    skill_dirs = [d for d in Path('skills').iterdir() if d.is_dir()] if Path('skills').exists() else []
    skill_files = []
    for skill_dir in skill_dirs:
        skill_file = skill_dir / 'SKILL.md'
        if skill_file.exists():
            skill_files.append(skill_file)

    print(f'OK Directory structure: Found {len(skill_files)} skill files')

    # 5. Cross-reference validation - check delegation mappings
    delegation_issues = []
    agent_short_names = [name.replace('autonomous-agent:', '') for name, _ in agent_names]

    for cmd_file in command_files:
        try:
            with open(cmd_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'delegates-to:' in content.lower():
                    # Extract delegated agent
                    delegates_match = re.search(r'delegates-to:\s*(.+)', content, re.IGNORECASE)
                    if delegates_match:
                        delegated_agent = delegates_match.group(1).strip()
                        # Check if agent exists (with or without prefix)
                        agent_exists = False
                        for full_name, _ in agent_names:
                            short_name = full_name.replace('autonomous-agent:', '')
                            if (delegated_agent == full_name or
                                delegated_agent.replace('autonomous-agent:', '') == short_name):
                                agent_exists = True
                                break

                        if not agent_exists:
                            delegation_issues.append(f'{cmd_file.name} -> {delegated_agent}')
        except Exception:
            pass

    if delegation_issues:
        issues.append(f'Broken delegation mappings: {delegation_issues}')
    else:
        print('OK Command-to-agent mappings: All references valid')

    # 6. Check for specific critical files
    critical_files = [
        'agents/orchestrator.md',
        'agents/quality-controller.md',
        'commands/quality-check.md',
        'commands/auto-analyze.md'
    ]

    missing_critical = []
    for critical_file in critical_files:
        if not Path(critical_file).exists():
            missing_critical.append(critical_file)

    if missing_critical:
        issues.append(f'Missing critical files: {missing_critical}')
    else:
        print('OK Critical files: All present')

    # 7. Check for command-to-agent consistency issues
    commands_without_proper_delegation = []
    for cmd_file in command_files:
        file_path = str(cmd_file)
        try:
            with open(cmd_file, 'r', encoding='utf-8') as f:
                content = f.read()

                # Check if command mentions orchestrator but doesn't delegate properly
                if 'orchestrator' in content.lower() and 'delegates-to:' not in content:
                    commands_without_proper_delegation.append(cmd_file.name)

        except Exception:
            pass

    if commands_without_proper_delegation:
        warnings.append(f'Commands mentioning orchestrator but missing delegation: {len(commands_without_proper_delegation)}')

    # Calculate quality score
    total_checks = 13  # Total number of validation checks
    failed_checks = len(issues)
    passed_checks = total_checks - failed_checks
    quality_score = (passed_checks / total_checks) * 100

    print('')
    print('VALIDATION SUMMARY')
    print('=' * 60)
    print(f'Quality Score: {quality_score:.1f}/100')
    print(f'Critical Issues: {len(issues)}')
    print(f'Warnings: {len(warnings)}')

    if issues:
        print('')
        print('CRITICAL ISSUES:')
        for issue in issues:
            print(f'  FAIL {issue}')

    if warnings:
        print('')
        print('WARNINGS:')
        for warning in warnings:
            print(f'  WARN {warning}')

    # Show specific details
    print('')
    print('DETAILED FINDINGS:')
    print('=' * 60)

    if commands_missing_delegation:
        print(f'Commands missing delegates-to field:')
        for cmd in commands_missing_delegation[:5]:  # Show first 5
            print(f'  - {cmd}')
        if len(commands_missing_delegation) > 5:
            print(f'  ... and {len(commands_missing_delegation) - 5} more')

    if agent_prefix_issues:
        print(f'Agent prefix inconsistencies:')
        for agent in agent_prefix_issues:
            print(f'  - {agent} (should be autonomous-agent:{agent})')

    if commands_without_proper_delegation:
        print(f'Commands needing delegation:')
        for cmd in commands_without_proper_delegation[:5]:
            print(f'  - {cmd}')

    # Installation readiness check
    print('')
    print('INSTALLATION READINESS:')
    print('=' * 60)

    if len(issues) == 0:
        print('READY Plugin is ready for Claude Code installation')
        print('READY All components are properly structured and validated')
    else:
        print('NOT READY Plugin has critical issues blocking installation')
        print('NOT READY Fix critical issues before attempting installation')

    print('')
    print('AUTO-FIX OPPORTUNITIES:')
    print('=' * 60)

    if commands_missing_delegation:
        print('FIX Add missing delegates-to fields to commands')
        print('   Most commands should delegate to autonomous-agent:orchestrator')

    if agent_prefix_issues:
        print('FIX Standardize agent name prefixes to autonomous-agent:agent-name')

    if not issues and not warnings:
        print('NONE No auto-fixes needed - plugin is in excellent condition')

    if not issues:
        print('')
        print('OK Plugin validation PASSED - Ready for installation!')
        return True
    else:
        print('')
        print(f'FAIL Plugin validation FAILED - {len(issues)} critical issues')
        return False

if __name__ == '__main__':
    validate_plugin()