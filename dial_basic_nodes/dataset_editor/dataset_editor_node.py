# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.datasets import Dataset
from dial_core.node_editor import Node
from PySide2.QtCore import QObject

from .dataset_editor_widget import DatasetEditorWidgetFactory

if TYPE_CHECKING:
    from .dataset_editor_widget import DatasetEditorWidget


class DatasetEditorNode(Node, QObject):
    """The DatasetEditorNode class provides a node capable of load, visualize and modify
        Dataset objects through an interface."""

    def __init__(
        self, dataset_editor_widget: "DatasetEditorWidget", parent: "QObject" = None
    ):
        Node.__init__(
            self, title="Dataset Editor Node", inner_widget=dataset_editor_widget
        )
        QObject.__init__(self, parent)

        self.add_output_port(name="train", port_type=Dataset)
        self.add_output_port(name="test", port_type=Dataset)

        self.outputs["train"].set_generator_function(
            self.inner_widget.get_train_dataset
        )
        self.outputs["test"].set_generator_function(self.inner_widget.get_test_dataset)

        self.inner_widget.train_dataset_modified.connect(
            lambda: self.outputs["train"].send()
        )
        self.inner_widget.test_dataset_modified.connect(
            lambda: self.outputs["test"].send()
        )

    def __reduce__(self):
        return (DatasetEditorNode, (self.inner_widget,), super().__getstate__())


DatasetEditorNodeFactory = providers.Factory(
    DatasetEditorNode, dataset_editor_widget=DatasetEditorWidgetFactory
)
