# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.datasets import Dataset
from dial_core.node_editor import Node
from tensorflow.keras import Model

from .training_console_widget import TrainingConsoleWidgetFactory

if TYPE_CHECKING:
    from .training_console_widget import TrainingConsoleWidget


class TrainingConsoleNode(Node):
    def __init__(self, training_console_widget: "TrainingConsoleWidget"):
        super().__init__(title="Training Console", inner_widget=training_console_widget)

        self.add_input_port("Train", port_type=Dataset)
        self.add_input_port("Test", port_type=Dataset)
        self.add_input_port("Validation", port_type=Dataset)
        self.add_input_port("Model", port_type=Model)

        self.inputs["Model"].set_processor_function(self.__model_received)

    def __model_received(self, model):
        print("Printing model summary")
        model.summary()


TrainingConsoleNodeFactory = providers.Factory(
    TrainingConsoleNode, training_console_widget=TrainingConsoleWidgetFactory
)
