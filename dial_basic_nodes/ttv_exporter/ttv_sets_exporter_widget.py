# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers

from dial_core.datasets.io import DatasetIOContainer
from dial_core.utils import log

from PySide2.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QComboBox,
    QFormLayout,
    QPushButton,
    QHBoxLayout,
)

LOGGER = log.get_logger(__name__)


class TTVSetsExporterWidget(QWidget):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        # Components
        self._ttv: Optional["TTVSets"] = None
        self._export_ttv_path = ""

        # Widgets
        self._name_textbox = QLineEdit("Unnamed TTV")
        self._name_textbox.setPlaceholderText("Name")

        self._train_label = QLabel("")
        self._test_label = QLabel("")
        self._validation_label = QLabel("")

        self._export_path_textbox = QLineEdit()
        self._export_path_textbox.setReadOnly(True)
        self._export_path_button = QPushButton("Directory...")

        self._export_button = QPushButton("Export")

        self._ttv_info_layout = QFormLayout()
        self._ttv_info_layout.addRow("Name:", self._name_textbox)
        self._ttv_info_layout.addRow("Train:", self._train_label)
        self._ttv_info_layout.addRow("Test:", self._test_label)
        self._ttv_info_layout.addRow("Validation:", self._validation_label)

        self._export_path_layout = QHBoxLayout()
        self._export_path_layout.addWidget(self._export_path_textbox)
        self._export_path_layout.addWidget(self._export_path_button)

        self._ttv_info_layout.addRow("Export Path:", self._export_path_layout)

        self._format_combobox = QComboBox()
        for io_format in DatasetIOContainer.providers.values():
            self._format_combobox.addItem(io_format.cls.__name__, io_format)
        self._ttv_info_layout.addRow("Format", self._format_combobox)

        self._main_layout = QVBoxLayout()
        self._main_layout.addLayout(self._ttv_info_layout)
        self._main_layout.addWidget(self._export_button)

        self.setLayout(self._main_layout)

    def set_ttv(self, ttv: "TTVSets"):
        """Sets a new TTVSets object for exporting."""
        self._ttv = ttv
        self._update_labels_text()

        LOGGER.info(f"TTVSets added to Export: {ttv}")

    def pick_export_path(self):
        LOGGER.debug("Picking a directory to export...")
        ttv_dir

    def _update_labels_text(self):
        """Update the text labels to reflect the TTVSets information"""
        self._train_label.setText(f"{str(self._ttv.train if self._ttv else None)}")
        self._test_label.setText(f"{str(self._ttv.test if self._ttv else None)}")
        self._validation_label.setText(
            f"{str(self._ttv.validation if self._ttv else None)}"
        )


TTVSetsExporterWidgetFactory = providers.Factory(TTVSetsExporterWidget)
