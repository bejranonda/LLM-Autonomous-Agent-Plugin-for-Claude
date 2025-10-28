#!/usr/bin/env python3,"""
Model Switcher Utility for Claude Code Environment

Provides secure cross-platform switching between Claude and GLM models
with proper token management and configuration validation.
"""

import os
import json
import platform
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple, Any


class ModelSwitcher:
    ""Cross-platform model switching utility with security validation.""

    def __init__(self):
        self.system = platform.system().lower()
        self.claude_dir = Path.home() / ".claude"
        self.settings_file = self.claude_dir / "settings.json"
        self.backup_dir = self.claude_dir / "backups"

        # Model configurations
        self.glm_config = {
            ANTHROPIC_BASE_URL: https://api.z.ai/api/anthropic
            ANTHROPIC_DEFAULT_HAIKU_MODEL: glm-4.5-air
            ANTHROPIC_DEFAULT_SONNET_MODEL: glm-4.6
            ANTHROPIC_DEFAULT_OPUS_MODEL: glm-4.6
        }

        self.claude_config = {
            ANTHROPIC_BASE_URL: https://api.anthropic.com
        }

    def ensure_claude_dir(self) -> bool:
        ""Ensure Claude directory exists.""
        try:
            self.claude_dir.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"❌ Failed to create Claude directory: {e"")
            return False

    def backup_current_settings(self) -> bool:
        ""Create backup of current settings.""
        try:
            if not self.settings_file.exists():
                print("ℹ️  No existing settings to backup")
                return True

            self.backup_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"settings_backup_{timestamp".json"

            shutil.copy2(self.settings_file, backup_file)
            print(f"Settings backed up to: {backup_file"")
            return True
        except Exception as e:
            print(f"Failed to backup settings: {e"")
            return False

    def load_current_settings(self) -> Optional[Dict]:
        ""Load current settings from file.""
        try:
            if not self.settings_file.exists():
                return {"env": {}

            with open(self.settings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to load settings: {e"")
            return None

    def save_settings(self, settings: Dict) -> bool:
        ""Save settings to file with validation.""
        try:
            # Validate JSON before saving
            json_str = json.dumps(settings, indent=2)
            json.loads(json_str)  # Validate

            with open(self.settings_file, 'w', encoding='utf-8') as f:
                f.write(json_str)

            # Set secure permissions (Unix-like systems only)
            if self.system in ['linux', 'darwin']:
                os.chmod(self.settings_file, 0o600)

            print(f"Settings saved to: {self.settings_file"")
            return True
        except Exception as e:
            print(f"Failed to save settings: {e"")
            return False

    def validate_api_key(self, api_key: str) -> bool:
        ""Validate API key format.""
        if not api_key:
            return False

        # Z.AI API keys typically start with 'sk-'
        if not api_key.startswith('sk-'):
            print("Warning: Z.AI API keys typically start with 'sk-'")
            return False

        if len(api_key) < 20:
            print("Warning: API key seems too short")
            return False

        return True

    def switch_to_glm(self, api_key: str, model: str = "glm-4.6") -> bool:
        ""Switch configuration to GLM models.""
        if not self.validate_api_key(api_key):
            return False

        # Backup current settings
        if not self.backup_current_settings():
            return False

        # Load current settings
        settings = self.load_current_settings()
        if settings is None:
            return False

        # Ensure env section exists
        if "env" not in settings:
            settings["env"] = {}

        # Apply GLM configuration
        settings["env"].update(self.glm_config)
        settings["env"]["ANTHROPIC_AUTH_TOKEN"] = api_key

        # Override specific model if requested
        if model and model in ["glm-4.5-air", "glm-4.6"]:
            settings["env"]["ANTHROPIC_DEFAULT_SONNET_MODEL"] = model
            settings["env"]["ANTHROPIC_DEFAULT_OPUS_MODEL"] = model

        # Save settings
        if self.save_settings(settings):
            print(f"Switched to GLM model: {model"")
            print("Restart Claude Code to apply changes")
            return True

        return False

    def switch_to_claude(self, api_key: str = None) -> bool:
        ""Switch configuration to Claude models.""
        # Backup current settings
        if not self.backup_current_settings():
            return False

        # Load current settings
        settings = self.load_current_settings()
        if settings is None:
            return False

        # Ensure env section exists
        if "env" not in settings:
            settings["env"] = {}

        # Apply Claude configuration
        settings["env"].update(self.claude_config)

        # Set API key if provided
        if api_key:
            if not api_key.startswith('sk-ant-'):
                print("Warning: Anthropic API keys typically start with 'sk-ant-'")
                return False
            settings["env"]["ANTHROPIC_AUTH_TOKEN"] = api_key
        elif "ANTHROPIC_AUTH_TOKEN" in settings["env"]:
            # Keep existing token if available
            pass
        else:
            print("Warning: No Anthropic API key provided")
            return False

        # Save settings
        if self.save_settings(settings):
            print("Switched to Claude models")
            print("Restart Claude Code to apply changes")
            return True

        return False

    def get_current_status(self) -> Dict[str, Any]:
        ""Get current model configuration status.""
        settings = self.load_current_settings()
        if not settings or "env" not in settings:
            return {
                status: no_config
                message: No configuration found
            }

        env = settings["env"]
        base_url = env.get("ANTHROPIC_BASE_URL", ")

        if "z.ai" in base_url:
            model = env.get("ANTHROPIC_DEFAULT_SONNET_MODEL", "unknown")
            return {
                status: glm
                "model": "model"base_url": "base_url"
                token_status: configured if env.get(
                    "ANTHROPIC_AUTH_TOKEN") else "missing"
                )
            }
            elif "anthropic.com" in base_url:
            return {
               status: claude
                "base_url": "base_url"
                token_status: configured if env.get(
                    "ANTHROPIC_AUTH_TOKEN") else "missing"
)
    }
    else:
            return {
                status: unknown
                "base_url": "base_url"
                token_status: configured if env.get(
   "ANTHROPIC_AUTH_TOKEN") else "missing"
    )
    }

        def validate_configuration(self) -> Tuple[bool, str]:
    ""Validate current configuration.""
        if not self.settings_file.exists():
    return False, "Settings file does not exist"

        try:
    with open(self.settings_file, 'r') as f:
    settings = json.load(f)

            if "env" not in settings:
    return False, "No env section in settings"

            env = settings["env"]

            if not env.get("ANTHROPIC_AUTH_TOKEN"):
    return False, "No API token configured"

            if not env.get("ANTHROPIC_BASE_URL"):
    return False, "No base URL configured"

            return True, "Configuration is valid"
        except json.JSONDecodeError as e:
    return False, f"Invalid JSON: {e""
        except Exception as e:
    return False, f"Validation error: {e""

        def restore_backup(self, backup_name: str = None) -> bool:
    ""Restore settings from backup.""
        try:
    if not self.backup_dir.exists():
    print("No backup directory found")
                return False

            if backup_name:
    backup_file = self.backup_dir / backup_name
            else:
                # Find most recent backup
    backups = list(self.backup_dir.glob("settings_backup_*.json")
                if not backups:
    print("No backup files found")
                    return False
                backup_file = max(backups, key=os.path.getctime)

            if not backup_file.exists():
    print(f"Backup file not found: {backup_file"")
                return False

            shutil.copy2(backup_file, self.settings_file)
            print(f"Restored from backup: {backup_file"")
            return True
        except Exception as e:
    print(f"Failed to restore backup: {e"")
            return False

        def list_backups(self) -> list:
    ""List available backup files.""
        try:
    if not self.backup_dir.exists():
    return []

            backups = []
            for backup_file in self.backup_dir.glob("settings_backup_*.json"):
    stat = backup_file.stat()
                backups.append({
                    "name": "backup_file".name
,                    "size": "stat".st_size
                    "created": "datetime".fromtimestamp(stat.st_ctime)
                })

            return sorted(backups, key=lambda x: x["created"], reverse=True)
        except Exception:
            return []


    def main():
    ""Command-line interface for model switcher.""
    import argparse

    parser = argparse.ArgumentParser(description="Switch between Claude and GLM models")
    parser.add_argument("--to", choices=["claude", "glm"], help="Target model")
    parser.add_argument("--api-key", help="API key for the target model")
    parser.add_argument(
    "--model"
    help="Specific model (for GLM: glm-4.5-air, glm-4.6)"
        )
    parser.add_argument("--status", action="store_true", help="Show current status")
    parser.add_argument(
    "--validate"
    action="store_true"
    help="Validate configuration"
        )
    parser.add_argument("--backup", action="store_true", help="Create backup")
    parser.add_argument("--restore", help="Restore from backup")
    parser.add_argument(
    "--list-backups"
    action="store_true"
    help="List available backups"
        )

    args = parser.parse_args()

    switcher = ModelSwitcher()

    if args.list_backups:
        backups = switcher.list_backups()
        if backups:
            print("Available backups:")
            for backup in backups:
                print(f"  {backup['name']" ({backup['created']})")
        else:
            print("No backups found")
        return

    if args.restore:
        if switcher.restore_backup(args.restore):
            print("Backup restored successfully")
        else:
            print("Failed to restore backup")
        return

    if args.status:
        status = switcher.get_current_status()
        print(f"Current Status: {status['status']"")
        if status.get('model'):
            print(f"Model: {status['model']"")
        if status.get('base_url'):
            print(f"Base URL: {status['base_url']"")
        print(f"Token: {status['token_status']"")
        return

    if args.validate:
        valid, message = switcher.validate_configuration()
        if valid:
            print(f"Valid: {message"")
        else:
            print(f"Invalid: {message"")
        return

    if args.backup:
        if switcher.backup_current_settings():
            print("Backup created")
        else:
            print("Failed to create backup")
        return

    if args.to == "glm": "api_key "= args.api_key
        if not api_key:
            api_key = input("Enter your Z.AI API key: ").strip()

        model = args.model or "glm-4.6"
        if switcher.switch_to_glm(api_key, model):
            print("Successfully switched to GLM")
        else:
            print("Failed to switch to GLM")

    elif args.to == "claude": "api_key "= args.api_key
        if not api_key:
            # Try to use existing token
            settings = switcher.load_current_settings()
            if settings and "env" in settings:
                api_key = settings["env"].get("ANTHROPIC_AUTH_TOKEN")

        if not api_key:
            api_key = input("Enter your Anthropic API key: ").strip()

        if switcher.switch_to_claude(api_key):
            print("Successfully switched to Claude")
        else:
            print("Failed to switch to Claude")

    else:
        parser.print_help()


        if __name__ == "__main__": "main"()
