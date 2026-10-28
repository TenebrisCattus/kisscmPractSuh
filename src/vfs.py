"""Virtual File System (VFS) representation in memory."""

from pathlib import Path


class VirtualFileSystem:
    """Manages an in-memory representation of a directory tree."""

    def __init__(self, source_path: str | None = None) -> None:
        """Initialize VFS from disk path or create default."""
        self.root: dict = {}
        if source_path:
            self._load_from_disk(source_path)
        else:
            self._create_default_vfs()

    def _load_from_disk(self, path_str: str) -> None:
        """Load directory structure and text files into memory."""
        source = Path(path_str)
        if not source.exists() or not source.is_dir():
            raise FileNotFoundError(
                f"VFS directory not found or invalid: {path_str}"
            )
        self.root = self._build_tree(source)

    def _build_tree(self, current_path: Path) -> dict:
        """Recursively build dictionary representation of directory."""
        tree = {}
        for item in current_path.iterdir():
            if item.is_dir():
                tree[item.name] = self._build_tree(item)
            elif item.is_file():
                try:
                    tree[item.name] = item.read_text(
                        encoding="utf-8"
                    )
                except UnicodeDecodeError:
                    tree[item.name] = "[Binary file data]"
        return tree

    def _create_default_vfs(self) -> None:
        """Create a default in-memory VFS structure if path is omitted."""
        self.root = {
            "home": {
                "user": {
                    "welcome.txt": "Hello, VFS!",
                    "notes.txt": "Some notes here.",
                }
            },
            "etc": {
                "config.cfg": "setting=true",
            },
        }