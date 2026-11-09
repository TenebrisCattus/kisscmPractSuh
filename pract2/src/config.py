"""Module for loading and validating configuration for Stage 1."""

import sys
import yaml


def load_config(file_path: str) -> dict:
    """Load configuration parameters from a YAML file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        if not isinstance(config, dict):
            raise ValueError("Config root must be a dictionary.")
        return config
    except FileNotFoundError:
        print(f"Error: Config file '{file_path}' not found.",
              file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        sys.exit(1)


def validate_config(config: dict) -> None:
    """Validate all required configuration parameters."""
    required_keys = [
        "package_name",
        "repo_path",
        "test_mode",
        "package_version",
        "ascii_tree"
    ]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")

    if not isinstance(config["package_name"], str):
        raise ValueError("package_name must be a string.")
    if not isinstance(config["repo_path"], str):
        raise ValueError("repo_path must be a string.")
    if not isinstance(config["test_mode"], bool):
        raise ValueError("test_mode must be a boolean.")
    if not isinstance(config["package_version"], str):
        raise ValueError("package_version must be a string.")
    if not isinstance(config["ascii_tree"], bool):
        raise ValueError("ascii_tree must be a boolean.")