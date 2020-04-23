# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Widgets for displaying a dialog with predefined datasets that can be loaded.
"""

from .dialog import (
    PredefinedTTVSetsListDialogFactory,
    TTVSetsListDialog,
    TTVSetsListDialogFactory,
)

__all__ = [
    "PredefinedTTVSetsListDialogFactory",
    "TTVSetsListDialogFactory",
    "TTVSetsListDialog",
]