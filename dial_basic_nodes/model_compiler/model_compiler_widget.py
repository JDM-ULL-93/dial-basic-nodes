# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.utils import log
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QPlainTextEdit, QVBoxLayout, QWidget
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Sequential

from .parameters_form import ParametersFormFactory

if TYPE_CHECKING:
    from .parameters_form import ParametersForm


LOGGER = log.get_logger(__name__)


class ModelCompilerWidget(QWidget):
    loss_function_changed = Signal(str)
    optimizer_changed = Signal(str)
    compilation_triggered = Signal()

    def __init__(self, parameters_form: "ParametersForm", parent: "QWidget" = None):
        super().__init__(parent)

        self.__model = None

        self.__main_layout = QVBoxLayout()
        self.__parameters_form = parameters_form

        self.__compilation_output_textbox = QPlainTextEdit(parent=self)
        self.__compilation_output_textbox.setReadOnly(True)

        self.__main_layout.addWidget(self.__parameters_form)
        self.__main_layout.addWidget(self.__compilation_output_textbox)
        self.setLayout(self.__main_layout)

        self.__parameters_form.loss_function_changed.connect(
            lambda value: self.loss_function_changed.emit(value)
        )
        self.__parameters_form.optimizer_changed.connect(
            lambda value: self.optimizer_changed.emit(value)
        )
        self.__parameters_form.compilation_triggered.connect(
            lambda: self.compilation_triggered.emit()
        )

    def get_model(self):
        return self.__model

    def compile_model(self, input_shape, layers) -> bool:
        print("Input shape: ", input_shape)
        print("Compiling layers: ", layers)

        try:
            self.__model = Sequential()
            self.__model.add(Input(input_shape))

            for layer in layers:
                self.__model.add(layer)

            self.__model.summary(print_fn=LOGGER.info)

            self.__model.compile(
                optimizer=self.__parameters_form.optimizer,
                loss=self.__parameters_form.loss_function,
                metrics=["accuracy"],
            )
            self.__compilation_output_textbox.setPlainText("Model compiled!")
        except Exception as err:
            print(err)
            self.__compilation_output_textbox.setPlainText(str(err))
            return False

        return True

    def __reduce__(self):
        return (ModelCompilerWidget, (self.__parameters_form,))


ModelCompilerWidgetFactory = providers.Factory(
    ModelCompilerWidget, parameters_form=ParametersFormFactory
)
