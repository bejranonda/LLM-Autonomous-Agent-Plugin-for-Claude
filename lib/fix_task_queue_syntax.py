#!/usr/bin/env python3
"""
Quick fix for task_queue.py syntax issues
"""

import sys
from pathlib import Path

def fix_task_queue():
    """Fix syntax issues in task_queue.py"""
    task_queue_path = Path("lib/task_queue.py")

    if not task_queue_path.exists():
        print("task_queue.py not found")
        return False

    # Read the content
    content = task_queue_path.read_text(encoding='utf-8')

    # Fix common syntax issues
    content = content.replace('""Create queue directory', '"""Create queue directory')
    content = content.replace('""Unix file locking', '"""Unix file locking')
    content = content.replace('""Unix file unlocking', '"""Unix file unlocking')
    content = content.replace('""Read task queue', '"""Read task queue')
    content = content.replace('""Write task queue', '"""Write task queue')

    # Fix duplicate return
    content = content.replace('return []\n            return []', 'return []')

    # Fix broken try block
    content = content.replace('    try:\n            with open(self.queue_file', '    try:\n            with open(self.queue_file')

    # Fix missing try block
    content = content.replace('lock_file(f, exclusive=True)\n    try: json.dump', 'lock_file(f, exclusive=True)\n                try:\n                    json.dump')

    # Fix duplicate json.dump
    content = content.replace('json.dump(queue, f, indent=2, ensure_ascii=False)\n                    json.dump(queue, f, indent=2, ensure_ascii=False)',
                             'json.dump(queue, f, indent=2, ensure_ascii=False)')

    # Fix except block
    content = content.replace('        except Exception as e: print(fError writing queue: {e"}", file=sys.stderr)',
                             '                except Exception as e:\n                    print(f"Error writing queue: {e}", file=sys.stderr)\n                    unlock_file(f)\n            except Exception as e:\n                print(f"Error writing queue: {e}", file=sys.stderr)')

    # Fix missing except block
    content = content.replace('                unlock_file(f)\n        except Exception as e: print(fError writing queue: {e"}", file=sys.stderr)\n            raise',
                             '                    unlock_file(f)\n                except Exception as e:\n                    print(f"Error writing queue: {e}", file=sys.stderr)\n                    unlock_file(f)\n            except Exception as e:\n                print(f"Error writing queue: {e}", file=sys.stderr)\n                raise')

    # Write back
    task_queue_path.write_text(content, encoding='utf-8')

    # Test syntax
    try:
        compile(content, str(task_queue_path), 'exec')
        print("[OK] task_queue.py syntax fixed successfully")
        return True
    except SyntaxError as e:
        print(f"[ERROR] Syntax error still exists: {e}")
        return False

if __name__ == "__main__":
    success = fix_task_queue()
    sys.exit(0 if success else 1)