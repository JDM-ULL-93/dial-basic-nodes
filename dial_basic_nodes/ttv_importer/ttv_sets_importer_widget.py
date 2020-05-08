# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers
from dial_core.datasets import TTVSets
from dial_core.datasets.io import TTVSetsFormatsContainer
from dial_core.utils import log
from PySide2.QtCore import QSize, Signal
from PySide2.QtWidgets import (
    QComboBox,
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
    QStackedWidget,
)

from .formats_widgets import (
    CategoricalImagesFormatWidgetFactory,
    NpzFormatWidgetFactory,
)
from .ttv_sets_list import PredefinedTTVSetsListDialogFactory, TTVSetsListDialog

LOGGER = log.get_logger(__name__)


class TTVSetsImporterWidget(QWidget):
    ttv_loaded = Signal(TTVSets)

    def __init__(
        self, ttv_sets_dialog: "TTVSetsListDialog", parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self.format_gui_mapper = {
            TTVSetsFormatsContainer.NpzFormat: NpzFormatWidgetFactory,
            TTVSetsFormatsContainer.CategoryImagesFormat: CategoricalImagesFormatWidgetFactory,
        }

        self._formats_stacked_widget = QStackedWidget()

        self._formatter_selector = QComboBox()
        for factory in self.format_gui_mapper.keys():
            self._formatter_selector.addItem(factory.cls.__name__, factory)
            self._formats_stacked_widget.addWidget(self.format_gui_mapper[factory]())

        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)
        horizontal_line.setFixedHeight(2)
        horizontal_line.setContentsMargins(0, 30, 0, 0)

        self._main_layout = QVBoxLayout()
        self._main_layout.addWidget(self._formatter_selector)
        self._main_layout.addWidget(horizontal_line)
        self._main_layout.addWidget(self._formats_stacked_widget)

        self.setLayout(self._main_layout)

        self._formatter_selector.currentIndexChanged[int].connect(
            lambda i: self._formats_stacked_widget.setCurrentIndex(i)
        )

    def get_ttv(self) -> "TTVSets":
        return None

    def sizeHint(self) -> "QSize":
        """Optimal size of the widget."""
        return QSize(450, 150)

    def __reduce__(self):
        return (
            TTVSetsImporterWidget,
            (self._ttv_sets_dialog, None),
        )


TTVSetsImporterWidgetFactory = providers.Factory(
    TTVSetsImporterWidget, ttv_sets_dialog=PredefinedTTVSetsListDialogFactory,
)
