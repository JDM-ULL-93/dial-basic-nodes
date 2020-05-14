# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import List

import dependency_injector.providers as providers
from dial_core.utils import log
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QFileDialog, QFormLayout, QLineEdit, QPushButton, QWidget
from tensorflow.keras.callbacks import Callback

LOGGER = log.get_logger(__name__)


class ModelCheckpointWidget(QWidget):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        # Widgets
        self._save_path_textbox = QLineEdit()
        self._save_path_textbox.setPlaceholderText("Directory to save model files...")
        self._save_path_button = QPushButton("Select...")
        self._save_path_button.clicked.connect(self._pick_save_directory)

        # Layouts
        self._main_layout = QFormLayout()
        self._main_layout.addRow("Save directory:", self._save_path_textbox)

        self.setLayout(self._main_layout)

    def get_callbacks(self) -> List[Callback]:
        return []

    def _pick_save_directory(self):
        save_dir = QFileDialog.getExistingDirectory(self, "Save directory...")

        if save_dir:
            self._save_path_textbox.setText(save_dir)
        else:
            LOGGER.debug("Picking save directory cancelled.")

    def sizeHint(self) -> "QSize":
        return QSize(400, 200)

    def __reduce__(self):
        return (ModelCheckpointWidget, (), super().__getstate__())


ModelCheckpointWidgetFactory = providers.Factory(ModelCheckpointWidget)
