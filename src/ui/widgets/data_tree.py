"""Reusable TreeView widget for displaying data."""

import tkinter as tk
from tkinter import ttk
from typing import List, Tuple, Callable, Optional


class DataTreeView(ttk.Frame):
    """Reusable TreeView widget with scrollbar."""

    def __init__(
        self,
        parent: tk.Widget,
        columns: List[Tuple[str, str, int]],
        height: int = 15,
        **kwargs
    ):
        """
        Initialize DataTreeView.

        Args:
            parent: Parent widget
            columns: List of (id, heading, width) tuples
            height: Number of visible rows
        """
        super().__init__(parent, **kwargs)
        self.columns = columns

        # Extract column IDs
        column_ids = [col[0] for col in columns]

        # Create treeview
        self.tree = ttk.Treeview(
            self,
            columns=column_ids,
            show="headings",
            height=height
        )

        # Configure columns
        for col_id, heading, width in columns:
            self.tree.heading(col_id, text=heading)
            self.tree.column(col_id, width=width)

        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Layout
        self.tree.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")



    def insert(self, values: Tuple, tags: Tuple = ()) -> str:
        """
        Insert a row into the tree.

        Args:
            values: Values for each column
            tags: Tags for styling

        Returns:
            Item ID
        """
        return self.tree.insert("", "end", values=values, tags=tags)

    def clear(self) -> None:
        """Clear all items from tree."""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def get_children(self) -> Tuple[str, ...]:
        """Get all child item IDs."""
        return self.tree.get_children()

    def get_item_values(self, item_id: str) -> Tuple:
        """Get values for an item."""
        return self.tree.item(item_id)['values']

    def get_selection(self) -> Tuple[str, ...]:
        """Get selected item IDs."""
        return self.tree.selection()

    def update_item(self, item_id: str, values: Tuple, tags: Tuple = ()) -> None:
        """
        Update an item's values.

        Args:
            item_id: Item to update
            values: New values
            tags: New tags
        """
        self.tree.item(item_id, values=values, tags=tags)

    def configure_tag(self, tag: str, **kwargs) -> None:
        """
        Configure a tag for styling.

        Args:
            tag: Tag name
            **kwargs: Style properties (background, foreground, etc.)
        """
        self.tree.tag_configure(tag, **kwargs)

    def bind_selection(self, callback: Callable) -> None:
        """
        Bind selection event.

        Args:
            callback: Function to call on selection
        """
        self.tree.bind('<<TreeviewSelect>>', callback)
