from typing import TYPE_CHECKING, List

import dependency_injector.providers as providers
from dial_core.node_editor import Node

from .dummy_widget import DummyWidgetFactory
from .dummy_widget import DummyWidget

class DummyNode(Node):
    def __init__(
        self, dummy_widget: DummyWidget,
    ):
        super().__init__(
            title="Dummy", inner_widget=dummy_widget,
        )

        self.add_output_port("Prueba_Output1", port_type=str)
        self.outputs["Prueba_Output1"].set_generator_function(self.getPruebaOutput)

    def getPruebaOutput(self):
        #return self.inner_widget.get_hyperparameters()
        return "Hola Mundo"

    #def __reduce__(self): #Esto es para uso interno de pickle, para serializar objetos sin necesidad de instanciarlos
        #return (HyperparametersConfigNode, (self.inner_widget,), super().__getstate__())


DummyNodeFactory = providers.Factory(
    DummyNode,
    dummy_widget=DummyWidgetFactory,
)

