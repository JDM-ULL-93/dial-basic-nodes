from dial_core.node_editor import Node

from .model_loader_widget import(
    ModelLoaderWidget,
    ModelLoaderWidgetFactory
)

import dependency_injector.providers as providers
from tensorflow.keras import Model
from typing import TYPE_CHECKING,Callable

class ModelLoaderNode(Node):
    def __init__(
        self, model_loader_widget: ModelLoaderWidget,
    ):
        super().__init__(
            title="Model Loader", inner_widget=model_loader_widget,
        )

        self.add_output_port(name="Model", port_type=Model)
        self.outputs["Model"].set_generator_function(
            self.inner_widget.send_model
        )
        return

    #def __reduce__(self): #Esto es para uso interno de pickle, para serializar objetos sin necesidad de instanciarlos
        #return (HyperparametersConfigNode, (self.inner_widget,), super().__getstate__())


ModelLoaderNodeFactory = providers.Factory(
    ModelLoaderNode,
    model_loader_widget=ModelLoaderWidgetFactory,
)
