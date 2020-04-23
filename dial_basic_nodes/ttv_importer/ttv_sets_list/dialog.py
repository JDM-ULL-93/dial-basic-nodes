# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, Optional

import dependency_injector.providers as providers
from PySide2.QtCore import Slot
from PySide2.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

from .model import PredefinedTTVSetsListModelFactory, TTVSetsListModelFactory
from .view import TTVSetsListViewFactory

if TYPE_CHECKING:
    from PySide2.QtCore import QModelIndex
    from dial_core.datasets.io import TTVSetsLoader
    from .model import DatasetsListModel
    from .view import DatasetsListView
    from PySide2.QtWidgets import QWidget


class TTVSetsListDialog(QDialog):
    """
    Dialog window for selecting between predefined datasets.
    """

    def __init__(
        self,
        model: "DatasetsListModel",
        view: "DatasetsListView",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self.setWindowTitle("Datasets")

        # Attributes
        self._ttv_sets_loader: Optional["TTVSetsLoader"] = None

        # Setup MVC
        self._model = model
        self._model.setParent(self)
        self._view = view
        self._view.setParent(self)

        self._view.setModel(self._model)

        # Create widgets
        self._name_label = QLabel()
        self._brief_label = QLabel()
        self._types_label = QLabel()

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Create Layouts
        self._main_layout = QHBoxLayout()
        self._description_layout = QFormLayout()

        # Setup UI
        self._setup_ui()

        self._view.activated.connect(self._selected_loader_changed)

    def selected_loader(self) -> Optional["TTVSetsLoader"]:
        """
        Return the loaded currently selected by the Dialog.
        """
        return self._ttv_sets_loader

    def _setup_ui(self):
        # Main layout
        self.setLayout(self._main_layout)

        # Right side (Description)

        self._description_layout.addRow("Name", self._name_label)
        self._description_layout.addRow("Brief", self._brief_label)
        self._description_layout.addRow("Data types:", self._types_label)

        # Extra vertical layout for dialog button_box widget
        right_layout = QVBoxLayout()
        right_layout.addLayout(self._description_layout)
        right_layout.addWidget(self.button_box)

        # Add widgets to main layout
        self._main_layout.addWidget(self._view)
        self._main_layout.addLayout(right_layout)

    @Slot("QModelIndex")
    def _selected_loader_changed(self, index: "QModelIndex"):
        """
        Slot called when a user clicks on any list item.
        """
        self._ttv_sets_loader = index.internalPointer()

        self._update_description(self._ttv_sets_loader)

    @Slot("TTVSetsLoader")
    def _update_description(self, ttv_sets_loader: "TTVSetsLoader"):
        """
        Update the description on the right widget after selecting a new TTVSetsLoader.
        """
        self._name_label.setText(ttv_sets_loader.name)
        self._brief_label.setText(ttv_sets_loader.brief)
        self._types_label.setText(
            ", ".join([str(ttv_sets_loader.x_type), str(ttv_sets_loader.y_type)])
        )


TTVSetsListDialogFactory = providers.Factory(
    TTVSetsListDialog, model=TTVSetsListModelFactory, view=TTVSetsListViewFactory
)

PredefinedTTVSetsListDialogFactory = providers.Factory(
    TTVSetsListDialogFactory,
    model=PredefinedTTVSetsListModelFactory,
    view=TTVSetsListViewFactory,
)
