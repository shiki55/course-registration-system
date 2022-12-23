"""
This module contains the PrettyTableWrapper class, which extends the PrettyTable class
from the `prettytable` library.
"""

from prettytable import PrettyTable, ALL

from .text_formatting import bold, underline

class PrettyTableWrapper(PrettyTable):
    """Wrapper for `PrettyTable` class."""
    def __init__(self, field_names=None, **kwargs):
        if field_names is not None:
            # bold & underline column headers
            field_names = list(map(lambda name: underline(bold(name)), field_names))
        super().__init__(field_names, **kwargs)