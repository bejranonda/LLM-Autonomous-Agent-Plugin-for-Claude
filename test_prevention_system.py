#!/usr/bin/env python3
"""
Test script for the comprehensive prevention system
"""

import sys
from pathlib import Path

# Test the core functionality
def test_command_validation():
    """Test command validation system"""
    print("Testing Command Validation System...")

    try:
        from lib.command_validator import CommandValidator
        validator = CommandValidator(".")

        # Check critical commands
        expected_commands = {
            "dev": ["auto", "release", "model-switch", "pr-review"],
            "analyze": ["project", "quality", "static", "dependencies"],
            "validate": ["all", "fullstack", "plugin", "patterns"],
            "monitor": ["recommend", "dashboard"],
            "debug": ["eval", "gui"],
            "learn": ["init", "analytics", "performance", "predict"],
            "workspace": ["organize", "reports", "improve"]
        }

        missing_critical = []
        total_expected = 0
        total_found = 0

        for category, commands in expected_commands.items():
            category_path = Path(f"commands/{category}")
            for cmd in commands:
                total_expected += 1
                cmd_file = category_path / f"{cmd}.md"
                if cmd_file.exists():
                    total_found += 1
                else:
                    missing_critical.append(f"/{category}:{cmd}")

        success_rate = (total_found / total_expected) * 100 if total_expected > 0 else 0

        print(f"  Expected Commands: {total_expected}")
        print(f"  Found Commands: {total_found}")
        print(f"  Missing Critical: {len(missing_critical)}")
        print(f"  Success Rate: {success_rate:.1f}%")

        if missing_critical:
            print(f"  Missing Commands:")
            for cmd in missing_critical:
                print(f"    - {cmd}")

        return success_rate >= 95

    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def test_file_structure():
    """Test file structure integrity"""
    print("\nTesting File Structure Integrity...")

    required_structure = [
        "commands/",
        "agents/",
        "skills/",
        ".claude-plugin/",
        "lib/",
        "patterns/"
    ]

    missing_dirs = []
    for dir_path in required_structure:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)

    print(f"  Required Directories: {len(required_structure)}")
    print(f"  Missing Directories: {len(missing_dirs)}")

    if missing_dirs:
        print(f"  Missing:")
        for dir_path in missing_dirs:
            print(f"    - {dir_path}")

    return len(missing_dirs) == 0

def test_lib_components():
    """Test library components"""
    print("\nTesting Library Components...")

    lib_files = [
        "lib/backup_manager.py",
        "lib/command_validator.py",
        "lib/recovery_manager.py",
        "lib/validation_hooks.py",
        "lib/dashboard.py"
    ]

    missing_libs = []
    for lib_file in lib_files:
        if not Path(lib_file).exists():
            missing_libs.append(lib_file)

    print(f"  Expected Library Files: {len(lib_files)}")
    print(f"  Found Library Files: {len(lib_files) - len(missing_libs)}")
    print(f"  Missing Library Files: {len(missing_libs)}")

    if missing_libs:
        print(f"  Missing:")
        for lib_file in missing_libs:
            print(f"    - {lib_file}")

    return len(missing_libs) == 0

def test_validation_commands():
    """Test validation commands"""
    print("\nTesting Validation Commands...")

    validation_commands = [
        "commands/validate/integrity.md",
        "commands/validate/commands.md",
        "commands/monitor/dashboard.md"
    ]

    missing_commands = []
    for cmd_file in validation_commands:
        if not Path(cmd_file).exists():
            missing_commands.append(cmd_file)

    print(f"  Expected Validation Commands: {len(validation_commands)}")
    print(
    f"  Found Validation Commands: {len(validation_commands) - len(missing_commands)}",
)
    print(f"  Missing Validation Commands: {len(missing_commands)}")

    if missing_commands:
        print(f"  Missing:")
        for cmd_file in missing_commands:
            print(f"    - {cmd_file}")

    return len(missing_commands) == 0

def test_missing_command_recovery():
    """Test missing command recovery"""
    print("\nTesting Missing Command Recovery...")

    try:
        sys.path.append('lib')
        from recovery_manager import RecoveryManager
        recovery_manager = RecoveryManager(".")

        # Test recovery for missing command
        test_component = {
            "type": "command",
            "path": "commands/monitor/dashboard.md",
            "critical": True,
            "category": "monitor",
            "name": "dashboard"
        }

        # This should succeed since we just created the dashboard command
        result = recovery_manager.recover_specific_component(test_component["type"], test_component["path"])

        print(f"  Recovery Success: {result['success']}")
        if 'strategy_used' in result:
            print(f"  Strategy Used: {result['strategy_used']}")
        if 'error' in result:
            print(f"  Recovery Error: {result['error']}")

        return result['success'] or result.get('error', '').find('already exists') >= 0

    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("COMPREHENSIVE PREVENTION SYSTEM TEST")
    print("=" * 60)

    tests = [
        ("Command Validation", test_command_validation),
        ("File Structure", test_file_structure),
        ("Library Components", test_lib_components),
        ("Validation Commands", test_validation_commands),
        ("Missing Command Recovery", test_missing_command_recovery)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ERROR in {test_name}: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:.<25} {status}")
        if result:
            passed += 1

    print(f"\nTests Passed: {passed}/{len(results)}")
    print(f"Success Rate: {(passed/len(results))*100:.1f}%")

    if passed == len(results):
        print("\n[SUCCESS] All prevention system tests passed!")
        return 0
    else:
        print(
    f"\n[WARNING] {len(results) - passed} tests failed. Review the issues above.",
)
        return 1

if __name__ == "__main__":
    sys.exit(main())
