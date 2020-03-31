# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.datasets import Dataset
from dial_core.node_editor import Node
from dial_core.utils import Dial
from tensorflow.keras import Model
from tensorflow.keras.models import Sequential

from .model_compiler_widget import ModelCompilerWidgetFactory

if TYPE_CHECKING:
    from .model_compiler_widget import ModelCompilerWidget


class ModelCompilerNode(Node):
    def __init__(self, model_compiler_widget: "ModelCompilerWidget"):
        super().__init__(
            title="Model Compiler Node", inner_widget=model_compiler_widget,
        )

        # Ports
        self.add_input_port("dataset", port_type=Dataset)
        self.add_input_port("layers", port_type=Dial.KerasLayerListMIME)
        self.inputs["dataset"].set_processor_function(self.__layers_modified)
        self.inputs["layers"].set_processor_function(self.__layers_modified)

        self.add_output_port("model", port_type=Model)
        self.outputs["model"].set_generator_function(self.get_model)

        self.model = Sequential()

    def get_model(self):
        return self.model

    def __layers_modified(self, _):
        print("Layers modified. Compiling model")
        layers = self.inputs["layers"].receive()
        input_shape = self.inputs["dataset"].receive().input_shape

        self.inner_widget.compile_model(input_shape, layers)

        self.outputs["model"].send()

    def __reduce__(self):
        return (ModelCompilerNode, (self.inner_widget,), super().__getstate__())


ModelCompilerNodeFactory = providers.Factory(
    ModelCompilerNode, model_compiler_widget=ModelCompilerWidgetFactory
)
