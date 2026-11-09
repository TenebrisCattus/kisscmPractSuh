"""Main module for CLI dependency visualizer application."""

import sys
from config import load_config, validate_config
from graph import load_test_graph, build_graph
from visualization import generate_plantuml, generate_ascii_tree


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

        test_data = {}
        if config.get("test_mode", False):
            test_data = load_test_graph(config["repo_path"])

        print("\nBuilding dependency graph...")
        graph = build_graph(
            config["package_name"],
            config["package_version"],
            config,
            test_data
        )

        print(f"\nPlantUML Description for {config['package_name']}:")
        print(generate_plantuml(graph))

        if config.get("ascii_tree", False):
            print(f"\nASCII Tree for {config['package_name']}:")
            print(generate_ascii_tree(graph, config["package_name"]))

    except ValueError as err:
        print(f"Validation error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()