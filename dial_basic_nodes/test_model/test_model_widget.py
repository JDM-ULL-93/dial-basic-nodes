# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Optional

import dependency_injector.providers as providers
from dial_core.datasets import Dataset
from PySide2.QtWidgets import QWidget
from tensorflow import keras


class TestModelWidget(QWidget):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        self.__test_dataset: Optional["Dataset"] = None
        self.__compiled_model: Optional["keras.models.Model"] = None

        self.__accuracy = 0

    def set_test_dataset(self, test_dataset: "Dataset"):
        print("Set test dataset")
        self.__test_dataset = test_dataset

        self.predict_values()

    def set_compiled_model(self, model: "keras.models.Model"):
        print("Set compiled model")
        self.__compiled_model = model

        self.predict_values()

    def predict_values(self):
        if self.__test_dataset is None or self.__compiled_model is None:
            return

        X = self.__compiled_model.predict(self.__test_dataset)
        print("Predicted")


TestModelWidgetFactory = providers.Factory(TestModelWidget)
