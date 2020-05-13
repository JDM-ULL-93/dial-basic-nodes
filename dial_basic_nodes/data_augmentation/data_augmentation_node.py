# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers
from dial_core.datasets import TTVSets
from dial_core.node_editor import Node

from .data_augmentation_widget import (
    DataAugmentationWidget,
    DataAugmentationWidgetFactory,
)


class DataAugmentationNode(Node):
    def __init__(self, data_augmentation_widget: "DataAugmentationWidget"):
        super().__init__(
            title="Data Augmentation Node", inner_widget=data_augmentation_widget
        )

        self.add_input_port("TTVSets", port_type=TTVSets)
        self.inputs["TTVSets"].set_processor_function(self.apply_data_augmentation)

        self.add_output_port("Augmented TTVSets", port_type=TTVSets)
        self.outputs["Augmented TTVSets"].set_generator_function(
            self.inner_widget.get_augmented_ttv
        )

        self.inner_widget.operations_updated.connect(
            lambda: self.outputs["Augmented TTVSets"].send()
        )

    def apply_data_augmentation(self, ttv: "TTVSets"):
        self.inner_widget.set_ttv(ttv)

        self.outputs["Augmented TTVSets"].send()

    def __reduce__(self):
        return (DataAugmentationNode, (self.inner_widget,), super().__getstate__())


DataAugmentationNodeFactory = providers.Factory(
    DataAugmentationNode, data_augmentation_widget=DataAugmentationWidgetFactory
)
