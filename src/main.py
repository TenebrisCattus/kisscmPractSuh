"""Application entry point."""

import tkinter as tk
from src.shell import Shell
from src.gui import ShellGUI

DEFAULT_VFS_NAME = "default_vfs"


def main() -> None:
    """Run the shell emulator application."""
    root = tk.Tk()
    shell = Shell(DEFAULT_VFS_NAME)
    ShellGUI(root, shell)
    root.mainloop()


if __name__ == "__main__":
    main()