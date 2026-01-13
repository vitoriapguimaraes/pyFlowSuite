"""
Configuration Manager for PyFlow Suite Apps
Handles loading, saving, and validating app configurations.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages app configurations stored as JSON files"""

    def __init__(self, config_dir: Path):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def get_config_path(self, app_name: str) -> Path:
        """Get path to app config file"""
        return self.config_dir / f"{app_name}.json"

    def load_config(self, app_name: str) -> Dict[str, Any]:
        """Load configuration for an app"""
        config_path = self.get_config_path(app_name)

        if not config_path.exists():
            return {}

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def save_config(self, app_name: str, config: Dict[str, Any]) -> bool:
        """Save configuration for an app"""
        config_path = self.get_config_path(app_name)

        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False

    def is_configured(self, app_name: str, required_keys: list) -> bool:
        """Check if app has all required configuration keys"""
        config = self.load_config(app_name)

        if not config:
            return False

        return all(key in config and config[key] for key in required_keys)

    def validate_path(self, path: str, must_exist: bool = False) -> bool:
        """Validate a file/folder path"""
        if not path:
            return False

        p = Path(path)

        if must_exist:
            return p.exists()

        # Check if parent directory exists for new files
        return p.parent.exists()
