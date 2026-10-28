"""Application entry point with configuration and startup script support."""

import argparse
import tkinter as tk
from src.shell import Shell
from src.gui import ShellGUI

DEFAULT_VFS_NAME = "default_vfs"
STARTUP_DELAY_MS = 100


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments for VFS and startup script."""
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument(
        "--vfs",
        type=str,
        default=DEFAULT_VFS_NAME,
        help="Path to physical VFS location",
    )
    parser.add_argument(
        "--script",
        type=str,
        default="",
        help="Path to startup script",
    )
    return parser.parse_args()


def run_startup_script(shell: Shell, gui: ShellGUI, script_path: str) -> None:
    """Execute startup script commands line by line."""
    try:
        with open(script_path, "r", encoding="utf-8") as file:
            for line in file:
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                gui.print_output(f"$ {stripped}")
                result = shell.execute_command(stripped)
                if result == "EXIT":
                    break
                if result:
                    gui.print_output(result)
    except Exception as exc:
        gui.print_output(f"Error executing startup script: {exc}")


def main() -> None:
    """Run the shell emulator application."""
    args = parse_arguments()

    print(f"[DEBUG] VFS path/name: {args.vfs}")
    print(f"[DEBUG] Startup script: {args.script if args.script else 'None'}")

    root = tk.Tk()
    shell = Shell(args.vfs)
    gui = ShellGUI(root, shell)

    if args.script:
        root.after(
            STARTUP_DELAY_MS,
            lambda: run_startup_script(shell, gui, args.script),
        )

    root.mainloop()


if __name__ == "__main__":
    main()