# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import re

import dependency_injector.providers as providers
from dial_core.datasets import TTVSets
from dial_core.datasets.datatype import DataType
from dial_core.datasets.io import CategoricalImgDatasetIO
from dial_core.utils import log
from PySide2.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from .file_loader_group import FileLoaderGroup

LOGGER = log.get_logger(__name__)


class CategoricalImagesWidget(QWidget):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        self._main_layout = QVBoxLayout()
        self._main_layout.addWidget(QLabel("Not Implemented"))

        self._train_dir_loader = FileLoaderGroup("Train", pick_directories=True)
        self._test_dir_loader = FileLoaderGroup("Test", pick_directories=True)
        self._validation_dir_loader = FileLoaderGroup(
            "Validation", pick_directories=True
        )

        self._organization_combobox = QComboBox()
        self._organization_combobox.addItem(
            "Extract Category from Folders",
            CategoricalImgDatasetIO.Organization.CategoryOnFolders,
        )
        self._organization_combobox.addItem(
            "Extract Category from Filename",
            CategoricalImgDatasetIO.Organization.CategoryOnFilename,
        )

        self._category_regex_textbox = QLineEdit("(.*)")
        self._category_regex_layout = QFormLayout()
        self._category_regex_layout.addRow(
            "Regex for extracting the category from filename",
            self._category_regex_textbox,
        )

        self._regex_test_input_textbox = QLineEdit()
        self._regex_test_output_textbox = QLineEdit()
        self._regex_test_output_textbox.setReadOnly(True)

        self._regex_test_layout = QHBoxLayout()
        self._regex_test_layout.addWidget(QLabel("Test: (Input)"))
        self._regex_test_layout.addWidget(self._regex_test_input_textbox)
        self._regex_test_layout.addWidget(QLabel(" => Output: "))
        self._regex_test_layout.addWidget(self._regex_test_output_textbox)

        self._options_groupbox = QGroupBox()

        self._main_layout = QVBoxLayout()
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.addWidget(self._train_dir_loader)
        self._main_layout.addWidget(self._test_dir_loader)
        self._main_layout.addWidget(self._validation_dir_loader)
        self._main_layout.addWidget(self._organization_combobox)
        self._main_layout.addLayout(self._category_regex_layout)
        self._main_layout.addLayout(self._regex_test_layout)

        self.setLayout(self._main_layout)

        self._category_regex_textbox.textChanged.connect(lambda: self._reload_regex())
        self._regex_test_input_textbox.textChanged.connect(lambda: self._reload_regex())

        self._reload_regex()

    def load_ttv(self, name: str, x_type: DataType, y_type: DataType):
        LOGGER.debug("Loading TTV %s", name)

        def load_dataset(dataset_dir):
            return (
                # Subdir
                # Organization
                # Categories
                CategoricalImgDatasetIO()
                .set_x_type(x_type)
                .set_y_type(y_type)
                .set_organization(self._organization_combobox.currentData())
                .set_filename_category_regex(self._category_regex_textbox.text())
                .load(dataset_dir)  # Absolute path set on filename
            )

        train = load_dataset(self._train_dir_loader.path)
        test = load_dataset(self._test_dir_loader.path)
        validation = load_dataset(self._validation_dir_loader.path)

        return TTVSets(name, train, test, validation)

    def _reload_regex(self):
        regex_string = self._category_regex_textbox.text()

        input_text = self._regex_test_input_textbox.text()

        match = re.match(regex_string, input_text)

        if match:
            try:
                self._regex_test_output_textbox.setText(match.group(1))
            except KeyError:
                self._regex_test_output_textbox.setText(match.group(0))
        else:
            self._regex_test_output_textbox.setText("[No match]")


CategoricalImagesWidgetFactory = providers.Factory(CategoricalImagesWidget)
