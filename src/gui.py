"""Graphical user interface for the shell emulator using tkinter."""

import tkinter as tk
from tkinter import scrolledtext
from shell import Shell


class ShellGUI:
    """Main GUI application class for shell emulator."""

    def __init__(self, root: tk.Tk, shell: Shell) -> None:
        """Initialize GUI components and window state."""
        self.root = root
        self.shell = shell
        self.root.title(f"VFS: {self.shell.vfs_name}")
        self.root.geometry("600x400")

        self.text_area = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, state="disabled"
        )
        self.text_area.pack(expand=True, fill="both", padx=5, pady=5)

        self.entry = tk.Entry(root)
        self.entry.pack(fill="x", padx=5, pady=5)
        self.entry.bind("<Return>", self.handle_enter)
        self.entry.focus()

        welcome_text = f"Welcome to Shell Emulator ({self.shell.vfs_name})"
        self.print_output(welcome_text)
        self.print_output("Type commands (ls, cd, exit):")

    def print_output(self, text: str) -> None:
        """Append text to the console display area."""
        self.text_area.config(state="normal")
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.see(tk.END)
        self.text_area.config(state="disabled")

    def handle_enter(self, event: tk.Event) -> None:
        """Handle user pressing Enter key in input entry."""
        user_input = self.entry.get()
        self.entry.delete(0, tk.END)
        if not user_input.strip():
            return

        self.print_output(f"$ {user_input}")
        result = self.shell.execute_command(user_input)
        if result == "EXIT":
            self.root.quit()
            return
        if result:
            self.print_output(result)