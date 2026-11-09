"""Module for generating PlantUML and ASCII tree visualizations."""


def generate_plantuml(graph: dict) -> str:
    """Generate PlantUML textual description from dependency graph."""
    lines = ["@startuml", "left to right direction"]
    for pkg, deps in graph.items():
        if not deps:
            lines.append(f'"{pkg}"')
        for dep in deps:
            lines.append(f'"{pkg}" --> "{dep}"')
    lines.append("@enduml")
    return "\n".join(lines)


def _build_ascii_branch(graph: dict, node: str, prefix: str,
                        visited: set) -> list:
    """Helper to build ASCII tree lines recursively avoiding cycles."""
    lines = []
    if node in visited:
        return [f"{prefix}{node} (cycle)"]
    visited.add(node)
    deps = list(graph.get(node, {}).keys())
    for i, dep in enumerate(deps):
        is_last = (i == len(deps) - 1)
        connector = "└── " if is_last else "├── "
        lines.append(f"{prefix}{connector}{dep}")
        extension = "    " if is_last else "│   "
        sub_lines = _build_ascii_branch(
            graph, dep, prefix + extension, visited.copy()
        )
        lines.extend(sub_lines)
    return lines


def generate_ascii_tree(graph: dict, root: str) -> str:
    """Generate ASCII tree representation of dependencies."""
    if root not in graph:
        return root
    lines = [root]
    lines.extend(_build_ascii_branch(graph, root, "", {root}))
    return "\n".join(lines)