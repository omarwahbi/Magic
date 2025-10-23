import tkinter as tk
from tkinter import ttk

class AppStyle:
    # Color Palette
    COLOR_PRIMARY = "#2196F3"  # Blue
    COLOR_SUCCESS = "#4CAF50"  # Green
    COLOR_WARNING = "#FF9800"  # Orange
    COLOR_DANGER = "#F44336"   # Red
    COLOR_PURPLE = "#9C27B0"  # Purple
    COLOR_WHITE = "#FFFFFF"
    COLOR_GRAY = "#808080"
    COLOR_BLACK = "#000000"
    
    COLOR_BG_SUCCESS = "#d4edda"
    COLOR_BG_MISSING = "#f8d7da"

    # Fonts
    FONT_BOLD_10 = ("Arial", 10, "bold")
    FONT_BOLD_12 = ("Arial", 12, "bold")
    FONT_NORMAL_10 = ("Arial", 10)
    FONT_NORMAL_12 = ("Arial", 12)

    @staticmethod
    def configure_styles():
        style = ttk.Style()
        
        # --- Button Styles ---
        style.configure("TButton", font=AppStyle.FONT_NORMAL_10, padding=5)
        style.configure("Success.TButton", background=AppStyle.COLOR_SUCCESS, foreground=AppStyle.COLOR_WHITE)
        style.map("Success.TButton", background=[('active', '#45a049')])
        
        style.configure("Primary.TButton", background=AppStyle.COLOR_PRIMARY, foreground=AppStyle.COLOR_WHITE)
        style.map("Primary.TButton", background=[('active', '#1e88e5')])

        style.configure("PrimaryBold.TButton", font=AppStyle.FONT_BOLD_12, background=AppStyle.COLOR_PRIMARY, foreground=AppStyle.COLOR_WHITE)
        style.map("PrimaryBold.TButton", background=[('active', '#1e88e5')])

        style.configure("Warning.TButton", background=AppStyle.COLOR_WARNING, foreground=AppStyle.COLOR_WHITE)
        style.map("Warning.TButton", background=[('active', '#fb8c00')])

        # --- Treeview Style ---
        style.configure("TTreeview", font=AppStyle.FONT_NORMAL_10, rowheight=25)
        style.configure("TTreeview.Heading", font=AppStyle.FONT_BOLD_10)
        style.map("TTreeview",
                  background=[('selected', AppStyle.COLOR_PRIMARY)],
                  foreground=[('selected', AppStyle.COLOR_WHITE)])
        
        # --- Label Styles ---
        style.configure("TLabel", font=AppStyle.FONT_NORMAL_10)
        style.configure("Status.TLabel", font=AppStyle.FONT_NORMAL_10, foreground=AppStyle.COLOR_PRIMARY)
        style.configure("Header.TLabel", font=AppStyle.FONT_BOLD_10)
        style.configure("Danger.TLabel", foreground=AppStyle.COLOR_DANGER)
        style.configure("Warning.TLabel", foreground=AppStyle.COLOR_WARNING)
        style.configure("Purple.TLabel", foreground=AppStyle.COLOR_PURPLE)

        # --- Notebook Style ---
        style.configure("TNotebook.Tab", font=AppStyle.FONT_NORMAL_10, padding=[10, 5])
        style.map("TNotebook.Tab",
                  background=[('selected', AppStyle.COLOR_PRIMARY)],
                  foreground=[('selected', AppStyle.COLOR_WHITE)])

        # --- Frame Styles ---
        style.configure("TFrame", padding=10)
        style.configure("TLabelframe", padding=10)
        style.configure("TLabelframe.Label", font=AppStyle.FONT_BOLD_10)
