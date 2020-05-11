# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Optional

import dependency_injector.providers as providers
from dial_core.datasets import TTVSets
from PySide2.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)


class DataAugmentationOperationsColumn(QWidget):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        self._main_layout = QVBoxLayout()

        # Initialize widets
        self._target_size_group = QGroupBox("Change Image Output Size")
        self._target_size_textbox = QLineEdit()
        self._target_size_textbox.setEnabled(False)

        # Target Size group
        self._target_size_enabled = QCheckBox("Enabled")
        self._target_size_enabled.setChecked(False)
        self._target_size_layout = QVBoxLayout()
        self._target_size_layout.addWidget(self._target_size_enabled)
        self._target_size_layout.addWidget(self._target_size_textbox)

        self._target_size_group.setLayout(self._target_size_layout)

        self._target_size_enabled.stateChanged.connect(
            lambda i: self._target_size_textbox.setEnabled(i)
        )

        self._main_layout.addWidget(self._target_size_group)

        self.setLayout(self._main_layout)

    @property
    def target_size(self):
        return self._target_size_textbox.text()

    @target_size.setter
    def target_size(self, new_target_size: str):
        self._target_size_textbox.setText(new_target_size)


class DataAugmentationWidget(QWidget):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        # Components
        self._ttv: Optional["TTVSets"] = None

        # Initialize widgets
        self._x_augmentation_operations = DataAugmentationOperationsColumn()
        self._y_augmentation_operations = DataAugmentationOperationsColumn()

        # Setup Layout
        self._main_layout = QHBoxLayout()
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.addWidget(self._x_augmentation_operations)
        self._main_layout.addWidget(self._y_augmentation_operations)

        self.setLayout(self._main_layout)

    def set_ttv(self, ttv: "TTVSets"):
        self._ttv = ttv

        def fill_column_values_from_dataset(dataset, label):
            if label == "x":
                self._x_augmentation_operations.target_size = str(dataset.input_shape)
            elif label == "y":
                self._y_augmentation_operations.target_size = str(dataset.output_shape)

        for dataset in (ttv.train, ttv.test, ttv.validation):
            if dataset is None:
                continue

            fill_column_values_from_dataset(dataset, "x")
            fill_column_values_from_dataset(dataset, "y")
            break

    def get_augmented_ttv(self):
        return self._ttv


DataAugmentationWidgetFactory = providers.Factory(DataAugmentationWidget)
