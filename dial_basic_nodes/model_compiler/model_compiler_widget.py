# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.utils import log
from PySide2.QtWidgets import QGridLayout, QWidget

from .parameters_form import ParametersFormFactory

if TYPE_CHECKING:
    from .parameters_form import ParametersForm


LOGGER = log.get_logger(__name__)


class ModelCompilerWidget(QWidget):
    def __init__(self, parameters_form: "ParametersForm", parent: "QWidget" = None):
        super().__init__(parent)

        # Initialize widgets
        self.__main_layout = QGridLayout()
        self.__parameters_form = parameters_form

        # Configure interface
        self.__main_layout.addWidget(self.__parameters_form)

        self.setLayout(self.__main_layout)

    def __reduce__(self):
        return (ModelCompilerWidget, (self.__parameters_form,))


ModelCompilerWidgetFactory = providers.Factory(
    ModelCompilerWidget, parameters_form=ParametersFormFactory
)
