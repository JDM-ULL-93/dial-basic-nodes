# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""This package has the basic nodes that can be placed on the Node Editor.

From editing datasets to compiling models, this nodes should satisfy most of the needs
when working with classical Deep Learning problems.
"""

from dial_core.node_editor import NodeRegistrySingleton
from dial_core.notebook import NodeCellsRegistrySingleton

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
from .test_model import TestModelNode, TestModelNodeCells, TestModelNodeFactory
from .training_console import (
    TrainingConsoleNode,
    TrainingConsoleNodeCells,
    TrainingConsoleNodeFactory,
)
from .ttv_editor import (
    TTVSetsEditorNode,
    TTVSetsEditorNodeCells,
    TTVSetsEditorNodeFactory,
)
from .ttv_importer import (
    TTVSetsImporterNode,
    TTVSetsImporterNodeCells,
    TTVSetsImporterNodeFactory,
)

from .ttv_exporter import (
    TTVSetsExporterNode,
    TTVSetsExporterNodeCells,
    TTVSetsExporterNodeFactory,
)
from .ttv_merger import (
    TTVSetsMergerNode,
    TTVSetsMergerNodeCells,
    TTVSetsMergerNodeFactory,
)
from .ttv_splitter import (
    TTVSetsSplitterNode,
    TTVSetsSplitterNodeCells,
    TTVSetsSplitterNodeFactory,
)


def load_plugin():
    node_registry = NodeRegistrySingleton()

    # Register Node
    node_registry.register_node("Datasets/TTV Editor", TTVSetsEditorNodeFactory)
    node_registry.register_node("Datasets/TTV Importer", TTVSetsImporterNodeFactory)
    node_registry.register_node("Datasets/TTV Exporter", TTVSetsExporterNodeFactory)
    node_registry.register_node("Datasets/TTV Splitter", TTVSetsSplitterNodeFactory)
    node_registry.register_node("Datasets/TTV Merger", TTVSetsMergerNodeFactory)
    node_registry.register_node("Models/Layers Editor", LayersEditorNodeFactory)
    node_registry.register_node(
        "Training/Hyperparameters Config", HyperparametersConfigNodeFactory
    )
    node_registry.register_node("Training/Training Console", TrainingConsoleNodeFactory)
    node_registry.register_node("Training/Test Model", TestModelNodeFactory)

    # Register Notebook Transformers
    node_cells_registry = NodeCellsRegistrySingleton()
    node_cells_registry.register_transformer(TTVSetsEditorNode, TTVSetsEditorNodeCells)
    node_cells_registry.register_transformer(
        TTVSetsImporterNode, TTVSetsImporterNodeCells
    )
    node_cells_registry.register_transformer(
        TTVSetsExporterNode, TTVSetsExporterNodeCells
    )
    node_cells_registry.register_transformer(
        TTVSetsSplitterNode, TTVSetsSplitterNodeCells
    )
    node_cells_registry.register_transformer(TTVSetsMergerNode, TTVSetsMergerNodeCells)
    node_cells_registry.register_transformer(
        HyperparametersConfigNode, HyperparametersConfigNodeCells
    )
    node_cells_registry.register_transformer(TestModelNode, TestModelNodeCells)
    node_cells_registry.register_transformer(LayersEditorNode, LayersEditorNodeCells)
    node_cells_registry.register_transformer(
        TrainingConsoleNode, TrainingConsoleNodeCells
    )


def unload_plugin():
    node_registry = NodeRegistrySingleton()

    # Unregister Nodes
    node_registry.unregister_node("Datasets/TTV Editor")
    node_registry.unregister_node("Datasets/TTV Importer")
    node_registry.unregister_node("Datasets/TTV Exporter")
    node_registry.unregister_node("Datasets/TTV Splitter")
    node_registry.unregister_node("Datasets/TTV Merger")
    node_registry.unregister_node("Models/Layers Editor")
    node_registry.unregister_node("Training/Hyperparameters Config")
    node_registry.unregister_node("Training/Training Console")
    node_registry.unregister_node("Training/Test Model")

    # Unregister Notebook Transformers
    node_cells_registry = NodeCellsRegistrySingleton()
    node_cells_registry.unregister_transformer(TTVSetsEditorNode)
    node_cells_registry.unregister_transformer(TTVSetsImporterNodeCells)
    node_cells_registry.unregister_transformer(TTVSetsExporterNodeCells)
    node_cells_registry.unregister_transformer(TTVSetsSplitterNodeCells)
    node_cells_registry.unregister_transformer(TTVSetsMergerNodeCells)
    node_cells_registry.unregister_transformer(HyperparametersConfigNode)
    node_cells_registry.unregister_transformer(LayersEditorNode)
    node_cells_registry.unregister_transformer(TrainingConsoleNode)
    node_cells_registry.unregister_transformer(TestModelNode)


__all__ = [
    "load_plugin",
    "unload_plugin",
    "TTVSetsEditorNode",
    "TTVSetsEditorNodeFactory",
    "TTVSetsImporterNode",
    "TTVSetsImporterNodeFactory",
    "TTVSetsExporterNode",
    "TTVSetsExporterNodeFactory",
    "TTVSetsSplitterNode",
    "TTVSetsSplitterNodeFactory",
    "TTVSetsMergerNode",
    "TTVSetsMergerNodeFactory",
    "LayersEditorNode",
    "LayersEditorNodeFactory",
    "TrainingConsoleNode",
    "TrainingConsoleNodeFactory",
    "HyperparametersConfigNode",
    "HyperparametersConfigNodeFactory",
    "TestModelNode",
    "TestModelNodeFactory",
]
