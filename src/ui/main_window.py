"""Main application window - orchestrates all components."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import logging
import threading
import os
from typing import Optional

from src.config.settings import AppSettings, LoggingConfig
from src.config.extraction_config import ExtractionType
from src.services.pdf_extractor import PDFExtractor
from src.services.excel_handler import ExcelHandler
from src.services.data_validator import DataValidator
from src.services.export_service import ExportService
from src.models.extraction_data import ExtractionResult
from src.ui.components.file_selector import FileSelector
from src.ui.components.type_selector import TypeSelector
from src.ui.components.results_tabs import ResultsTabs
from src.ui.components.issues_tabs import IssuesTabs
from src.ui.components.manual_entry import ManualEntryWidget
from src.ui.widgets.loading_dialog import LoadingDialog
from src.services.settings_manager import SettingsManager


class BalanceUpdaterApp:
    """Main application window."""

    def __init__(self, root: tk.Tk):
        """
        Initialize the application.

        Args:
            root: Root Tk window
        """
        self.root = root
        self.settings_manager = SettingsManager()
        self.app_settings = AppSettings()

        # Configure logging
        LoggingConfig().configure()

        # Configure window
        self.root.title(self.app_settings.WINDOW_TITLE)
        self.root.geometry(f"{self.app_settings.WINDOW_SIZE[0]}x{self.app_settings.WINDOW_SIZE[1]}")
        self.root.state('zoomed') # Start maximized

        # Application state
        self.pdf_files = []
        self.excel_file: Optional[str] = None
        self.extraction_result: Optional[ExtractionResult] = None
        self.excel_codes: set = set()

        # Threading state
        self.extraction_thread_result = None
        self.extraction_thread_error = None

        # Build UI
        self._setup_ui()
        self._load_initial_settings()

    def _load_initial_settings(self):
        """Load settings from file and update UI."""
        settings = self.settings_manager.load_settings()
        excel_path = settings.get("excel_file_path")

        if excel_path and os.path.exists(excel_path):
            self.excel_file = excel_path
            self.excel_path_label.config(text=os.path.basename(excel_path))
            self.excel_tooltip.text = excel_path
        elif excel_path:
            messagebox.showwarning(
                "File Not Found",
                f"The saved Excel file could not be found at:\n{excel_path}\n\nPlease select a new file."
            )
        else:
            self.excel_path_label.config(text="No Excel file selected")

    def _setup_ui(self) -> None:
        """Setup all UI components."""
        # --- Main layout frames ---
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        top_container = ttk.Frame(self.root, padding=10)
        top_container.grid(row=0, column=0, sticky="ew")

        middle_frame = ttk.Frame(self.root, padding=10)
        middle_frame.grid(row=1, column=0, sticky="nsew")
        middle_frame.rowconfigure(0, weight=1)
        middle_frame.columnconfigure(0, weight=1)

        bottom_frame = ttk.Frame(self.root, padding=10)
        bottom_frame.grid(row=2, column=0, sticky="ew")

        # --- Top Frame Content ---
        top_frame = ttk.Frame(top_container)
        top_frame.pack(fill="x")

        # PDF selector
        self.pdf_selector = FileSelector(
            top_frame,
            label_text="1. Select PDF(s):",
            button_text="Browse PDFs",
            file_types=[("PDF files", "*.pdf")],
            multiple=True,
            on_select=self._on_pdf_selected
        )
        self.pdf_selector.grid(row=0, column=0, sticky="ew", pady=(0, 5), columnspan=3)

        # Type selector
        self.type_selector = TypeSelector(top_frame, default_value="Stock", label_text="2. Select Type:")
        self.type_selector.grid(row=1, column=0, sticky="ew", pady=5, columnspan=3)

        # Extract button
        ttk.Button(
            top_frame,
            text="Extract Data",
            command=self._extract_data,
        ).grid(row=0, column=3, rowspan=2, padx=10, pady=10, sticky="ns")

        # Export button
        export_menubutton = ttk.Menubutton(top_frame, text="Export")
        export_menu = tk.Menu(export_menubutton, tearoff=False)
        export_menubutton["menu"] = export_menu
        export_menu.add_command(label="Export Unmatched", command=self._export_unmatched)
        export_menu.add_command(label="Export Expired", command=self._export_expired)
        export_menu.add_command(label="Export Duplicates", command=self._export_duplicates)
        export_menu.add_command(label="Export Zero Balance", command=self._export_zero_balance)
        export_menubutton.grid(row=0, column=4, rowspan=2, padx=10, pady=10, sticky="ns")

        # --- Settings Frame ---
        settings_frame = ttk.LabelFrame(top_container, text="Settings", padding=(10, 5))
        settings_frame.pack(fill="x", padx=10, pady=(5, 10))

        ttk.Label(settings_frame, text="Default Excel File:").grid(row=0, column=0, sticky="w")
        
        self.excel_path_label = ttk.Label(settings_frame, text="Not Selected", anchor="w")
        self.excel_path_label.grid(row=0, column=1, sticky="ew", padx=5)
        
        from src.ui.widgets.tooltip import ToolTip
        self.excel_tooltip = ToolTip(self.excel_path_label, "")

        ttk.Button(
            settings_frame,
            text="Change...",
            command=self._select_excel_file,
        ).grid(row=0, column=2)
        
        settings_frame.columnconfigure(1, weight=1)

        # --- Middle Frame Content ---
        # Main content notebook
        main_notebook = ttk.Notebook(middle_frame)
        main_notebook.grid(row=0, column=0, sticky="nsew")

        # Results frame
        results_frame = ttk.Frame(main_notebook)
        main_notebook.add(results_frame, text="Extraction Results")

        self.results_tabs = ResultsTabs(
            results_frame,
            on_export_unmatched=self._export_unmatched
        )
        self.results_tabs.pack(fill="both", expand=True)

        # Issues frame
        issues_frame = ttk.Frame(main_notebook)
        main_notebook.add(issues_frame, text="Data Issues")

        self.issues_tabs = IssuesTabs(
            issues_frame,
            on_export_expired=self._export_expired,
            on_export_duplicates=self._export_duplicates,
            on_export_zero_balance=self._export_zero_balance
        )
        self.issues_tabs.pack(fill="both", expand=True)

        # --- Bottom Frame Content ---
        # Manual entry widget
        self.manual_entry = ManualEntryWidget(
            bottom_frame,
            on_update=self._handle_manual_update,
        )
        self.manual_entry.pack(fill="x", padx=10, pady=5)

        # Save button
        self.save_button = ttk.Button(
            bottom_frame,
            text="Save Updated Excel",
            command=self._save_excel,
        )
        self.save_button.pack(pady=10, padx=10, fill="x")

        # Status label
        self.status_label = ttk.Label(bottom_frame, text="Ready", anchor="w")
        self.status_label.pack(pady=(0, 5), fill="x")

    def _on_pdf_selected(self, files) -> None:
        """Handle PDF files selection."""
        self.pdf_files = files
        self.status_label.config(text=f"{len(files)} PDF(s) selected.")

    def _select_excel_file(self) -> None:
        """Handle Excel file selection and save to settings."""
        file = filedialog.askopenfilename(
            title="Select the default Excel file",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if not file:
            return

        self.excel_file = file
        self.excel_path_label.config(text=os.path.basename(file))
        self.excel_tooltip.text = file
        
        # Save to settings
        current_settings = self.settings_manager.load_settings()
        current_settings["excel_file_path"] = file
        self.settings_manager.save_settings(current_settings)
        
        messagebox.showinfo("Settings Saved", f"Default Excel file has been set to:\n{file}")

    def _extract_data(self) -> None:
        """Extract data from PDFs using background thread."""
        logging.debug("--- Starting Extraction ---")

        # Validate selections
        if not self.pdf_selector.has_selection():
            messagebox.showerror("Error", "Please select at least one PDF file.")
            logging.error("Execution stopped: PDF file not selected.")
            return
            
        if not self.excel_file:
            messagebox.showerror("Error", "Please set the default Excel file in Settings.")
            logging.error("Execution stopped: Excel file not set.")
            return

        self.status_label.config(text="Extracting...")
        self.root.update_idletasks()

        # Reset thread state
        self.extraction_thread_result = None
        self.extraction_thread_error = None

        # Show loading dialog
        loading_dialog = LoadingDialog(
            self.root,
            message=f"Processing {len(self.pdf_files)} PDF file(s)... Please wait."
        )

        # Start extraction in background thread (daemon=True so it closes with app)
        thread = threading.Thread(
            target=self._run_extraction_thread,
            args=(loading_dialog,),
            daemon=True
        )
        thread.start()

        # Check periodically if thread is done
        self._check_extraction_complete(loading_dialog, thread)

    def _run_extraction_thread(self, loading_dialog: LoadingDialog) -> None:
        """
        Run extraction in background thread.

        Args:
            loading_dialog: Loading dialog to update with progress
        """
        try:
            # Get extraction type
            extraction_type = self.type_selector.get_extraction_type()
            logging.debug(f"Extraction type selected: {extraction_type.value}")

            # Extract from PDFs with progress updates
            extractor = PDFExtractor(extraction_type)

            def progress_callback(message: str):
                """Thread-safe progress update."""
                self.root.after(0, lambda: loading_dialog.update_message(message))

            extraction_data = extractor.extract_from_files(
                self.pdf_files,
                progress_callback=progress_callback
            )

            # Read Excel codes
            self.root.after(0, lambda: loading_dialog.update_message("Reading Excel file..."))
            excel_handler = ExcelHandler(self.excel_file)
            excel_codes = excel_handler.read_codes()

            # Validate and match
            self.root.after(0, lambda: loading_dialog.update_message("Validating and matching data..."))
            validator = DataValidator()
            result = validator.validate_and_match(
                extraction_data,
                excel_codes
            )

            # Store results (thread-safe)
            self.extraction_thread_result = (result, excel_codes)

        except Exception as e:
            logging.error(f"Error during extraction: {e}")
            self.extraction_thread_error = e

    def _check_extraction_complete(self, loading_dialog: LoadingDialog, thread: threading.Thread) -> None:
        """
        Check if extraction thread is complete and handle results.

        Args:
            loading_dialog: Loading dialog to close when done
            thread: The extraction thread
        """
        if thread.is_alive():
            # Still running, check again in 100ms
            self.root.after(100, lambda: self._check_extraction_complete(loading_dialog, thread))
        else:
            # Thread is done, close loading dialog
            loading_dialog.close()

            # Handle errors
            if self.extraction_thread_error:
                messagebox.showerror(
                    "Error",
                    f"An error occurred during extraction: {self.extraction_thread_error}"
                )
                self.status_label.config(text="Extraction failed.")
                return

            # Handle successful results
            if self.extraction_thread_result:
                self.extraction_result, self.excel_codes = self.extraction_thread_result
                self._display_results()
                self.status_label.config(text="Extraction complete.")
            else:
                self.status_label.config(text="Extraction completed with no data.")

    def _display_results(self) -> None:
        """Display extraction results in UI."""
        if not self.extraction_result:
            return

        # Populate tabs
        self.results_tabs.populate(self.extraction_result, self.excel_codes)
        self.issues_tabs.populate(self.extraction_result)

        # Update status with statistics
        stats = DataValidator.get_summary_stats(self.extraction_result)
        self.status_label.config(
            text=f"Matched: {stats['matched']} | "
                 f"Missing: {stats['missing']} | "
                 f"Not in Excel: {stats['unmatched']} | "
                 f"Duplicates: {stats['duplicates']} | "
                 f"Expired: {stats['expired']} | "
                 f"Zero Balance: {stats['zero_balance']}"
        )

    def _handle_manual_update(self, balance: float) -> None:
        """
        Handle manual balance update.

        Args:
            balance: New balance value
        """
        selected = self.results_tabs.get_matched_selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a row first")
            return

        code = selected[0]

        # Update extraction result
        if self.extraction_result:
            DataValidator.update_manual_balance(
                self.extraction_result,
                code,
                balance
            )

            # Update display
            self.results_tabs.update_matched_item(code, balance)

    def _save_excel(self) -> None:
        """Save updated Excel file."""
        if not self.extraction_result or not self.extraction_result.matched_codes:
            messagebox.showwarning("Warning", "No data to save")
            return

        try:
            excel_handler = ExcelHandler(self.excel_file)
            extraction_type = self.type_selector.get_extraction_type()

            output_file = excel_handler.update_balances(
                self.extraction_result.matched_codes,
                extraction_type
            )

            messagebox.showinfo(
                "Success",
                f"Saved successfully!\n\n"
                f"Updated: {self.extraction_result.matched_count} items\n"
                f"File: {output_file}"
            )

            self.status_label.config(text=f"✓ Saved: {output_file}")

        except Exception as e:
            messagebox.showerror("Error", f"Save failed: {str(e)}")

    def _export_unmatched(self) -> None:
        """Export unmatched codes to Excel."""
        if not self.extraction_result:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if not file_path:
            return

        try:
            ExportService.export_unmatched_codes(
                self.extraction_result.unmatched_codes,
                file_path
            )
            messagebox.showinfo("Success", f"Unmatched codes exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def _export_expired(self) -> None:
        """Export expired items to Excel."""
        if not self.extraction_result:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if not file_path:
            return

        try:
            ExportService.export_expired_items(
                self.extraction_result.expired_items,
                file_path
            )
            messagebox.showinfo("Success", f"Expired items exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def _export_duplicates(self) -> None:
        """Export duplicate codes to Excel."""
        if not self.extraction_result:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if not file_path:
            return

        try:
            ExportService.export_duplicates(
                self.extraction_result.duplicates,
                file_path
            )
            messagebox.showinfo("Success", f"Duplicate codes exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")

    def _export_zero_balance(self) -> None:
        """Export zero balance items to Excel."""
        if not self.extraction_result:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if not file_path:
            return

        try:
            ExportService.export_zero_balance_items(
                self.extraction_result.zero_balance_items,
                file_path
            )
            messagebox.showinfo("Success", f"Zero balance items exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
