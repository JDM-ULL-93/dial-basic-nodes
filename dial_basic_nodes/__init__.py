# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""This package has the basic nodes that can be placed on the Node Editor.

From editing datasets to compiling models, this nodes should satisfy most of the needs
when working with classical Deep Learning problems.
"""

from dial_core.node_editor import NodeRegistrySingleton

from .dataset_editor import DatasetEditorNodeFactory, DatasetEditorNode
from .layers_editor import LayersEditorNodeFactory, LayersEditorNode
from .model_compiler import ModelCompilerNodeFactory, ModelCompilerNode


def initialize_plugin():
    node_registry = NodeRegistrySingleton()

    node_registry.register_node("Dataset Editor", DatasetEditorNodeFactory)
    node_registry.register_node("Layers Editor", LayersEditorNodeFactory)
    node_registry.register_node("Parameters Compiler", ModelCompilerNodeFactory)


__all__ = [
    "initialize_plugin",
    "DatasetEditorNode",
    "DatasetEditorNodeFactory",
    "LayersEditorNode",
    "LayersEditorNodeFactory",
    "ModelCompilerNode",
    "ModelCompilerNodeFactory",
]
