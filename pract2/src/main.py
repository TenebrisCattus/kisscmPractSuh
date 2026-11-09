"""Main module for CLI dependency visualizer application."""

import sys
from config import load_config, validate_config


def print_parameters(config: dict) -> None:
    """Print configuration parameters in key-value format."""
    print("Configuration parameters:")
    for key, value in config.items():
        print(f"  {key}: {value}")


def main() -> None:
    """Entry point of the application."""
    config_path = "config.yaml"
    if len(sys.argv) > 1:
        config_path = sys.argv[1]

    try:
        config = load_config(config_path)
        validate_config(config)
        print_parameters(config)
    except ValueError as err:
        print(f"Validation error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()