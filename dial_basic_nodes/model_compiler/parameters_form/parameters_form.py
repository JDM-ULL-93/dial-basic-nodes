# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers
from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QComboBox, QFormLayout, QPushButton, QSpinBox, QWidget


class ParametersForm(QWidget):
    """
    Form for changing the parameters used for the training process.
    """

    compile_model = Signal()

    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        # Initialize widgets
        self.__main_layout = QFormLayout()

        self.__epoch_spinbox = QSpinBox()
        self.__epoch_spinbox.setMinimum(1)

        self.__loss_function_combobox = QComboBox()
        self.__loss_function_combobox.addItems(
            ["mean_squared_error", "binary_crossentropy", "categorical_crossentropy"]
        )

        self.__optimizer_combobox = QComboBox()
        self.__optimizer_combobox.addItems(["Adam", "SDG", "RMSprop"])

        # self.__batch_size_spinbox = QSpinBox()
        # self.__batch_size_spinbox.setRange(1, 99999999)
        # self.__batch_size_spinbox.setValue(32)

        self.__compile_button = QPushButton("Compile model")

        self.__main_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.__main_layout.setFormAlignment(Qt.AlignHCenter)
        self.__main_layout.setHorizontalSpacing(50)

        self.__main_layout.addRow("Epochs", self.__epoch_spinbox)
        self.__main_layout.addRow("Loss functions", self.__loss_function_combobox)
        self.__main_layout.addRow("Optimizers", self.__optimizer_combobox)
        # self.__main_layout.addRow("Batch Size", self.__batch_size_spinbox)
        self.__main_layout.addWidget(self.__compile_button)

        self.setLayout(self.__main_layout)

        self.__compile_button.clicked.connect(lambda: self.compile_model.emit())

    @property
    def optimizer(self) -> str:
        return self.__optimizer_combobox.currentText()

    @property
    def loss_function(self) -> str:
        return self.__loss_function_combobox.currentText()

    @property
    def batch_size(self) -> int:
        return self.__batch_size_spinbox.value()

    def __getstate__(self):
        return {
            "epoch": self.__epoch_spinbox.value(),
            "loss_function": self.__loss_function_combobox.currentText(),
            "optimizer": self.__optimizer_combobox.currentText(),
            # "batch_size": self.__batch_size_spinbox.value(),
        }

    def __setstate__(self, new_state):
        self.__epoch_spinbox.setValue(new_state["epoch"])
        self.__loss_function_combobox.setCurrentIndex(
            self.__loss_function_combobox.findText(new_state["loss_function"])
        )
        self.__optimizer_combobox.setCurrentIndex(
            self.__optimizer_combobox.findText(new_state["optimizer"])
        )
        # self.__batch_size_spinbox.setValue(new_state["batch_size"])

    def __reduce__(self):
        return (ParametersForm, (), self.__getstate__())


ParametersFormFactory = providers.Factory(ParametersForm)
