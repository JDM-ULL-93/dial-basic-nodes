# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers
from dial_core.datasets import TTVSets
from dial_core.datasets.io import DatasetIOContainer
from dial_core.utils import log
from PySide2.QtCore import QSize, Signal
from PySide2.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from .datatype_selector import DatatypeSelectorFactory
from .formats_widgets import CategoricalImagesWidgetFactory, NpzWidgetFactory
from .ttv_sets_list import PredefinedTTVSetsListDialogFactory, TTVSetsListDialog

LOGGER = log.get_logger(__name__)

FORMAT_TO_WIDGET = {
    DatasetIOContainer.NpzDatasetIO: {
        "name": "Npz Files",
        "widget_factory": NpzWidgetFactory,
    },
    DatasetIOContainer.CategoricalImgDatasetIO: {
        "name": "Categorical Images",
        "widget_factory": CategoricalImagesWidgetFactory,
    },
}


class TTVSetsImporterWidget(QWidget):
    ttv_updated = Signal(TTVSets)

    def __init__(
        self,
        ttv_sets_dialog: "TTVSetsListDialog",
        format_to_widget,
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        # Components
        self._ttv = None

        # Maps a  with its respective Widget
        self._format_to_widget = format_to_widget

        self._stacked_widgets = QStackedWidget()

        self._name_textbox = QLineEdit("Unnamed")

        self._formatter_selector = QComboBox()
        for (format_factory, widget_dict) in self._format_to_widget.items():
            self._formatter_selector.addItem(widget_dict["name"], format_factory)
            self._stacked_widgets.addWidget(
                self._format_to_widget[format_factory]["widget_factory"]()
            )

        def horizontal_line():
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setFixedHeight(2)
            line.setContentsMargins(0, 30, 0, 0)
            return line

        self._x_datatype_selector = DatatypeSelectorFactory(title="X (Input) Datatype")
        self._y_datatype_selector = DatatypeSelectorFactory(title="Y (Output) Datatype")

        datatypes_layout = QHBoxLayout()
        datatypes_layout.addWidget(self._x_datatype_selector)
        datatypes_layout.addWidget(self._y_datatype_selector)

        self._main_layout = QVBoxLayout()
        self._main_layout.addWidget(self._name_textbox)
        self._main_layout.addWidget(self._formatter_selector)
        self._main_layout.addWidget(horizontal_line())
        self._main_layout.addWidget(self._stacked_widgets)
        self._main_layout.addWidget(horizontal_line())
        self._main_layout.addLayout(datatypes_layout)

        self._update_ttv_button = QPushButton("Update TTV")
        self._update_ttv_button.clicked.connect(self._update_ttv)
        self._main_layout.addWidget(self._update_ttv_button)

        self.setLayout(self._main_layout)

        self._formatter_selector.currentIndexChanged[int].connect(
            lambda i: self._stacked_widgets.setCurrentIndex(i)
        )

    def get_ttv(self) -> "TTVSets":
        return self._ttv

    def _update_ttv(self):
        self._ttv = self._stacked_widgets.currentWidget().load_ttv(
            self._name_textbox.text(),
            self._x_datatype_selector.selected_datatype,
            self._y_datatype_selector.selected_datatype,
        )

        self.ttv_updated.emit(self._ttv)

    def _selected_index_changed(self, index: int):
        self._stacked_widgets.setCurrentIndex(index)

    def sizeHint(self) -> "QSize":
        """Optimal size of the widget."""
        return QSize(450, 150)

    def __reduce__(self):
        return (
            TTVSetsImporterWidget,
            (self._ttv_sets_dialog, None),
        )


TTVSetsImporterWidgetFactory = providers.Factory(
    TTVSetsImporterWidget,
    ttv_sets_dialog=PredefinedTTVSetsListDialogFactory,
    format_to_widget=FORMAT_TO_WIDGET,
)
