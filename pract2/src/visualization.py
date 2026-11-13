"""Module for generating PlantUML and ASCII tree visualizations."""


def generate_plantuml(graph: dict) -> str:
    """Generate PlantUML textual description from dependency graph."""
    lines = ["@startuml", "left to right direction"]
    for pkg, deps in graph.items():
        for dep in deps:
            lines.append(f'"{pkg}" --> "{dep}"')
    lines.append("@enduml")
    return "\n".join(lines)


def _build_ascii_branch(graph: dict, node: str, prefix: str,
                        path: set) -> list:
    """Helper to build ASCII tree lines recursively avoiding cycles."""
    lines = []
    deps = list(graph.get(node, {}).keys())
    for i, dep in enumerate(deps):
        is_last = (i == len(deps) - 1)
        connector = "└── " if is_last else "├── "
        if dep in path:
            lines.append(f"{prefix}{connector}{dep} (cycle)")
            continue
        lines.append(f"{prefix}{connector}{dep}")
        extension = "    " if is_last else "│   "
        sub_path = path.copy()
        sub_path.add(dep)
        sub_lines = _build_ascii_branch(
            graph, dep, prefix + extension, sub_path
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