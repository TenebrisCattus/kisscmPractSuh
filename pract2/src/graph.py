"""Module for building dependency graph via recursive DFS."""

import json
import sys
from dependency import fetch_package_data, get_direct_dependencies


def load_test_graph(file_path: str) -> dict:
    """Load test graph from a file with capital letters."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, dict):
            raise ValueError("Test graph root must be dict.")
        return data
    except FileNotFoundError:
        print(f"Error: Test file '{file_path}' not found.",
              file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Failed to parse test JSON.",
              file=sys.stderr)
        sys.exit(1)


def fetch_deps(name: str, ver: str, cfg: dict,
               test_data: dict) -> dict:
    """Get package dependencies based on mode."""
    if cfg.get("test_mode", False):
        return test_data.get(name, {})
    repo = cfg.get("repo_path", "")
    pkg_data = fetch_package_data(repo, name, ver)
    return get_direct_dependencies(pkg_data)


def build_graph(name: str, ver: str, cfg: dict,
                test_data: dict, graph: dict = None,
                visited: set = None,
                rec_stack: set = None) -> dict:
    """Build full graph via recursive DFS with cycles check."""
    if graph is None:
        graph = {}
    if visited is None:
        visited = set()
    if rec_stack is None:
        rec_stack = set()

    if name in rec_stack or name in visited:
        return graph

    visited.add(name)
    rec_stack.add(name)

    deps = fetch_deps(name, ver, cfg, test_data)
    graph[name] = deps

    for dep_n, dep_v in deps.items():
        if dep_n not in visited:
            build_graph(dep_n, dep_v, cfg, test_data,
                        graph, visited, rec_stack)

    rec_stack.remove(name)
    return graph