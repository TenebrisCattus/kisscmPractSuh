"""Main module for CLI dependency visualizer application."""

import sys
from config import load_config, validate_config
from dependency import fetch_package_data, get_direct_dependencies


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

        print("\nFetching package dependencies...")
        pkg_data = fetch_package_data(
            config["repo_path"],
            config["package_name"],
            config["package_version"]
        )
        dependencies = get_direct_dependencies(pkg_data)

        print(f"Direct dependencies for {config['package_name']} "
              f"(@{config['package_version']}):")
        if not dependencies:
            print("  No direct dependencies found.")
        else:
            for dep_name, dep_version in dependencies.items():
                print(f"  - {dep_name}: {dep_version}")

    except ValueError as err:
        print(f"Validation error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()