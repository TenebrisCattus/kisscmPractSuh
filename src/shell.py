"""Shell REPL logic and command handling with VFS, core, and extra commands."""

import time
from src.vfs import VirtualFileSystem

DEFAULT_TAIL_LINES = 10
UPTIME_FORMAT_SECONDS = 60


class Shell:
    """Represents the shell emulator with full command set and chown."""

    def __init__(self, vfs_path: str | None) -> None:
        """Initialize shell with VFS, history, uptime, and ownerships."""
        self.vfs_path = vfs_path
        self.vfs_error = None
        try:
            self.vfs = VirtualFileSystem(vfs_path)
        except Exception as exc:
            self.vfs_error = str(exc)
            self.vfs = VirtualFileSystem(None)

        self.cwd: list[str] = []
        self.history_list: list[str] = []
        self.start_time = time.time()
        self.owners: dict[str, str] = {}

    def parse_input(self, user_input: str) -> tuple[str, list[str]]:
        """Parse user input into command and arguments."""
        parts = user_input.strip().split()
        if not parts:
            return "", []
        return parts[0], parts[1:]

    def _get_current_dir_node(self) -> dict | str:
        """Navigate VFS to current working directory."""
        node = self.vfs.root
        for part in self.cwd:
            if isinstance(node, dict) and part in node:
                node = node[part]
            else:
                return {}
        return node

    def cmd_ls(self, args: list[str]) -> str:
        """List directory contents."""
        target_node = self._get_current_dir_node()
        if args:
            target_node = self._resolve_path(args[0])

        if not isinstance(target_node, dict):
            target_name = args[0] if args else "."
            return f"ls: {target_name}: Not a directory"

        return "  ".join(target_node.keys())

    def cmd_cd(self, args: list[str]) -> str:
        """Change current working directory."""
        if not args:
            self.cwd = []
            return ""

        path_arg = args[0]
        if path_arg == "/":
            self.cwd = []
            return ""

        parts = path_arg.split("/")
        new_cwd = list(self.cwd)
        for part in parts:
            if not part or part == ".":
                continue
            if part == "..":
                if new_cwd:
                    new_cwd.pop()
            else:
                node = self._navigate_from(new_cwd, part)
                if isinstance(node, dict):
                    new_cwd.append(part)
                else:
                    return f"cd: {path_arg}: No such file or directory"
        self.cwd = new_cwd
        return ""

    def _navigate_from(self, base_cwd: list[str], target: str) -> dict | str:
        """Navigate from specific cwd to target child."""
        node = self.vfs.root
        for part in base_cwd:
            if isinstance(node, dict) and part in node:
                node = node[part]
            else:
                return {}
        if isinstance(node, dict) and target in node:
            return node[target]
        return {}

    def _resolve_path(self, path_str: str) -> dict | str:
        """Resolve path string to VFS node."""
        if path_str.startswith("/"):
            parts = [p for p in path_str.split("/") if p]
            node = self.vfs.root
            for p in parts:
                if isinstance(node, dict) and p in node:
                    node = node[p]
                else:
                    return None
            return node
        else:
            target_node = self._get_current_dir_node()
            parts = [p for p in path_str.split("/") if p]
            for p in parts:
                if isinstance(target_node, dict) and p in target_node:
                    target_node = target_node[p]
                else:
                    return None
            return target_node

    def cmd_history(self) -> str:
        """Return command history."""
        return "\n".join(
            f"{idx + 1}  {cmd}"
            for idx, cmd in enumerate(self.history_list)
        )

    def cmd_uptime(self) -> str:
        """Return system uptime."""
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // UPTIME_FORMAT_SECONDS
        seconds = elapsed % UPTIME_FORMAT_SECONDS
        return f"Uptime: {minutes}m {seconds}s"

    def cmd_tail(self, args: list[str]) -> str:
        """Return last lines of a file."""
        if not args:
            return "tail: missing file operand"

        node = self._resolve_path(args[0])
        if node is None:
            return f"tail: {args[0]}: No such file or directory"
        if isinstance(node, dict):
            return f"tail: {args[0]}: Is a directory"

        lines = node.splitlines()
        last_lines = lines[-DEFAULT_TAIL_LINES:]
        return "\n".join(last_lines)

    def cmd_chown(self, args: list[str]) -> str:
        """Change file or directory owner in memory."""
        if len(args) < 2:
            return "chown: missing operand"

        new_owner = args[0]
        target_path = args[1]
        node = self._resolve_path(target_path)

        if node is None:
            return f"chown: {target_path}: No such file or directory"

        self.owners[target_path] = new_owner
        return f"Owner of '{target_path}' changed to '{new_owner}'"

    def execute_command(self, user_input: str) -> str:
        """Execute command and return output string."""
        if self.vfs_error:
            err_msg = f"Error loading VFS: {self.vfs_error}"
            self.vfs_error = None
            return err_msg

        cmd, args = self.parse_input(user_input)
        if not cmd:
            return ""

        if cmd != "history":
            self.history_list.append(user_input)

        if cmd == "exit":
            return "EXIT"
        if cmd == "ls":
            return self.cmd_ls(args)
        if cmd == "cd":
            return self.cmd_cd(args)
        if cmd == "history":
            res = self.cmd_history()
            self.history_list.append(user_input)
            return res
        if cmd == "uptime":
            return self.cmd_uptime()
        if cmd == "tail":
            return self.cmd_tail(args)
        if cmd == "chown":
            return self.cmd_chown(args)

        return f"Error: unknown command '{cmd}'"