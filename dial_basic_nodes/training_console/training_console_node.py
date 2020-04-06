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

        self.add_input_port("Train Dataset", port_type=Dataset)
        self.add_input_port("Validation Dataset", port_type=Dataset)
        self.add_input_port("Model", port_type=Model)
        self.add_input_port("Hyperparameters", port_type=dict)

        self.add_output_port("Trained Model", port_type=Model)

        self.inputs["Train Dataset"].set_processor_function(
            self.inner_widget.set_train_dataset
        )
        self.inputs["Validation Dataset"].set_processor_function(
            self.inner_widget.set_validation_dataset
        )
        self.inputs["Model"].set_processor_function(
            self.inner_widget.set_pretrained_model
        )
        self.inputs["Hyperparameters"].set_processor_function(
            self.inner_widget.set_hyperparameters
        )

        self.outputs["Trained Model"].set_generator_function(
            self.inner_widget.get_trained_model
        )

    def __reduce__(self):
        return (TrainingConsoleNode, (self.inner_widget,), super().__getstate__())


TrainingConsoleNodeFactory = providers.Factory(
    TrainingConsoleNode, training_console_widget=TrainingConsoleWidgetFactory
)