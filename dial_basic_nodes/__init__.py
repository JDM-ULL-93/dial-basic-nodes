# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""This package has the basic nodes that can be placed on the Node Editor.

From editing datasets to compiling models, this nodes should satisfy most of the needs
when working with classical Deep Learning problems.
"""

from dial_core.node_editor import NodeRegistrySingleton

from .dataset_editor import DatasetEditorNode, DatasetEditorNodeFactory
from .layers_editor import LayersEditorNode, LayersEditorNodeFactory
from .model_compiler import ModelCompilerNode, ModelCompilerNodeFactory
from .training_console import TrainingConsoleNode, TrainingConsoleNodeFactory


def load_plugin():
    node_registry = NodeRegistrySingleton()

    node_registry.register_node("Dataset Editor", DatasetEditorNodeFactory)
    node_registry.register_node("Layers Editor", LayersEditorNodeFactory)
    node_registry.register_node("Parameters Compiler", ModelCompilerNodeFactory)
    node_registry.register_node("Training Console", TrainingConsoleNodeFactory)


def unload_plugin():
    node_registry = NodeRegistrySingleton()

    node_registry.unregister_node("Dataset Editor")
    node_registry.unregister_node("Layers Editor")
    node_registry.unregister_node("Parameters Compiler")
    node_registry.unregister_node("Training Console")


__all__ = [
    "load_plugin",
    "unload_plugin",
    "DatasetEditorNode",
    "DatasetEditorNodeFactory",
    "LayersEditorNode",
    "LayersEditorNodeFactory",
    "ModelCompilerNode",
    "ModelCompilerNodeFactory",
    "TrainingConsoleNode",
    "TrainingConsoleNodeFactory",
]
