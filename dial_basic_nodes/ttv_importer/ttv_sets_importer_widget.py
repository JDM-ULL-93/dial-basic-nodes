# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


from typing import Optional

import dependency_injector.providers as providers
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QFileDialog, QPushButton, QVBoxLayout, QWidget

from dial_core.datasets import TTVSets
from dial_core.datasets.io import TTVSetsFormatsContainer, TTVSetsIO
from dial_core.utils import log

from .ttv_sets_list import PredefinedTTVSetsListDialogFactory, TTVSetsListDialog

LOGGER = log.get_logger(__name__)


class TTVSetsImporterWidget(QWidget):
    ttv_loaded = Signal(TTVSets)

    def __init__(self, ttv_sets_dialog: "TTVSetsListDialog", parent: "QWidget" = None):
        super().__init__(parent)

        # Components
        self._ttv: Optional["TTVSets"] = None

        self._ttv_sets_dialog = ttv_sets_dialog

        # Widgets
        self._directory_picker_button = QPushButton("Load TTV...")
        self._directory_picker_button.clicked.connect(self._load_ttv_from_filesys)

        self._predefined_load_button = QPushButton("Load predefined datasets...")
        self._predefined_load_button.clicked.connect(self._load_predefined_datasets)

        self._main_layout = QVBoxLayout()
        self._main_layout.addWidget(self._directory_picker_button)
        self._main_layout.addWidget(self._predefined_load_button)

        self.setLayout(self._main_layout)

    def get_ttv(self) -> "TTVSets":
        """Returns the loaded TTVSets object."""
        return self._ttv

    def _load_ttv_from_filesys(self):
        LOGGER.debug("Picking a TTV Directory...")
        selected_ttv_dir = QFileDialog.getExistingDirectory(
            parent=self,
            caption="TTV Folder",
            options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )

        if not selected_ttv_dir:
            LOGGER.debug("Loading cancelled...")
            return

        try:
            self._ttv = TTVSetsIO.load(selected_ttv_dir, TTVSetsFormatsContainer)

            LOGGER.info(f"TTVSets loaded! {self._ttv}")
            self.ttv_loaded.emit(self._ttv)

        except IOError as err:
            LOGGER.exception("Couldn't load TTV Sets!", err)

    def _load_predefined_datasets(self):
        exit_code = self._ttv_sets_dialog.exec_()

        if exit_code == 1:
            self._ttv = self._ttv_sets_dialog.selected_loader().load()

            LOGGER.info(f"TTVSets loaded! {self._ttv}")
            self.ttv_loaded.emit(self._ttv)
        else:
            LOGGER.debug("Loading cancelled...")

    def __reduce__(self):
        return (TTVSetsImporterWidget, (), super().__getstate__())


TTVSetsImporterWidgetFactory = providers.Factory(
    TTVSetsImporterWidget, ttv_sets_dialog=PredefinedTTVSetsListDialogFactory
)
