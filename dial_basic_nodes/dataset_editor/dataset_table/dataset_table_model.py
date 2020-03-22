# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import IntEnum
from typing import TYPE_CHECKING, Any, List, Optional

from dial_core.datasets import Dataset
from dial_core.datasets.datatype import DataType
from dial_core.utils import log
from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide2.QtGui import QPixmapCache
from PySide2.QtWidgets import QMessageBox, QWidget

if TYPE_CHECKING:
    from PySide2.QtWidgets import QObject


LOGGER = log.get_logger(__name__)


class DatasetTableModel(QAbstractTableModel):
    """
    The DatasetTableModel class provides a model for displaying the content of a
    Dataset object.

    Attributes:
        dataset: The dataset associated to this model.
        max_row_count: Maximum number of rows of data to fetch from the dataset on each
            fetch operation (Default: 100).
    """

    TypeRole = Qt.UserRole + 1

    class ColumnLabel(IntEnum):
        Input = 0
        Output = 1

    def __init__(self, parent: "QObject" = None):
        super().__init__(parent)

        self.__cached_data: List[List[Any]] = [[], []]
        self.__types: List[Optional[DataType]] = [None, None]

        self.__dataset: Optional["Dataset"] = None

        self.max_row_count = 100

        self.__role_map = {
            Qt.DisplayRole: self.__display_role,
            self.TypeRole: self.__type_role,
        }

    @property
    def dataset(self) -> "Dataset":
        return self.__dataset

    def load_dataset(self, dataset: "Dataset"):
        """
        Load new Dataset data to the model.
        """

        LOGGER.debug("Loading new dataset to DatasetTableModel...")

        self.__dataset = dataset

        self.__cached_data = [[], []]

        if self.__dataset:
            self.__types = [dataset.x_type, dataset.y_type]

        QPixmapCache.clear()

        # Model has been reset, redraw view
        self.modelReset.emit()

    def rowCount(self, parent=QModelIndex()) -> int:
        """
        Return the number of rows.
        """
        row_count = len(self.__cached_data[self.ColumnLabel.Input])
        return row_count

    def columnCount(self, parent=QModelIndex()) -> int:
        """
        Return the number of columns.
        """
        return len(self.ColumnLabel)

    def headerData(
        self, section: int, orientation: "Qt.Orientation", role=Qt.DisplayRole
    ):
        """
        Return the name of the headers.
        """
        if role != Qt.DisplayRole:
            return None

        # Column header must have their respective names
        if orientation == Qt.Horizontal:
            return self.ColumnLabel(section).name

        # Row header will have the row number as name
        if orientation == Qt.Vertical:
            return str(section)

        return None

    def canFetchMore(self, parent: "QModelIndex") -> bool:
        if parent.isValid():
            return False

        if not self.__dataset:
            return False

        return self.rowCount() < self.__dataset.row_count()

    def fetchMore(self, parent: "QModelIndex"):
        if parent.isValid() or not self.__dataset:
            return False

        remainder = self.__dataset.row_count() - self.rowCount()
        items_to_fetch = min(remainder, self.max_row_count)

        if items_to_fetch <= 0:
            return

        self.insertRows(self.rowCount(), items_to_fetch, parent)

    def index(self, row: int, column: int, parent=QModelIndex()):
        if row < 0 or row > self.rowCount():
            return QModelIndex()

        try:
            return self.createIndex(row, column, self.__cached_data[column][row])

        except IndexError:
            return QModelIndex()

    def data(self, index: "QModelIndex", role=Qt.DisplayRole):
        """
        Return the corresponding data depending on the specified role.
        """
        if not index.isValid():
            return None

        try:
            return self.__role_map[role](index.row(), index.column())

        except KeyError:
            return None

    def setData(
        self, index: "QModelIndex", value: Any, role: int = Qt.EditRole
    ) -> bool:
        if not index.isValid():
            return False

        # TODO: Modify Dataset too
        if role == Qt.EditRole:
            try:
                self.__cached_data[index.column()][index.row()] = self.__types[
                    index.column()
                ].display(
                    self.__types[index.column()].convert_to_expected_format(value)
                )

                self.dataChanged.emit(index, index, (Qt.EditRole))
                return True

            except ValueError:
                LOGGER.exception("Tried to store an invalid value")

        return False

    def flags(self, index: "QModelIndex") -> int:
        general_flags = super().flags(index)

        try:
            if self.__types[index.column()].is_editable:
                return general_flags | Qt.ItemIsEditable
        except IndexError:
            pass

        return general_flags

    def insertRows(self, row: int, count: int, parent=QModelIndex()) -> bool:
        if not self.__dataset:
            return False

        self.beginInsertRows(QModelIndex(), row, row + count - 1)

        x_set, y_set = self.__dataset.items(
            start=row, end=row + count, role=Dataset.Role.Display
        )

        self.__cached_data[self.ColumnLabel.Input][row:row] = x_set
        self.__cached_data[self.ColumnLabel.Output][row:row] = y_set

        self.endInsertRows()

        return True

    def removeRows(self, row: int, count: int, index=QModelIndex()) -> bool:
        """
        Remove rows from the dataset. Rows being deleted must be consecutive.
        """
        if row < 0:
            return False

        LOGGER.debug("Remove rows BEGIN: row %s, %s items", row, count)
        LOGGER.debug("Previous model size: %s", self.rowCount())

        self.beginRemoveRows(QModelIndex(), row, row + count - 1)

        del self.__cached_data[self.ColumnLabel.Input][row : row + count]
        del self.__cached_data[self.ColumnLabel.Output][row : row + count]
        self.__dataset.delete_rows(row, count)  # type: ignore

        self.endRemoveRows()
        LOGGER.debug("Remove rows END")
        LOGGER.debug("New model size: %s", self.rowCount())

        return True

    def __display_role(self, row: int, column: int):
        """
        Return the text representation of the cell value.
        """
        try:
            return self.__cached_data[column][row]

        except IndexError:
            return None

    def __type_role(self, row: int, column: int):
        try:
            return self.__types[column]

        except IndexError:
            return None
