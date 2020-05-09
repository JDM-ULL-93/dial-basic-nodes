# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from PySide2.QtWidgets import QListWidget

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget


class CategoricalWidget(QListWidget):
    def __init__(self, categorical_datatype, parent: "QWidget" = None):
        super().__init__(parent)

        self._categorical_datatype = categorical_datatype

        for category in self._categorical_datatype.categories:
            self.addItem(category)

        print("Categorical")


CategoricalWidgetFactory = providers.Factory(CategoricalWidget)
