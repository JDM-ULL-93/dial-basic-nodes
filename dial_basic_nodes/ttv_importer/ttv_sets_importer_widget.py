# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


from typing import Optional

import dependency_injector.providers as providers
from PySide2.QtCore import QSize, Signal
from PySide2.QtWidgets import QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget

from dial_core.datasets import TTVSets
from dial_core.datasets.io import TTVSetsFormatsContainer, TTVSetsIO
from dial_core.utils import log

from .ttv_sets_list import PredefinedTTVSetsListDialogFactory, TTVSetsListDialog

LOGGER = log.get_logger(__name__)


class TTVSetsImporterWidget(QWidget):
    ttv_loaded = Signal(TTVSets)

    def __init__(
        self, ttv_sets_dialog: "TTVSetsListDialog", parent: "QWidget" = None,
    ):
        super().__init__(parent)

        # Components
        self._ttv: Optional["TTVSets"] = None

        self._ttv_sets_dialog = ttv_sets_dialog

        # Widgets
        self._directory_picker_button = QPushButton("Load TTV from file...")
        self._directory_picker_button.clicked.connect(self.pick_ttv_from_filesystem)

        self._predefined_load_button = QPushButton("Load predefined datasets...")
        self._predefined_load_button.clicked.connect(self.pick_predefined_ttv)

        self._name_label = QLabel("Name:")
        self._train_label = QLabel("Train:")
        self._test_label = QLabel("Test:")
        self._validation_label = QLabel("Validation:")

        self._main_layout = QVBoxLayout()
        self._main_layout.addWidget(self._directory_picker_button)
        self._main_layout.addWidget(self._predefined_load_button)
        self._main_layout.addWidget(self._name_label)
        self._main_layout.addWidget(self._train_label)
        self._main_layout.addWidget(self._test_label)
        self._main_layout.addWidget(self._validation_label)

        self.setLayout(self._main_layout)

    def get_ttv(self) -> "TTVSets":
        """Returns the loaded TTVSets object."""
        return self._ttv

    def set_ttv(self, ttv: "TTVSets"):
        """Sets a new TTVSets object as the loaded ttv."""
        self._ttv = ttv
        self._update_labels_text()
        self.ttv_loaded.emit(self._ttv)

        LOGGER.info(f"TTVSets loaded: {ttv}")

    def pick_ttv_from_filesystem(self):
        """Shows a dialog for picking a directory from the filesystem.

        The selected directory will be loaded as a TTVSets dataset.
        """
        LOGGER.debug("Picking a TTV Directory...")
        selected_ttv_dir = QFileDialog.getExistingDirectory(
            parent=self,
            caption="TTV Folder",
            options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )

        if not selected_ttv_dir:
            LOGGER.debug("Loading cancelled...")
            return

        self.load_ttv_from_dir(selected_ttv_dir)

    def pick_predefined_ttv(self):
        """Picks and loads a TTVSets object from a predefined list of TTVSetsLoaders."""
        exit_code = self._ttv_sets_dialog.exec_()

        if exit_code != 1:
            LOGGER.debug("Loading cancelled...")
            return

        ttv = self._ttv_sets_dialog.selected_loader().load()
        self.set_ttv(ttv)

    def load_ttv_from_dir(self, ttv_dir: str):
        """Loads a TTVSets object from a directory."""
        try:
            ttv = TTVSetsIO.load(ttv_dir, TTVSetsFormatsContainer)
            self.set_ttv(ttv)

        except IOError as err:
            LOGGER.exception("Couldn't load TTV Sets!", err)

    def _update_labels_text(self):
        """Update the text labels to reflect the TTVSets information"""
        self._name_label.setText(f"Name: {self._ttv.name if self._ttv else ''}")
        self._train_label.setText(
            f"Train: {str(self._ttv.train if self._ttv else None)}"
        )
        self._test_label.setText(f"Test: {str(self._ttv.test if self._ttv else None)}")
        self._validation_label.setText(
            f"Validation: {str(self._ttv.validation if self._ttv else None)}"
        )

    def sizeHint(self) -> "QSize":
        """Optimal size of the widget."""
        return QSize(450, 150)

    def __reduce__(self):
        return (
            TTVSetsImporterWidget,
            (self._ttv_sets_dialog, None),
        )


TTVSetsImporterWidgetFactory = providers.Factory(
    TTVSetsImporterWidget, ttv_sets_dialog=PredefinedTTVSetsListDialogFactory,
)
