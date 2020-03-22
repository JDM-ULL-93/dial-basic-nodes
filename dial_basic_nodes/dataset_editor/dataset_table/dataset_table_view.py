# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from dial_core.utils import log
from PySide2.QtGui import QContextMenuEvent
from PySide2.QtWidgets import QAbstractItemView, QHeaderView, QMenu, QTableView

from .dataset_item_delegate import DatasetItemDelegate

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget

LOGGER = log.get_logger(__name__)


class DatasetTableView(QTableView):
    """
    View for the Dataset Table model. Leverages all painting to the DatasetImteDelegate
    class.
    """

    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)

        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.setItemDelegate(DatasetItemDelegate())

    def contextMenuEvent(self, event: "QContextMenuEvent"):
        """Show a context menu for modifying dataset entries."""
        menu = QMenu(parent=self)

        menu.popup(event.globalPos())
        menu.addAction("Remove entries", lambda: self.deleteSelectedRows())

    def deleteSelectedRows(self):
        # When a row is deleted, the new row index is the last row index - 1
        # That's why we have an i variable on this loop, which represents the amount of
        # rows that have been deleted
        chunks = []

        chunk_start = -1
        chunk_end = -1
        for index in self.selectedIndexes():
            if chunk_start == -1:
                chunk_start = index.row()
                chunk_end = chunk_start
                continue

            if (
                index.row() == chunk_end
                or index.row() - 1 == chunk_end
                or index.row() + 1 == chunk_end
            ):
                chunk_end = index.row()
                continue

            chunks.append([min(chunk_start, chunk_end), max(chunk_start, chunk_end)])
            chunk_start = index.row()
            chunk_end = chunk_start

        chunks.append([chunk_start, chunk_end])

        LOGGER.debug("Chunks to remove: %s", chunks)

        for chunks in chunks:
            self.model().removeRows(row=chunks[0], count=(chunks[1] - chunks[0] + 1))

        self.clearSelection()
