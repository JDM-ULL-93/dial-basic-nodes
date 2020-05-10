# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import os

import dependency_injector.providers as providers
from dial_core.datasets import TTVSets
from dial_core.datasets.datatype import DataType
from dial_core.datasets.io import NpzDatasetIO, TTVSetsIO
from dial_core.utils import log
from PySide2.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

LOGGER = log.get_logger(__name__)


class FileLoaderGroup(QGroupBox):
    def __init__(
        self,
        title: str,
        parent: "QWidget" = None,
        filter: str = "",
        pick_directories: bool = False,
    ):
        super().__init__(title, parent)

        self._file_picker_dialog = QFileDialog(
            caption=f'Picking a "{title}" file...', filter=filter
        )
        self._file_picker_dialog.setFileMode(
            QFileDialog.DirectoryOnly if pick_directories else QFileDialog.ExistingFile
        )

        self._pick_file_text = QLineEdit()
        self._pick_file_text.setReadOnly(True)
        self._pick_file_text.setPlaceholderText("Path...")
        self._pick_file_button = QPushButton("Load")

        self._pick_file_layout = QHBoxLayout()
        self._pick_file_layout.addWidget(self._pick_file_text)
        self._pick_file_layout.addWidget(self._pick_file_button)

        self._main_layout = QVBoxLayout()
        self._main_layout.addLayout(self._pick_file_layout)

        self.setLayout(self._main_layout)

        self._pick_file_button.clicked.connect(self._load_from_filesystem)

    @property
    def layout(self) -> "QVBoxLayout":
        return self._main_layout

    @property
    def path(self) -> str:
        return self._pick_file_text.text()

    @path.setter
    def path(self, path: str):
        self._pick_file_text.setText(path)

    def _load_from_filesystem(self):
        LOGGER.debug("Picking file...")

        if self._file_picker_dialog.exec():
            self._pick_file_text.setText(self._file_picker_dialog.selectedFiles()[0])


class NpzWidget(QWidget):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        self._train_file_loader = FileLoaderGroup("Train", filter="*.npz")
        self._test_file_loader = FileLoaderGroup("Test", filter="*.npz")
        self._validation_file_loader = FileLoaderGroup("Validation", filter="*.npz")

        self._main_layout = QVBoxLayout()
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.addWidget(self._train_file_loader)
        self._main_layout.addWidget(self._test_file_loader)
        self._main_layout.addWidget(self._validation_file_loader)

        self.setLayout(self._main_layout)

    def load_ttv(self, name: str, x_type: DataType, y_type: DataType):
        LOGGER.debug("Loading TTV %s", name)

        def load_dataset(filename):
            return (
                NpzDatasetIO()
                .set_x_type(x_type)
                .set_y_type(y_type)
                .set_filename(filename)
                .load(parent_dir="")  # Absolute path set on filename
            )

        train = load_dataset(self._train_file_loader.path)
        test = load_dataset(self._test_file_loader.path)
        validation = load_dataset(self._validation_file_loader.path)

        return TTVSets(name, train, test, validation)

    def update_widgets(self, ttv_dir: str, ttv_description: dict):
        def update_file_loader_path(file_loader, dataset_dir, dataset_description):
            if "filename" in dataset_description:
                file_loader.path = os.path.join(
                    ttv_dir, dataset_dir, dataset_description["filename"]
                )
            else:
                file_loader.path = ""

        update_file_loader_path(
            self._train_file_loader, "train", ttv_description["train"]
        )
        update_file_loader_path(self._test_file_loader, "test", ttv_description["test"])
        update_file_loader_path(
            self._validation_file_loader, "validation", ttv_description["validation"]
        )


NpzWidgetFactory = providers.Factory(NpzWidget)
