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
        width, height = 400, 180
        self.dialog.geometry(f"{width}x{height}")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center on parent
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")

        # Main frame with padding and background
        main_frame = tk.Frame(
            self.dialog,
            bg="#f0f0f0",
            relief=tk.FLAT,
            borderwidth=0
        )
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title label
        title_label = tk.Label(
            main_frame,
            text=title,
            font=("Segoe UI", 14, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=(10, 5))

        # Message label with better styling
        self.message_label = tk.Label(
            main_frame,
            text=message,
            font=("Segoe UI", 10),
            bg="#f0f0f0",
            fg="#666666",
            wraplength=350
        )
        self.message_label.pack(pady=(5, 20))

        # Progress bar with better styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor='#e0e0e0',
            bordercolor='#cccccc',
            background='#2196F3',  # Blue color for better visibility
            lightcolor='#2196F3',
            darkcolor='#1976D2',
            borderwidth=1,
            thickness=20,  # Thicker bar
            relief=tk.FLAT
        )

        # Progress bar container frame for better visibility
        progress_frame = tk.Frame(
            main_frame,
            bg="#f0f0f0"
        )
        progress_frame.pack(pady=(0, 10), fill=tk.X)

        self.progressbar = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=350,
            style="Custom.Horizontal.TProgressbar"
        )
        self.progressbar.pack()

        # Start animation with visible speed
        # 10ms between steps = smooth animation
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
        if hasattr(self, 'message_label'):
            self.message_label.config(text=message, bg="#f0f0f0")
            self.dialog.update_idletasks()
            self.dialog.update()

    def close(self) -> None:
        """Close the loading dialog."""
        self.progressbar.stop()
        self.dialog.destroy()
