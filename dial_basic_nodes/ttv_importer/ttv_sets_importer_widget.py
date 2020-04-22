# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


from typing import TYPE_CHECKING, Optional

import dependency_injector.providers as providers
from PySide2.QtWidgets import QVBoxLayout, QWidget
from dial_core.datasets import TTVSets

if TYPE_CHECKING:
    from dial_core.datasets import TTVSets


class TTVSetsImporterWidget(QWidget):
    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        self._main_layout = QVBoxLayout()

        self._ttv_sets = TTVSets(name="Empty")

        self.setLayout(self._main_layout)

    def get_ttv_sets(self) -> "TTVSets":
        return self._ttv_sets

    def __reduce__(self):
        return (TTVSetsImporterWidget, (), super().__getstate__())


TTVSetsImporterWidgetFactory = providers.Factory(TTVSetsImporterWidget)
