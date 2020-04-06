# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


from typing import TYPE_CHECKING

import dependency_injector.providers as providers
from dial_core.datasets import Dataset
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QTabWidget

from dial_basic_nodes.utils.dataset_table import DatasetTableWidgetFactory

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget


class TrainTestTabs(QTabWidget):
    """
    The TrainTestTabs class is a container for a pair of train/test datasets. Each
    dataset is displayed on its own tab, and can be accessed through the `train_dataset`
    and `test_dataset` methods.
    """

    train_dataset_modified = Signal(Dataset)
    test_dataset_modified = Signal(Dataset)

    def __init__(
        self,
        dataset_table_widget_factory: "providers.Factory",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self._train_table_widget = dataset_table_widget_factory(parent=self)
        self._test_table_widget = dataset_table_widget_factory(parent=self)

        self.addTab(self._train_table_widget, "Train")
        self.addTab(self._test_table_widget, "Test")

        self._dataset_table_widget_factory = dataset_table_widget_factory

        self._train_table_widget.dataset_modified.connect(
            lambda dataset: self.train_dataset_modified.emit(dataset)
        )
        self._train_table_widget.dataset_modified.connect(
            lambda dataset: self.test_dataset_modified.emit(dataset)
        )

    def train_dataset(self) -> "Dataset":
        """Returns the train dataset."""
        return self._train_table_widget.dataset

    def test_dataset(self) -> "Dataset":
        """Returns the test dataset."""
        return self._test_table_widget.dataset

    def load_train_dataset(self, train_dataset: "Dataset"):
        """Sets a new dataset as the train dataset."""
        self._train_table_widget.load_dataset(train_dataset)

    def load_test_dataset(self, test_dataset: "Dataset"):
        """Sets a new dataset as the test dataset."""
        self._test_table_widget.load_dataset(test_dataset)

    def __getstate__(self):
        return {
            "train_dataset": self._train_model.dataset,
            "test_dataset": self._test_model.dataset,
        }

    def __setstate__(self, new_state):
        self.load_train_dataset(new_state["train_dataset"])
        self.load_test_dataset(new_state["test_dataset"])

    def __reduce__(self):
        return (
            TrainTestTabs,
            (self._dataset_table_widget_factory,),
            self.__getstate__(),
        )


TrainTestTabsFactory = providers.Factory(
    TrainTestTabs, dataset_table_widget_factory=DatasetTableWidgetFactory.delegate()
)
