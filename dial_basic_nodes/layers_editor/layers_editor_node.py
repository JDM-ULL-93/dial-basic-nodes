# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from dial_core.node_editor import Node, OutputPort
from dial_core.utils import Dial

if TYPE_CHECKING:
    from .layers_editor_widget import LayersEditorWidget


class LayersEditorNode(Node):
    def __init__(self, layers_editor_widget: "LayersEditorWidget"):
        super().__init__(title="Layers Editor Node", inner_widget=layers_editor_widget)

        self.add_output_port(OutputPort("layers", port_type=dial_core.KerasLayerListMIME))
        self.outputs["layers"].output_generator = self.get_model_layers

    def get_model_layers(self):  # TODO: Implement
        raise NotImplementedError("get_model_layers not implemented!")
