# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""This package has the basic nodes that can be placed on the Node Editor.

From editing datasets to compiling models, this nodes should satisfy most of the needs
when working with classical Deep Learning problems.
"""

from dial_core.node_editor import NodeRegistrySingleton
from dial_core.notebook import NodeCellsRegistrySingleton

from .dataset_editor import (
    DatasetEditorNode,
    DatasetEditorNodeCells,
    DatasetEditorNodeFactory,
)
from .hyperparameters_config import (
    HyperparametersConfigNode,
    HyperparametersConfigNodeCells,
    HyperparametersConfigNodeFactory,
)
from .layers_editor import (
    LayersEditorNode,
    LayersEditorNodeCells,
    LayersEditorNodeFactory,
)
from .test_model import TestModelNode, TestModelNodeFactory
from .training_console import (
    TrainingConsoleNode,
    TrainingConsoleNodeCells,
    TrainingConsoleNodeFactory,
)


def load_plugin():
    node_registry = NodeRegistrySingleton()

    node_registry.register_node("Dataset Editor", DatasetEditorNodeFactory)
    node_registry.register_node("Layers Editor", LayersEditorNodeFactory)
    node_registry.register_node(
        "Hyperparameters Config", HyperparametersConfigNodeFactory
    )
    node_registry.register_node("Training Console", TrainingConsoleNodeFactory)
    node_registry.register_node("Test Model", TestModelNodeFactory)

    node_cells_registry = NodeCellsRegistrySingleton()
    node_cells_registry.register_transformer(DatasetEditorNode, DatasetEditorNodeCells)
    node_cells_registry.register_transformer(
        HyperparametersConfigNode, HyperparametersConfigNodeCells
    )
    node_cells_registry.register_transformer(LayersEditorNode, LayersEditorNodeCells)
    node_cells_registry.register_transformer(
        TrainingConsoleNode, TrainingConsoleNodeCells
    )


def unload_plugin():
    node_registry = NodeRegistrySingleton()

    node_registry.unregister_node("Dataset Editor")
    node_registry.unregister_node("Layers Editor")
    node_registry.unregister_node("Hyperparameters Config")
    node_registry.unregister_node("Training Console")
    node_registry.unregister_node("Test Model")

    node_cells_registry = NodeCellsRegistrySingleton()
    node_cells_registry.unregister_transformer(DatasetEditorNode)
    node_cells_registry.unregister_transformer(HyperparametersConfigNode)
    node_cells_registry.unregister_transformer(LayersEditorNode)
    node_cells_registry.unregister_transformer(TrainingConsoleNode)


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
