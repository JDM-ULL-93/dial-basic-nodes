# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Optional

import dependency_injector.providers as providers
from dial_core.datasets import TTVSets
from PySide2.QtWidgets import QWidget


class DataAugmentationWidget(QWidget):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        self._ttv: Optional["TTVSets"] = None

    def set_ttv(self, ttv: "TTVSets"):
        self._ttv = ttv

    def get_augmented_ttv(self):
        return self._ttv


DataAugmentationWidgetFactory = providers.Factory(DataAugmentationWidget)
