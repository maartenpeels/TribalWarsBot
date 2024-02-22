import logging

from src.core.file_manager import FileManager
from src.core.input import Input

logger = logging.getLogger("Config")


class Config:
    """Class for handling the config file."""
    config_file = "config.yaml"
    config_file_example = "config.example.yaml"

    def __init__(self):
        """Load the config file or create a new one if it doesn't exist."""
        if FileManager.path_exists(self.config_file):
            logger.info("Loading config file")
            self.config = self.load_config()
        else:
            logger.info("Config file not found, creating a new one")
            self.config = self.create_config()

    def load_config(self):
        """Load the config file and update it if it's outdated."""
        old_config = FileManager.load_yaml_file(self.config_file)
        new_config = FileManager.load_yaml_file(self.config_file_example)

        # Check if the config file is outdated
        if old_config["version"] < new_config["version"]:
            logger.warning("Config file is outdated, updating it")
            old_config = self.update_config(old_config, new_config)

        return old_config

    def update_config(self, old_config, new_config):
        """Update the config file with new values."""
        for key, value in new_config.items():
            if key not in old_config:
                old_config[key] = value
            elif isinstance(value, dict):
                old_config[key] = self.update_config(old_config[key], value)

        old_config["version"] = new_config["version"]
        FileManager.save_yaml_file(self.config_file, old_config)
        return old_config

    def create_config(self):
        """Create a new config file."""
        config = FileManager.load_yaml_file(self.config_file_example)

        config.update({
            "web": {
                "server": Input.ask_string("Enter the server", "nl95"),
                "domain": Input.ask_string("Enter the domain", "tribalwars.nl"),
                "user-agent": Input.ask_string("Enter the user agent",
                                               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                                               "like Gecko) Chrome/121.0.0.0 Safari/537.36")
            },
        })

        FileManager.save_yaml_file(self.config_file, config)
        return config

    def get_village(self, village_id, path, default=None):
        """Get a village from the config file."""
        villages = self.get("villages")
        value = None
        for village in villages:
            if village["id"] == village_id:
                value = village

        if value is None:
            raise KeyError(f"Village with id {village_id} not found in config")

        keys = path.split('.')
        for key in keys:
            if key not in value:
                if default is not None:
                    return default
                raise KeyError(f"Path {path} not found in village({village_id}) config (missing key {key})")
            value = value[key]

        return value

    def get(self, path, default=None):
        """Get a value from the config file. If the value doesn't exist, return the default value or a KeyError."""
        keys = path.split('.')
        value = self.config
        for key in keys:
            if key not in value:
                if default is not None:
                    return default
                raise KeyError(f"Path {path} not found in config (missing key {key})")
            value = value[key]
        return value

    def set(self, path, value):
        """Set a value in the config file. If the path doesn't exist, create it."""
        keys = path.split('.')
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value
        FileManager.save_yaml_file(self.config_file, self.config)
        return value
