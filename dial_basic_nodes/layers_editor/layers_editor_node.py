# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, List
from copy import deepcopy

import dependency_injector.providers as providers
from dial_core.node_editor import Node
from dial_core.utils import Dial
from PySide2.QtCore import QObject, Signal

from .layers_editor_widget import LayersEditorWidgetFactory

if TYPE_CHECKING:
    from .layers_editor_widget import LayersEditorWidget


class LayersEditorNode(Node, QObject):
    layers_modified = Signal(object)

    def __init__(
        self, layers_editor_widget: "LayersEditorWidget", parent: "QObject" = None
    ):
        QObject.__init__(self, parent)
        Node.__init__(
            self, title="Layers Editor Node", inner_widget=layers_editor_widget
        )

        self.add_output_port(name="layers", port_type=Dial.KerasLayerListMIME)
        self.outputs["layers"].set_generator_function(self.get_layers)

        def triggered():
            print("Layers changed", self.get_layers())

            self.outputs["layers"].send()

        self.inner_widget.layers_modified.connect(triggered)

    def get_layers(self):
        return deepcopy(self.inner_widget.layers)

    def __reduce__(self):
        return (LayersEditorNode, (self.inner_widget,), super().__getstate__())


LayersEditorNodeFactory = providers.Factory(
    LayersEditorNode, layers_editor_widget=LayersEditorWidgetFactory
)
