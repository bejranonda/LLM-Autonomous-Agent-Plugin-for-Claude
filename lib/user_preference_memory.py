#!/usr/bin/env python3
"""
User Preference Memory System for Autonomous Agent Plugin

Captures, stores, and learns from user preferences and system environments
to provide personalized development guidance and intelligent suggestions.

Features:
- User preference storage with cross-platform compatibility
- System environment detection and fingerprinting
- Intelligent suggestion generation based on preferences
- Pattern learning from user choices and behaviors
- Cross-project preference synchronization
- Privacy-first design with optional data sharing

Version: 1.0.0
Author: Autonomous Agent Development Team
"""

import json
import sys
import threading
import time
import shutil
import platform
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Callable
from collections import defaultdict
import psutil
import os

# Handle Windows compatibility for file locking
if platform.system() == 'Windows':
    import msvcrt

    def lock_file(f, exclusive=False):
        """Windows file locking using msvcrt."""
        msvcrt.locking(f.fileno(), msvcrt.LK_LOCK if exclusive else msvcrt.LK_NBLCK, 1)

    def unlock_file(f):
        """Windows file unlocking."""
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        except:
            pass
else:
    import fcntl

    def lock_file(f, exclusive=False):
        """Unix file locking using fcntl."""
        fcntl.flock(f.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)

    def unlock_file(f):
        """Unix file unlocking."""
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)


