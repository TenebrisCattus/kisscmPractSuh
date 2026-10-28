"""Shell REPL logic and command handling."""


class Shell:
    """Represents the shell emulator."""

    def __init__(self, vfs_name: str) -> None:
        """Initialize shell with VFS name."""
        self.vfs_name = vfs_name

    def parse_input(self, user_input: str) -> tuple[str, list[str]]:
        """Parse user input into command and arguments."""
        parts = user_input.strip().split()
        if not parts:
            return "", []
        return parts[0], parts[1:]

    def execute_command(self, user_input: str) -> str:
        """Execute command and return output string."""
        cmd, args = self.parse_input(user_input)
        if not cmd:
            return ""

        if cmd == "exit":
            return "EXIT"

        if cmd in ("ls", "cd"):
            args_str = ", ".join(args)
            return f"Stub command '{cmd}', args: [{args_str}]"

        return f"Error: unknown command '{cmd}'"