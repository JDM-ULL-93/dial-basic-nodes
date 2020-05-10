# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Optional

import dependency_injector.providers as providers
from PySide2.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QWidget,
)
from tensorflow.keras.models import Model  # noqa: F401

from .predefined_models_window import PredefinedModelsWindowFactory


class PredefinedModelsWidget(QWidget):
    def __init__(self, predefined_models_window, parent: "QWidget" = None):
        super().__init__(parent)

        # Model picker size (left)
        self._predefined_models_window = predefined_models_window

        self._predefined_models_group = QGroupBox("Predefined Models:")
        self._predefined_models_layout = QHBoxLayout()
        self._predefined_models_layout.setContentsMargins(0, 0, 0, 0)
        self._predefined_models_group.setLayout(self._predefined_models_layout)
        self._predefined_models_layout.addWidget(self._predefined_models_window)

        # Description Side (right)
        self._model_name = QLabel("")
        self._include_top = QCheckBox("Include")
        self._include_top.setChecked(True)

        self._description_group = QGroupBox("Description:")
        self._description_layout = QFormLayout()

        self._description_group.setLayout(self._description_layout)

        self._description_layout.addRow("Name:", self._model_name)
        self._description_layout.addRow("Include Top:", self._include_top)

        self._main_layout = QHBoxLayout()
        self._main_layout.addWidget(self._predefined_models_group)
        self._main_layout.addWidget(self._description_group)

        self.setLayout(self._main_layout)

        self._predefined_models_window.selected_model_changed.connect(
            self._update_description_labels
        )

    def get_model(self) -> Optional["Model"]:
        return self._predefined_models_window.get_selected_model()["loader"](
            include_top=self.__include_top.isChecked()
        )

    def _update_description_labels(self, model_desc: dict):
        self._model_name.setText(model_desc["name"])


PredefinedModelsWidgetFactory = providers.Factory(
    PredefinedModelsWidget, predefined_models_window=PredefinedModelsWindowFactory
)
