# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""This package has the basic nodes that can be placed on the Node Editor.

From editing datasets to compiling models, this nodes should satisfy most of the needs
when working with classical Deep Learning problems.
"""

from dial_core.node_editor import NodeRegistrySingleton
from dial_core.notebook import NodeTransformersRegistrySingleton

from .dataset_editor import (
    DatasetEditorNode,
    DatasetEditorNodeFactory,
    DatasetEditorNodeTransformer,
)
from .hyperparameters_config import (
    HyperparametersConfigNode,
    HyperparametersConfigNodeFactory,
    HyperparametersConfigNodeTransformer,
)
from .layers_editor import LayersEditorNode, LayersEditorNodeFactory
from .test_model import TestModelNode, TestModelNodeFactory
from .training_console import TrainingConsoleNode, TrainingConsoleNodeFactory


def load_plugin():
    node_registry = NodeRegistrySingleton()

    node_registry.register_node("Dataset Editor", DatasetEditorNodeFactory)
    node_registry.register_node("Layers Editor", LayersEditorNodeFactory)
    node_registry.register_node(
        "Hyperparameters Config", HyperparametersConfigNodeFactory
    )
    node_registry.register_node("Training Console", TrainingConsoleNodeFactory)
    node_registry.register_node("Test Model", TestModelNodeFactory)

    node_transformers_registry = NodeTransformersRegistrySingleton()
    node_transformers_registry.register_transformer(
        DatasetEditorNode, DatasetEditorNodeTransformer
    )
    node_transformers_registry.register_transformer(
        HyperparametersConfigNode, HyperparametersConfigNodeTransformer
    )


def unload_plugin():
    node_registry = NodeRegistrySingleton()

    node_registry.unregister_node("Dataset Editor")
    node_registry.unregister_node("Layers Editor")
    node_registry.unregister_node("Hyperparameters Config")
    node_registry.unregister_node("Training Console")
    node_registry.unregister_node("Test Model")

    node_transformers_registry = NodeTransformersRegistrySingleton()
    node_transformers_registry.unregister_transformer(DatasetEditorNode)
    node_transformers_registry.unregister_transformer(HyperparametersConfigNode)


__all__ = [
    "load_plugin",
    "unload_plugin",
    "DatasetEditorNode",
    "DatasetEditorNodeFactory",
    "LayersEditorNode",
    "LayersEditorNodeFactory",
    "TrainingConsoleNode",
    "TrainingConsoleNodeFactory",
    "HyperparametersConfigNode",
    "HyperparametersConfigNodeFactory",
    "TestModelNode",
    "TestModelNodeFactory",
]
