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

    def set_test_dataset(self, test_dataset: "Dataset"):
        print("Set test dataset")
        self.__test_dataset = test_dataset

    def set_compiled_model(self, model: "keras.models.Model"):
        print("Set compiled model")
        self.__compiled_model = model


TestModelWidgetFactory = providers.Factory(TestModelWidget)
