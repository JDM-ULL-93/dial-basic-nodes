# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers
from dial_core.datasets import Dataset
from PySide2.QtCore import QSize
from PySide2.QtWidgets import (
    QFormLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QSplitter,
    QWidget,
)

from .dataset_table import TrainTestTabs, TrainTestTabsFactory
from .datasets_list import PredefinedDatasetsList


class DatasetEditorWidget(QWidget):
    """
    Window for all the dataset related operations (Visualization, loading...)
    """

    def __init__(self, train_test_tabs: "TrainTestTabs", parent: "QWidget" = None):
        super().__init__(parent)

        # Initialize widgets
        self.__main_layout = QGridLayout()
        self.__options_layout = QFormLayout()

        self.__train_test_tabs = train_test_tabs
        self.__train_test_tabs.setParent(self)

        self.__dataset_name_label = QLabel("")
        self.__dataset_loader_button = QPushButton("More...")

        self.__train_len_label = QLabel("")
        self.__test_len_label = QLabel("")

        # Configure interface
        self.__setup_ui()

        # Connections
        self.__dataset_loader_button.clicked.connect(self.__load_predefined_dataset)

        self.__train_test_tabs.train_dataset_changed.connect(self.__update_train_labels)
        self.__train_test_tabs.test_dataset_changed.connect(self.__update_test_labels)
        self.__update_train_labels(self.get_train_dataset())
        self.__update_test_labels(self.get_test_dataset())

    def get_train_dataset(self) -> "Dataset":
        return self.__train_test_tabs.train_dataset()

    def get_test_dataset(self) -> "Dataset":
        return self.__train_test_tabs.test_dataset()

    def sizeHint(self) -> "QSize":
        return QSize(500, 300)

    def __setup_ui(self):
        splitter = QSplitter()

        # Set label names
        self.__options_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.__options_layout.addRow("Dataset name", self.__dataset_name_label)
        self.__options_layout.addRow("Total items (train)", self.__train_len_label)
        self.__options_layout.addRow("Total items (test)", self.__test_len_label)
        self.__options_layout.addRow(
            "Load predefined dataset", self.__dataset_loader_button
        )

        options_widget = QWidget()
        options_widget.setLayout(self.__options_layout)

        splitter.addWidget(options_widget)
        splitter.addWidget(self.__train_test_tabs)

        self.__main_layout.addWidget(splitter, 0, 0)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)

    def __load_predefined_dataset(self):
        datasets_loader_dialog = PredefinedDatasetsList.Dialog()

        accepted = datasets_loader_dialog.exec()

        if accepted:
            dataset_loader = datasets_loader_dialog.selected_loader()

            train, test = dataset_loader.load()

            self.__train_test_tabs.set_train_dataset(train)
            self.__train_test_tabs.set_test_dataset(test)

            self.__dataset_name_label.setText(dataset_loader.name)
            self.__update_train_labels(train)
            self.__update_test_labels(test)

    def __update_train_labels(self, dataset):
        self.__train_len_label.setText(str(dataset.row_count()))

    def __update_test_labels(self, dataset):
        self.__test_len_label.setText(str(dataset.row_count()))

    def __getstate__(self):
        return {
            "dataset_name": self.__dataset_name_label.text(),
            "train_len": self.__train_len_label.text(),
            "test_len": self.__test_len_label.text(),
        }

    def __setstate__(self, new_state):
        self.__dataset_name_label.setText(new_state["dataset_name"])
        self.__train_len_label.setText(new_state["train_len"])
        self.__test_len_label.setText(new_state["test_len"])

    def __reduce__(self):
        return (DatasetEditorWidget, (self.__train_test_tabs,), self.__getstate__())


DatasetEditorWidgetFactory = providers.Factory(
    DatasetEditorWidget, train_test_tabs=TrainTestTabsFactory
)
