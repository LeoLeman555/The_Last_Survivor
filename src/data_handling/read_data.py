import ast
import json
import yaml


class ReadData:
    def read_json(self, filepath: str) -> dict:
        """Read a .json file and return its content as a dictionary."""
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                content = json.load(file)  # Parse JSON content into a dictionary
            return content
        except FileNotFoundError:
            print(f"Error: File not found at '{filepath}'.")
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON content in file '{filepath}'.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return {}

    def read_yaml(self, filepath: str) -> dict:
        """Read a .yaml file and return its content as a dictionary."""
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                content = yaml.safe_load(file)  # Safely load the YAML content
            return content
        except FileNotFoundError:
            print(f"Error: File not found at '{filepath}'.")
        except json.JSONDecodeError:
            print(f"Error: Failed to decode YAML content in file '{filepath}'.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return {}
