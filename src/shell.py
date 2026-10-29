"""Shell REPL logic and command handling with VFS support."""

from src.vfs import VirtualFileSystem


class Shell:
    """Represents the shell emulator."""

    def __init__(self, vfs_path: str | None) -> None:
        """Initialize shell with VFS instance and error handling."""
        self.vfs_path = vfs_path
        self.vfs_error = None
        try:
            self.vfs = VirtualFileSystem(vfs_path)
        except Exception as exc:
            self.vfs_error = str(exc)
            self.vfs = VirtualFileSystem(None)

        self.cwd = [""]

    def parse_input(self, user_input: str) -> tuple[str, list[str]]:
        """Parse user input into command and arguments."""
        parts = user_input.strip().split()
        if not parts:
            return "", []
        return parts[0], parts[1:]

    def execute_command(self, user_input: str) -> str:
        """Execute command and return output string."""
        if self.vfs_error:
            err_msg = f"Error loading VFS: {self.vfs_error}"
            self.vfs_error = None
            return err_msg

        cmd, args = self.parse_input(user_input)
        if not cmd:
            return ""

        if cmd == "exit":
            return "EXIT"

        if cmd in ("ls", "cd"):
            args_str = ", ".join(args)
            return f"Stub command '{cmd}', args: [{args_str}]"

        return f"Error: unknown command '{cmd}'"