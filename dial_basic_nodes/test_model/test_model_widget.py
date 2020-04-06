# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Optional

import dependency_injector.providers as providers
from dial_core.datasets import Dataset
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QVBoxLayout, QWidget
from tensorflow import keras

from .test_dataset_table import TestDatasetTableWidgetFactory


class TestModelWidget(QWidget):
    # Top: Data about the current model.
    # (Name, Training accuracy? Dunno)
    # Bottom: List with all the training dataset things
    # Three columns: Class, Predicted, Expected
    # Accuracy of the test
    # Possibility to filter and see only the failed tests, for example.
    # When the button (Check tests) is clicked, update the predicted values.
    def __init__(self, test_dataset_widget, parent: "QWidget" = None):
        super().__init__(parent)

        # Componentes
        self.__compiled_model: Optional["keras.models.Model"] = None

        # Widgets
        self.__test_dataset_widget = test_dataset_widget

        self.__main_layout = QVBoxLayout()
        self.__main_layout.setContentsMargins(0, 0, 0, 0)
        self.__main_layout.addWidget(self.__test_dataset_widget)

        self.setLayout(self.__main_layout)

    def set_test_dataset(self, test_dataset: "Dataset"):
        print("Set test dataset")
        self.__test_dataset_widget.load_dataset(test_dataset)

        self.predict_values()

    def set_compiled_model(self, model: "keras.models.Model"):
        print("Set compiled model")
        self.__compiled_model = model

        self.predict_values()

    def predict_values(self):
        if self.__test_dataset_widget.dataset is None or self.__compiled_model is None:
            return

        # X = self.__compiled_model.predict(self.__test_dataset)
        print("Predicted")

    def sizeHint(self) -> "QSize":
        """Optimal size for visualizing the widget."""
        return QSize(500, 300)


TestModelWidgetFactory = providers.Factory(
    TestModelWidget, test_dataset_widget=TestDatasetTableWidgetFactory
)
