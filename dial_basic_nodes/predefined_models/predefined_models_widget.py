# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Optional

import dependency_injector.providers as providers
from PySide2.QtWidgets import QWidget
from tensorflow.keras.models import Model  # noqa: F401


class PredefinedModelsWidget(QWidget):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        self._model: Optional["Model"] = None

    def get_model(self) -> Optional["Model"]:
        return self._model


PredefinedModelsWidgetFactory = providers.Factory(PredefinedModelsWidget)
