# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.datasets import Dataset
from dial_core.node_editor import Node

from .dataset_editor_widget import DatasetEditorWidgetFactory

if TYPE_CHECKING:
    from .dataset_editor_widget import DatasetEditorWidget


class DatasetEditorNode(Node):
    def __init__(self, dataset_editor_widget: "DatasetEditorWidget"):
        super().__init__(
            title="Dataset Editor Node", inner_widget=dataset_editor_widget
        )

        # Ports
        self.add_output_port(name="train", port_type=Dataset)
        self.add_output_port(name="test", port_type=Dataset)

        self.outputs["train"].output_generator = self.inner_widget.train_dataset
        self.outputs["test"].output_generator = self.inner_widget.test_dataset

    def __reduce__(self):
        return (DatasetEditorNode, (self.inner_widget,), super().__getstate__())


DatasetEditorNodeFactory = providers.Factory(
    DatasetEditorNode, dataset_editor_widget=DatasetEditorWidgetFactory
)
