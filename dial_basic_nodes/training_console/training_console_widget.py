# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import threading
from enum import Enum

import dependency_injector.providers as providers
from dial_core.utils import log
from PySide2.QtCore import QSize, Signal
from PySide2.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from tensorflow import keras
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model

LOGGER = log.get_logger(__name__)


class TrainingStatus(Enum):
    Running = 1
    Stopped = 2


class TrainingControllerCallback(keras.callbacks.Callback):
    def __init__(self, training_widget):
        super().__init__()
        # Sightly dangerous, but it works
        self.training_widget = training_widget

    def on_train_batch_end(self, batch, logs=None):
        if self.training_widget.training_status == TrainingStatus.Stopped:
            self.model.stop_training = True


class TrainingConsoleWidget(QWidget):
    start_training_triggered = Signal()
    stop_training_triggered = Signal()

    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        self.__start_training_button = QPushButton("Start training", parent=self)
        self.__stop_training_button = QPushButton("Stop training", parent=self)

        self.__buttons_layout = QHBoxLayout()
        self.__buttons_layout.addWidget(self.__start_training_button)
        self.__buttons_layout.addWidget(self.__stop_training_button)

        self.__training_output_textbox = QPlainTextEdit(parent=self)
        self.__training_output_textbox.setReadOnly(True)

        console_output_group = QGroupBox("Console output")
        console_output_layout = QVBoxLayout()
        console_output_layout.setContentsMargins(0, 0, 0, 0)
        console_output_layout.addWidget(self.__training_output_textbox)
        console_output_group.setLayout(console_output_layout)

        self.__main_layout = QVBoxLayout()
        self.__main_layout.addLayout(self.__buttons_layout)
        self.__main_layout.addWidget(console_output_group)
        self.setLayout(self.__main_layout)

        self.__start_training_button.clicked.connect(
            lambda: self.start_training_triggered.emit()
        )

        self.__stop_training_button.clicked.connect(
            lambda: self.stop_training_triggered.emit()
        )

        self.training_status = TrainingStatus.Stopped
        self.__training_thread = None

        self.__trained_model = None

    @property
    def training_status(self):
        return self.__training_status

    @training_status.setter
    def training_status(self, new_status):
        self.__training_status = new_status

        if self.__training_status == TrainingStatus.Running:
            self.__start_training_button.setEnabled(False)
            self.__stop_training_button.setEnabled(True)

        elif self.__training_status == TrainingStatus.Stopped:
            self.__start_training_button.setEnabled(True)
            self.__stop_training_button.setEnabled(False)

    def get_trained_model(self):
        return self.__trained_model

    def compile_model(self, hyperparameters, model, train_dataset):
        LOGGER.debug("Compiling model")

        input_layer = Input(train_dataset.input_shape)
        output = model(input_layer)

        self.__trained_model = Model(input_layer, output)

        try:
            self.__trained_model.compile(
                optimizer=hyperparameters["optimizer"],
                loss=hyperparameters["loss_function"],
                metrics=["accuracy"],
            )
        except Exception as err:
            LOGGER.exception("Model Compiling error: ", err)
            self.__training_output_textbox.setPlainText(
                "> Error while compiling the model:\n", str(err)
            )
            return

        self.__trained_model.summary()

    def start_training(self, hyperparameters, train_dataset, validation_dataset=None):
        print("Starting training!!!!")
        if (
            self.training_status == TrainingStatus.Stopped
            and self.__trained_model is not None
        ):
            self.__training_thread = threading.Thread(
                target=self.__async_fit, args=(train_dataset, hyperparameters)
            )
            self.__training_thread.start()

    def stop_training(self):
        if self.training_status == TrainingStatus.Running:
            self.training_status = TrainingStatus.Stopped
            print("Stopped")

    def __async_fit(self, train_dataset, hyperparameters):
        self.training_status = TrainingStatus.Running

        self.__trained_model.fit(
            train_dataset,
            epochs=hyperparameters["epochs"],
            callbacks=[TrainingControllerCallback(self)],
        )

        self.training_status = TrainingStatus.Stopped

    def sizeHint(self) -> "QSize":
        return QSize(500, 300)

    def __reduce__(self):
        return (TrainingConsoleWidget, ())


TrainingConsoleWidgetFactory = providers.Factory(TrainingConsoleWidget)
