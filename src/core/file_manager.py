import json
import os

from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True


class FileManager:
    """Class to manage file operations. All the operations are ran from the root path of the project."""

    @staticmethod
    def get_root_path():
        """Get the root path of the project."""
        return os.path.join(os.path.dirname(__file__), "..", "..")

    @staticmethod
    def create_directory(directory_path):
        """Create a directory."""
        full_path = os.path.join(FileManager.get_root_path(), directory_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)

    @staticmethod
    def path_exists(file_path):
        """Check if a file exists."""
        full_path = os.path.join(FileManager.get_root_path(), file_path)
        return os.path.exists(full_path)

    @staticmethod
    def read_lines(file_path):
        """Read a text file."""
        full_path = os.path.join(FileManager.get_root_path(), file_path)

        if not os.path.exists(full_path):
            return None

        with open(full_path, 'r') as file:
            return [line.strip() for line in file.readlines()]

    @staticmethod
    def load_yaml_file(file_path):
        """Load a yaml file."""
        full_path = os.path.join(FileManager.get_root_path(), file_path)

        if not os.path.exists(full_path):
            return None

        with open(full_path, 'r') as file:
            return yaml.load(file)

    @staticmethod
    def save_yaml_file(file_path, data):
        """Save a yaml file."""
        full_path = os.path.join(FileManager.get_root_path(), file_path)
        with open(full_path, 'w') as file:
            yaml.dump(data, file)

    @staticmethod
    def load_json_file(file_path):
        """Load a json file."""
        full_path = os.path.join(FileManager.get_root_path(), file_path)

        if not os.path.exists(full_path):
            return None

        with open(full_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def save_json_file(file_path, data):
        """Save a json file."""
        full_path = os.path.join(FileManager.get_root_path(), file_path)
        with open(full_path, 'w') as file:
            json.dump(data, file, indent=2)
