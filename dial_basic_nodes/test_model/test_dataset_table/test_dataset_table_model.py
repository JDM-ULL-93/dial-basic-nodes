# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Any, List, Optional

from dial_core.datasets import Dataset
from PySide2.QtCore import QAbstractTableModel, QObject


class TestDatasetTableModel(QAbstractTableModel):
    def __init__(self, parent: "QObject" = None):
        super().__init__(parent)

        self.__cached_data: List[List[Any]] = [[], [], []]

        self.__test_dataset: Optional["Dataset"] = None

    @property
    def dataset(self) -> "Dataset":
        return self.__test_dataset

    # def load_test_dataset(self, dataset: "Dataset"):
    #     LOGGER.debug("Loading new dataset to the TestDatasetTableModel")