class SystemProfiler:
    """Comprehensive system environment detection and profiling."""

    def __init__(self):
        self.profile_cache = {}
        self.cache_ttl = 3600  # 1 hour cache

    def get_system_fingerprint(self) -> Dict[str, Any]:
        """
        Generate comprehensive system fingerprint for environment identification.

        Returns:
            Dictionary containing system environment details
        """
        current_time = time.time()

        # Check cache
        if (self.profile_cache and
            current_time - self.profile_cache.get('timestamp', 0) < self.cache_ttl):
            return self.profile_cache.get('fingerprint', {})

        fingerprint = {
            "timestamp": current_time,
            "system": self._get_system_info(),
            "hardware": self._get_hardware_info(),
            "development": self._get_development_environment(),
            "preferences": self._detect_user_preferences(),
            "capabilities": self._assess_system_capabilities()
        }

        # Cache result
        self.profile_cache = {
            'fingerprint': fingerprint,
            'timestamp': current_time
        }

        return fingerprint

    def _get_system_info(self) -> Dict[str, Any]:
        """Get basic system information."""
        return {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "hostname": platform.node(),
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "os_type": os.name
        }

    def _get_hardware_info(self) -> Dict[str, Any]:
        """Get hardware information."""
        try:
            # CPU information
            cpu_info = {
                "cores": psutil.cpu_count(logical=True),
                "physical_cores": psutil.cpu_count(logical=False),
                "frequency": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
                "usage_percent": psutil.cpu_percent(interval=1)
            }

            # Memory information
            memory = psutil.virtual_memory()
            memory_info = {
                "total_gb": round(memory.total / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "usage_percent": memory.percent,
                "used_gb": round(memory.used / (1024**3), 2)
            }

            # Disk information
            disk = psutil.disk_usage('/')
            disk_info = {
                "total_gb": round(disk.total / (1024**3), 2),
                "used_gb": round(disk.used / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "usage_percent": round((disk.used / disk.total) * 100, 2)
            }

            return {
                "cpu": cpu_info,
                "memory": memory_info,
                "disk": disk_info,
                "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat()
            }

        except Exception as e:
            return {"error": f"Hardware detection failed: {e}"}

    def _get_development_environment(self) -> Dict[str, Any]:
        """Detect development environment and tools."""
        dev_env = {
            "installed_tools": self._detect_installed_tools(),
            "preferred_editors": self._detect_editors(),
            "shell": os.environ.get('SHELL', 'unknown'),
            "path_directories": os.environ.get('PATH', '').split(os.pathsep)[:10],  # First 10
            "env_variables": self._get_relevant_env_vars()
        }

        return dev_env

    def _detect_installed_tools(self) -> Dict[str, str]:
        """Detect common development tools and their versions."""
        tools = {
            'git': self._get_tool_version('git --version'),
            'node': self._get_tool_version('node --version'),
            'npm': self._get_tool_version('npm --version'),
            'python': self._get_tool_version('python --version'),
            'pip': self._get_tool_version('pip --version'),
            'docker': self._get_tool_version('docker --version'),
            'vscode': self._detect_vscode(),
            'git': self._get_tool_version('git --version')
        }

        # Filter out tools that aren't installed
        return {k: v for k, v in tools.items() if v and 'not found' not in v.lower()}

    def _get_tool_version(self, command: str) -> Optional[str]:
        """Get version of a command-line tool."""
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return None

    def _detect_vscode(self) -> Optional[str]:
        """Detect Visual Studio Code installation."""
        try:
            if platform.system() == 'Windows':
                vscode_path = r'C:\Program Files\Microsoft VS Code\bin\code.cmd'
                if os.path.exists(vscode_path):
                    result = subprocess.run([vscode_path, '--version'],
                                          capture_output=True, text=True, timeout=5)
                    return result.stdout.strip() if result.returncode == 0 else None
            else:
                return self._get_tool_version('code --version')
        except:
            return None

    def _detect_editors(self) -> List[str]:
        """Detect preferred text editors."""
        editors = []

        # Check environment variables
        editor_vars = ['EDITOR', 'VISUAL']
        for var in editor_vars:
            if var in os.environ:
                editors.append(os.environ[var])

        # Check for common editors
        common_editors = ['code', 'vim', 'nano', 'emacs', 'subl', 'atom']
        for editor in common_editors:
            if self._get_tool_version(f'{editor} --version') or shutil.which(editor):
                editors.append(editor)

        return list(set(editors))  # Remove duplicates

    def _get_relevant_env_vars(self) -> Dict[str, str]:
        """Get development-relevant environment variables."""
        relevant_vars = [
            'HOME', 'USER', 'USERNAME', 'USERPROFILE',
            'PATH', 'SHELL', 'TERM', 'LANG', 'LC_ALL',
            'PYTHONPATH', 'NODE_PATH', 'JAVA_HOME',
            'DOCKER_HOST', 'GIT_SSH', 'SSH_AUTH_SOCK'
        ]

        return {var: os.environ.get(var, '') for var in relevant_vars if var in os.environ}

    def _detect_user_preferences(self) -> Dict[str, Any]:
        """Detect user preferences from environment."""
        return {
            "timezone": self._detect_timezone(),
            "language": self._detect_language(),
            "git_config": self._get_git_config(),
            "preferred_shell": os.environ.get('SHELL', os.environ.get('COMSPEC', 'unknown')),
            "terminal_preference": self._detect_terminal_preference()
        }

    def _detect_timezone(self) -> str:
        """Detect user's timezone."""
        try:
            import time
            return time.tzname[0] if time.tzname else 'UTC'
        except:
            return 'UTC'

    def _detect_language(self) -> str:
        """Detect system language."""
        import locale
        try:
            return locale.getdefaultlocale()[0] or 'en_US'
        except:
            return 'en_US'

    def _get_git_config(self) -> Dict[str, str]:
        """Get Git configuration."""
        git_config = {}
        try:
            # Get global Git configuration
            result = subprocess.run(
                ['git', 'config', '--global', '--list'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        # Only include non-sensitive config
                        if not any(sensitive in key.lower() for sensitive in ['token', 'password', 'key']):
                            git_config[key] = value
        except:
            pass

        return git_config

    def _detect_terminal_preference(self) -> str:
        """Detect terminal preferences."""
        term = os.environ.get('TERM', '')
        if 'xterm' in term.lower():
            return 'xterm'
        elif 'screen' in term.lower():
            return 'screen'
        elif 'tmux' in term.lower():
            return 'tmux'
        else:
            return term or 'unknown'

    def _assess_system_capabilities(self) -> Dict[str, Any]:
        """Assess system capabilities for development tasks."""
        return {
            "parallel_processing": psutil.cpu_count(logical=True) >= 4,
            "memory_adequate": psutil.virtual_memory().total >= 8 * (1024**3),  # 8GB
            "disk_space_adequate": psutil.disk_usage('/').free >= 10 * (1024**3),  # 10GB
            "virtualization_available": self._check_virtualization(),
            "docker_available": self._get_tool_version('docker --version') is not None,
            "git_available": self._get_tool_version('git --version') is not None
        }

    def _check_virtualization(self) -> bool:
        """Check if virtualization is available."""
        try:
            if platform.system() == 'Linux':
                return os.path.exists('/proc/vz') or os.path.exists('/proc/xen')
            elif platform.system() == 'Windows':
                # Check for Hyper-V or WSL
                try:
                    result = subprocess.run(['systeminfo'], capture_output=True, text=True, timeout=10)
                    return 'Hyper-V' in result.stdout or 'WSL' in result.stdout
                except:
                    return False
            else:
                return False
        except:
            return False


class UserPreferenceMemory:
    """
    User Preference Memory System for storing and learning from user behavior.

    Maintains user preferences, system environment data, and generates
    intelligent suggestions based on patterns and historical data.
    """

    def __init__(self, storage_dir: str = ".claude-preferences"):
        """
        Initialize user preference memory system.

        Args:
            storage_dir: Directory for preference storage
        """
        self.storage_dir = Path(storage_dir)
        self.preferences_file = self.storage_dir / "user_preferences.json"
        self.environment_file = self.storage_dir / "system_environment.json"
        self.suggestions_file = self.storage_dir / "suggestions_history.json"
        self.backup_dir = self.storage_dir / "backups"

        # Thread safety
        self._lock = threading.RLock()
        self._cache = {}
        self._cache_timestamp = 0
        self._cache_ttl = 60  # 1 minute cache

        # System profiler
        self.profiler = SystemProfiler()

        self._ensure_directories()
        self._initialize_storage()

    def _ensure_directories(self):
        """Create necessary directories."""
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def _initialize_storage(self):
        """Initialize storage with default structure if needed."""
        if not self.preferences_file.exists():
            default_preferences = {
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "user_id": self._generate_user_id(),
                "preferences": {
                    "development": {
                        "preferred_languages": [],
                        "frameworks": [],
                        "tools": [],
                        "code_style": {},
                        "testing_preference": "balanced",
                        "documentation_style": "comprehensive"
                    },
                    "workflow": {
                        "auto_save": True,
                        "auto_backup": True,
                        "parallel_execution": True,
                        "quality_threshold": 70,
                        "suggestion_level": "balanced",
                        "notification_level": "important"
                    },
                    "ui": {
                        "theme": "auto",
                        "verbosity": "medium",
                        "show_progress": True,
                        "confirm_destructive": True
                    },
                    "privacy": {
                        "share_patterns": False,
                        "share_analytics": False,
                        "local_storage_only": True,
                        "data_retention_days": 90
                    }
                },
                "learned_patterns": {
                    "command_preferences": {},
                    "agent_effectiveness": {},
                    "skill_success_rates": {},
                    "common_workflows": [],
                    "error_patterns": {}
                },
                "history": {
                    "commands_used": [],
                    "tasks_completed": [],
                    "suggestions_accepted": [],
                    "suggestions_rejected": []
                }
            }
            self._write_preferences(default_preferences)

        if not self.environment_file.exists():
            # Initialize with current system profile
            current_profile = self.profiler.get_system_fingerprint()
            env_data = {
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "profiles": [current_profile],
                "baseline_profile": current_profile,
                "last_profile": current_profile,
                "profile_count": 1
            }
            self._write_environment(env_data)

        if not self.suggestions_file.exists():
            suggestions_data = {
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "suggestions": [],
                "response_rates": {},
                "effectiveness_scores": {}
            }
            self._write_suggestions(suggestions_data)

    def _generate_user_id(self) -> str:
        """Generate a unique user ID based on system fingerprint."""
        import hashlib
        system_info = f"{platform.system()}-{platform.node()}-{platform.machine()}"
        return hashlib.md5(system_info.encode()).hexdigest()[:16]

    def _read_preferences(self, use_cache: bool = True) -> Dict[str, Any]:
        """Read user preferences with caching support."""
        current_time = time.time()

        # Check cache
        if (use_cache and
            'preferences' in self._cache and
            current_time - self._cache_timestamp < self._cache_ttl):
            return self._cache['preferences']

        with self._lock:
            try:
                with open(self.preferences_file, 'r', encoding='utf-8') as f:
                    lock_file(f, exclusive=False)
                    try:
                        data = json.load(f)
                        self._cache['preferences'] = data
                        self._cache_timestamp = current_time
                        return data
                    finally:
                        unlock_file(f)
            except FileNotFoundError:
                self._initialize_storage()
                return self._read_preferences(use_cache)
            except json.JSONDecodeError as e:
                print(f"Error reading preferences: {e}", file=sys.stderr)
                if self._restore_from_backup(self.preferences_file):
                    return self._read_preferences(use_cache)
                return self._get_default_preferences()
            except Exception as e:
                print(f"Error reading preferences: {e}", file=sys.stderr)
                return self._get_default_preferences()

    def _write_preferences(self, data: Dict[str, Any], create_backup: bool = True):
        """Write user preferences with backup support."""
        with self._lock:
            try:
                # Create backup if requested
                if create_backup and self.preferences_file.exists():
                    self._create_backup(self.preferences_file)

                # Update metadata
                data["last_updated"] = datetime.now().isoformat()

                with open(self.preferences_file, 'w', encoding='utf-8') as f:
                    lock_file(f, exclusive=True)
                    try:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                        # Update cache
                        self._cache['preferences'] = data
                        self._cache_timestamp = time.time()
                    finally:
                        unlock_file(f)

            except Exception as e:
                print(f"Error writing preferences: {e}", file=sys.stderr)
                raise

    def _read_environment(self) -> Dict[str, Any]:
        """Read system environment data."""
        with self._lock:
            try:
                with open(self.environment_file, 'r', encoding='utf-8') as f:
                    lock_file(f, exclusive=False)
                    try:
                        return json.load(f)
                    finally:
                        unlock_file(f)
            except (FileNotFoundError, json.JSONDecodeError):
                self._initialize_storage()
                return self._read_environment()
            except Exception as e:
                print(f"Error reading environment data: {e}", file=sys.stderr)
                return {"profiles": [], "baseline_profile": {}, "last_profile": {}}

    def _write_environment(self, data: Dict[str, Any]):
        """Write system environment data."""
        with self._lock:
            try:
                with open(self.environment_file, 'w', encoding='utf-8') as f:
                    lock_file(f, exclusive=True)
                    try:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    finally:
                        unlock_file(f)
            except Exception as e:
                print(f"Error writing environment data: {e}", file=sys.stderr)

    def _read_suggestions(self) -> Dict[str, Any]:
        """Read suggestions history."""
        with self._lock:
            try:
                with open(self.suggestions_file, 'r', encoding='utf-8') as f:
                    lock_file(f, exclusive=False)
                    try:
                        return json.load(f)
                    finally:
                        unlock_file(f)
            except (FileNotFoundError, json.JSONDecodeError):
                self._initialize_storage()
                return self._read_suggestions()
            except Exception as e:
                print(f"Error reading suggestions data: {e}", file=sys.stderr)
                return {"suggestions": [], "response_rates": {}, "effectiveness_scores": {}}

    def _write_suggestions(self, data: Dict[str, Any]):
        """Write suggestions history."""
        with self._lock:
            try:
                with open(self.suggestions_file, 'w', encoding='utf-8') as f:
                    lock_file(f, exclusive=True)
                    try:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    finally:
                        unlock_file(f)
            except Exception as e:
                print(f"Error writing suggestions data: {e}", file=sys.stderr)

    def _create_backup(self, file_path: Path):
        """Create a backup of the specified file."""
        if not file_path.exists():
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"{file_path.stem}_{timestamp}.json"

        try:
            shutil.copy2(file_path, backup_file)
            # Keep only last 5 backups per file type
            self._cleanup_old_backups(file_path.stem)
        except Exception as e:
            print(f"Warning: Failed to create backup: {e}", file=sys.stderr)

    def _cleanup_old_backups(self, file_stem: str):
        """Keep only the most recent backups for a file type."""
        backups = sorted(self.backup_dir.glob(f"{file_stem}_*.json"))
        if len(backups) > 5:
            for old_backup in backups[:-5]:
                try:
                    old_backup.unlink()
                except Exception as e:
                    print(f"Warning: Failed to delete old backup {old_backup}: {e}")

    def _restore_from_backup(self, file_path: Path) -> bool:
        """Restore data from the most recent backup."""
        backups = sorted(self.backup_dir.glob(f"{file_path.stem}_*.json"))
        if not backups:
            return False

        latest_backup = backups[-1]
        try:
            shutil.copy2(latest_backup, file_path)
            print(f"Restored from backup: {latest_backup}", file=sys.stderr)
            return True
        except Exception as e:
            print(f"Failed to restore from backup: {e}", file=sys.stderr)
            return False

    def _get_default_preferences(self) -> Dict[str, Any]:
        """Get default preferences structure."""
        return {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "user_id": self._generate_user_id(),
            "preferences": {
                "development": {"preferred_languages": [], "frameworks": [], "tools": []},
                "workflow": {"auto_save": True, "quality_threshold": 70},
                "ui": {"theme": "auto", "verbosity": "medium"},
                "privacy": {"local_storage_only": True}
            },
            "learned_patterns": {},
            "history": {"commands_used": [], "tasks_completed": []}
        }

    # Public API methods

    def update_system_profile(self, force: bool = False) -> Dict[str, Any]:
        """
        Update system environment profile.

        Args:
            force: Force update even if recent profile exists

        Returns:
            Updated profile data
        """
        env_data = self._read_environment()
        current_profile = self.profiler.get_system_fingerprint()

        # Check if update is needed
        if not force and env_data.get("profiles"):
            last_profile = env_data["profiles"][-1]
            time_diff = time.time() - last_profile.get("timestamp", 0)
            if time_diff < 3600:  # Only update if last profile is older than 1 hour
                return last_profile

        # Add new profile
        env_data["profiles"].append(current_profile)
        env_data["last_profile"] = current_profile
        env_data["profile_count"] = len(env_data["profiles"])
        env_data["last_updated"] = datetime.now().isoformat()

        # Keep only last 100 profiles
        if len(env_data["profiles"]) > 100:
            env_data["profiles"] = env_data["profiles"][-100:]

        self._write_environment(env_data)
        return current_profile

    def set_preference(self, category: str, key: str, value: Any):
        """
        Set a user preference.

        Args:
            category: Preference category (e.g., 'development', 'workflow', 'ui')
            key: Preference key
            value: Preference value
        """
        preferences = self._read_preferences()

        if category not in preferences["preferences"]:
            preferences["preferences"][category] = {}

        preferences["preferences"][category][key] = value
        self._write_preferences(preferences)

    def get_preference(self, category: str, key: str, default: Any = None) -> Any:
        """
        Get a user preference.

        Args:
            category: Preference category
            key: Preference key
            default: Default value if preference doesn't exist

        Returns:
            Preference value or default
        """
        preferences = self._read_preferences()
        return preferences["preferences"].get(category, {}).get(key, default)

    def get_all_preferences(self) -> Dict[str, Any]:
        """Get all user preferences."""
        preferences = self._read_preferences()
        return preferences.get("preferences", {})

    def record_command_usage(self, command: str, context: Dict[str, Any] = None):
        """
        Record command usage for learning patterns.

        Args:
            command: Command that was used
            context: Additional context about command usage
        """
        preferences = self._read_preferences()

        usage_record = {
            "command": command,
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }

        preferences["history"]["commands_used"].append(usage_record)

        # Keep only last 1000 commands
        if len(preferences["history"]["commands_used"]) > 1000:
            preferences["history"]["commands_used"] = preferences["history"]["commands_used"][-1000:]

        # Update command preferences
        if command not in preferences["learned_patterns"]["command_preferences"]:
            preferences["learned_patterns"]["command_preferences"][command] = {
                "usage_count": 0,
                "last_used": None,
                "success_rate": 0.0,
                "contexts": []
            }

        cmd_pref = preferences["learned_patterns"]["command_preferences"][command]
        cmd_pref["usage_count"] += 1
        cmd_pref["last_used"] = usage_record["timestamp"]
        if context:
            cmd_pref["contexts"].append(context)
            # Keep only last 10 contexts per command
            if len(cmd_pref["contexts"]) > 10:
                cmd_pref["contexts"] = cmd_pref["contexts"][-10:]

        self._write_preferences(preferences)

    def record_task_completion(self, task_type: str, success: bool,
                             quality_score: float, context: Dict[str, Any] = None):
        """
        Record task completion for learning patterns.

        Args:
            task_type: Type of task completed
            success: Whether task was successful
            quality_score: Quality score achieved (0-100)
            context: Additional context about the task
        """
        preferences = self._read_preferences()

        task_record = {
            "task_type": task_type,
            "success": success,
            "quality_score": quality_score,
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }

        preferences["history"]["tasks_completed"].append(task_record)

        # Keep only last 500 tasks
        if len(preferences["history"]["tasks_completed"]) > 500:
            preferences["history"]["tasks_completed"] = preferences["history"]["tasks_completed"][-500:]

        self._write_preferences(preferences)

    def record_suggestion_response(self, suggestion: str, accepted: bool,
                                 context: Dict[str, Any] = None):
        """
        Record user response to suggestions for learning.

        Args:
            suggestion: Suggestion that was made
            accepted: Whether user accepted the suggestion
            context: Additional context
        """
        preferences = self._read_preferences()
        suggestions_data = self._read_suggestions()

        response_record = {
            "suggestion": suggestion,
            "accepted": accepted,
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }

        if accepted:
            preferences["history"]["suggestions_accepted"].append(response_record)
        else:
            preferences["history"]["suggestions_rejected"].append(response_record)

        # Keep only last 200 of each type
        for history_type in ["suggestions_accepted", "suggestions_rejected"]:
            if len(preferences["history"][history_type]) > 200:
                preferences["history"][history_type] = preferences["history"][history_type][-200:]

        # Update suggestion effectiveness
        suggestion_key = hash(suggestion) % 10000  # Simple hash for key
        if suggestion_key not in suggestions_data["response_rates"]:
            suggestions_data["response_rates"][suggestion_key] = {
                "suggestion": suggestion,
                "total_shown": 0,
                "accepted": 0,
                "rejected": 0,
                "acceptance_rate": 0.0
            }

        sugg_stats = suggestions_data["response_rates"][suggestion_key]
        sugg_stats["total_shown"] += 1
        if accepted:
            sugg_stats["accepted"] += 1
        else:
            sugg_stats["rejected"] += 1
        sugg_stats["acceptance_rate"] = sugg_stats["accepted"] / sugg_stats["total_shown"]

        self._write_preferences(preferences)
        self._write_suggestions(suggestions_data)

    def get_user_profile(self) -> Dict[str, Any]:
        """
        Get comprehensive user profile.

        Returns:
            Dictionary containing user preferences and environment data
        """
        preferences = self._read_preferences()
        environment = self._read_environment()

        return {
            "user_id": preferences.get("user_id"),
            "preferences": preferences.get("preferences", {}),
            "learned_patterns": preferences.get("learned_patterns", {}),
            "system_environment": environment.get("last_profile", {}),
            "profile_created": preferences.get("created_at"),
            "last_updated": preferences.get("last_updated"),
            "usage_stats": {
                "commands_used": len(preferences.get("history", {}).get("commands_used", [])),
                "tasks_completed": len(preferences.get("history", {}).get("tasks_completed", [])),
                "suggestions_responded": len(preferences.get("history", {}).get("suggestions_accepted", [])) +
                                      len(preferences.get("history", {}).get("suggestions_rejected", []))
            }
        }

    def export_preferences(self, export_path: str, include_sensitive: bool = False) -> bool:
        """
        Export user preferences to file.

        Args:
            export_path: Path to export file
            include_sensitive: Whether to include potentially sensitive data

        Returns:
            True if export was successful
        """
        try:
            profile = self.get_user_profile()

            # Filter sensitive data if requested
            if not include_sensitive:
                profile = self._filter_sensitive_data(profile)

            export_file = Path(export_path)
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"Export failed: {e}", file=sys.stderr)
            return False

    def import_preferences(self, import_path: str, merge_strategy: str = "merge") -> bool:
        """
        Import user preferences from file.

        Args:
            import_path: Path to import file
            merge_strategy: How to merge with existing data ("overwrite", "merge", "skip")

        Returns:
            True if import was successful
        """
        try:
            import_file = Path(import_path)
            if not import_file.exists():
                raise FileNotFoundError(f"Import file not found: {import_path}")

            with open(import_file, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)

            if merge_strategy == "overwrite":
                # Overwrite all preferences
                current_prefs = self._read_preferences()
                current_prefs["preferences"] = imported_data.get("preferences", {})
                current_prefs["learned_patterns"] = imported_data.get("learned_patterns", {})
                self._write_preferences(current_prefs)
            elif merge_strategy == "merge":
                # Merge preferences
                current_prefs = self._read_preferences()
                self._deep_merge(current_prefs["preferences"], imported_data.get("preferences", {}))
                self._deep_merge(current_prefs["learned_patterns"], imported_data.get("learned_patterns", {}))
                self._write_preferences(current_prefs)
            elif merge_strategy == "skip":
                # Only import if no existing preferences
                current_prefs = self._read_preferences()
                if not current_prefs.get("preferences"):
                    current_prefs["preferences"] = imported_data.get("preferences", {})
                    current_prefs["learned_patterns"] = imported_data.get("learned_patterns", {})
                    self._write_preferences(current_prefs)

            return True

        except Exception as e:
            print(f"Import failed: {e}", file=sys.stderr)
            return False

    def _filter_sensitive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Filter out potentially sensitive data."""
        filtered = data.copy()

        # Remove system environment details
        if "system_environment" in filtered:
            filtered["system_environment"] = {
                "platform": filtered["system_environment"].get("system", {}).get("platform"),
                "architecture": filtered["system_environment"].get("system", {}).get("architecture"),
                "capabilities": filtered["system_environment"].get("capabilities", {})
            }

        # Remove specific sensitive keys
        sensitive_keys = ["hostname", "processor", "env_variables", "git_config"]
        for key in sensitive_keys:
            if key in filtered.get("system_environment", {}):
                del filtered["system_environment"][key]

        return filtered

    def _deep_merge(self, base: Dict[str, Any], update: Dict[str, Any]):
        """Deep merge two dictionaries."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value


def main():
    """Command-line interface for user preference memory."""
    import argparse

    parser = argparse.ArgumentParser(description='User Preference Memory System')
    parser.add_argument('--dir', default='.claude-preferences', help='Storage directory path')

    subparsers = parser.add_subparsers(dest='action', help='Action to perform')

    # Profile commands
    subparsers.add_parser('profile', help='Show system profile')
    subparsers.add_parser('update-profile', help='Update system profile')

    # Preference commands
    pref_parser = subparsers.add_parser('set', help='Set preference')
    pref_parser.add_argument('--category', required=True, help='Preference category')
    pref_parser.add_argument('--key', required=True, help='Preference key')
    pref_parser.add_argument('--value', required=True, help='Preference value')

    get_parser = subparsers.add_parser('get', help='Get preference')
    get_parser.add_argument('--category', required=True, help='Preference category')
    get_parser.add_argument('--key', required=True, help='Preference key')

    subparsers.add_parser('show', help='Show all preferences')

    # Export/Import commands
    export_parser = subparsers.add_parser('export', help='Export preferences')
    export_parser.add_argument('--path', required=True, help='Export file path')
    export_parser.add_argument('--include-sensitive', action='store_true', help='Include sensitive data')

    import_parser = subparsers.add_parser('import', help='Import preferences')
    import_parser.add_argument('--path', required=True, help='Import file path')
    import_parser.add_argument('--strategy', default='merge',
                              choices=['overwrite', 'merge', 'skip'], help='Merge strategy')

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    memory = UserPreferenceMemory(args.dir)

    try:
        if args.action == 'profile':
            profile = memory.profiler.get_system_fingerprint()
            print(json.dumps(profile, indent=2))

        elif args.action == 'update-profile':
            profile = memory.update_system_profile(force=True)
            print(f"✅ Profile updated at {profile.get('timestamp')}")

        elif args.action == 'set':
            # Try to parse as JSON, fallback to string
            try:
                value = json.loads(args.value)
            except json.JSONDecodeError:
                value = args.value
            memory.set_preference(args.category, args.key, value)
            print(f"✅ Set {args.category}.{args.key} = {value}")

        elif args.action == 'get':
            value = memory.get_preference(args.category, args.key)
            print(json.dumps(value, indent=2))

        elif args.action == 'show':
            profile = memory.get_user_profile()
            print(json.dumps(profile, indent=2))

        elif args.action == 'export':
            success = memory.export_preferences(args.path, args.include_sensitive)
            print(f"✅ Export {'successful' if success else 'failed'}")

        elif args.action == 'import':
            success = memory.import_preferences(args.path, args.strategy)
            print(f"✅ Import {'successful' if success else 'failed'}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()