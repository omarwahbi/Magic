"""Loading dialog widget."""

import tkinter as tk
from tkinter import ttk


class LoadingDialog:
    """Modern modal loading dialog with progress bar."""

    def __init__(self, parent: tk.Tk, title: str = "Loading...", message: str = "Please wait..."):
        """
        Initialize loading dialog.

        Args:
            parent: Parent window
            title: Dialog title
            message: Message to display
        """
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)

        # Remove window decorations for modern look
        self.dialog.overrideredirect(False)

        # Set size
        width, height = 400, 150
        self.dialog.geometry(f"{width}x{height}")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center on parent
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")

        # Main frame with padding
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title label
        title_label = ttk.Label(
            main_frame,
            text=title,
            font=("Segoe UI", 14, "bold"),
        )
        title_label.pack(pady=(0, 10))

        # Message label
        self.message_label = ttk.Label(
            main_frame,
            text=message,
            wraplength=350
        )
        self.message_label.pack(pady=(0, 15))

        # Progress bar
        self.progressbar = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=350,
        )
        self.progressbar.pack()
        self.progressbar.start(10)

        # Force the window to display
        self.dialog.update_idletasks()
        self.dialog.update()

    def update_message(self, message: str) -> None:
        """
        Update the loading message.

        Args:
            message: New message to display
        """
        try:
            if hasattr(self, 'message_label') and self.dialog.winfo_exists():
                self.message_label.config(text=message)
                self.dialog.update_idletasks()
                self.dialog.update()
        except tk.TclError:
            # Dialog was already closed, ignore the error
            pass

    def close(self) -> None:
        """Close the loading dialog."""
        try:
            if hasattr(self, 'progressbar'):
                self.progressbar.stop()
            if hasattr(self, 'dialog') and self.dialog.winfo_exists():
                self.dialog.destroy()
        except tk.TclError:
            # Dialog was already closed, ignore the error
            pass
