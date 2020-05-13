# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import re
from typing import Optional

import dependency_injector.providers as providers
from dial_core.utils import log
from PySide2.QtCore import QSize
from PySide2.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QWidget,
)
from tensorflow.keras.models import Model  # noqa: F401

from .predefined_models_window import PredefinedModelsWindowFactory

LOGGER = log.get_logger(__name__)


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
        self._shape_textbox = QLineEdit("(224, 224, 3)")
        self._shape_textbox.setEnabled(False)

        self._description_group = QGroupBox("Description:")
        self._description_layout = QFormLayout()

        self._description_group.setLayout(self._description_layout)

        self._description_layout.addRow("Name:", self._model_name)
        self._description_layout.addRow("Include Top:", self._include_top)
        self._description_layout.addRow("Input Shape:", self._shape_textbox)

        self._main_layout = QHBoxLayout()
        self._main_layout.addWidget(self._predefined_models_group)
        self._main_layout.addWidget(self._description_group)

        self.setLayout(self._main_layout)

        sp_left = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sp_left.setHorizontalStretch(1)

        self._predefined_models_group.setSizePolicy(sp_left)

        sp_right = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sp_right.setHorizontalStretch(2.5)

        self._description_group.setSizePolicy(sp_right)

        self._include_top.stateChanged.connect(
            lambda state: self._shape_textbox.setEnabled(not state)
        )

        self._predefined_models_window.selected_model_changed.connect(
            self._update_description_labels
        )

    def get_model(self) -> Optional["Model"]:
        try:
            if not self._include_top.isChecked():
                input_shape = tuple(
                    map(int, re.sub("[()]", "", self._shape_textbox.text()).split(","))
                )

                LOGGER.debug("Input tuple: %s", input_shape)

                return self._predefined_models_window.get_selected_model()["loader"](
                    include_top=False, input_shape=input_shape
                )

            return self._predefined_models_window.get_selected_model()["loader"]()

        except TypeError as err:
            LOGGER.exception(err)
            return None

    def sizeHint(self) -> "QSize":
        return QSize(400, 170)

    def _update_description_labels(self, model_desc: dict):
        self._model_name.setText(model_desc["name"])


PredefinedModelsWidgetFactory = providers.Factory(
    PredefinedModelsWidget, predefined_models_window=PredefinedModelsWindowFactory
)
