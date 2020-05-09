# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import List

import dependency_injector.providers as providers
from dial_core.datasets import TTVSets
from dial_core.datasets.datatype import DataTypeContainer
from dial_core.datasets.io import TTVSetsFormatsContainer
from dial_core.utils import log
from PySide2.QtCore import QSize, Signal
from PySide2.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from .formats_widgets import (
    CategoricalImagesFormatWidgetFactory,
    NpzFormatWidgetFactory,
)
from .ttv_sets_list import PredefinedTTVSetsListDialogFactory, TTVSetsListDialog

LOGGER = log.get_logger(__name__)


class CategoricalList(QListWidget):
    def __init__(self, categorical_datatype, parent: "QWidget" = None):
        super().__init__(parent)

        self._categorical_datatype = categorical_datatype

        for category in self._categorical_datatype.categories:
            self.addItem(category)

        print("Categorical")


class DatatypeSelector(QGroupBox):
    def __init__(self, title: str, parent: "QWidget" = None):
        super().__init__(title, parent)

        self.datatype_widget_mapper = {DataTypeContainer.Categorical: CategoricalList}

        self._datatype_stacked_widget = QStackedWidget()

        self._datatype_combobox = QComboBox()
        for (i, (name, datatype_factory)) in enumerate(
            DataTypeContainer.providers.items()
        ):
            datatype = datatype_factory()
            self._datatype_combobox.addItem(name, datatype)
            try:
                self._datatype_stacked_widget.insertWidget(
                    i, self.datatype_widget_mapper[datatype_factory](datatype)
                )
            except KeyError as err:
                print(err)

        self._main_layout = QVBoxLayout()
        self._main_layout.addWidget(self._datatype_combobox)
        self._main_layout.addWidget(self._datatype_stacked_widget)

        self.setLayout(self._main_layout)

        self._datatype_combobox.currentIndexChanged[int].connect(
            self.change_active_widget
        )

    def change_active_widget(self, index):
        self._datatype_stacked_widget.setCurrentIndex(index)

        if self._datatype_stacked_widget.currentIndex() != index:
            self._datatype_stacked_widget.setVisible(False)
        else:
            self._datatype_stacked_widget.setVisible(True)


class TTVSetsImporterWidget(QWidget):
    ttv_loaded = Signal(TTVSets)

    def __init__(
        self, ttv_sets_dialog: "TTVSetsListDialog", parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self.format_widget_mapper = {
            TTVSetsFormatsContainer.NpzFormat: NpzFormatWidgetFactory,
            TTVSetsFormatsContainer.CategoryImagesFormat: CategoricalImagesFormatWidgetFactory,
        }

        self._formats_stacked_widget = QStackedWidget()

        self._formatter_selector = QComboBox()
        for factory in self.format_widget_mapper.keys():
            self._formatter_selector.addItem(factory.cls.__name__, factory)
            self._formats_stacked_widget.addWidget(self.format_widget_mapper[factory]())

        def horizontal_line():
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setFixedHeight(2)
            line.setContentsMargins(0, 30, 0, 0)
            return line

        self._x_datatype_selector = DatatypeSelector(title="X (Input) Datatype")
        self._y_datatype_selector = DatatypeSelector(title="Y (Output) Datatype")
        datatypes_layout = QHBoxLayout()
        datatypes_layout.addWidget(self._x_datatype_selector)
        datatypes_layout.addWidget(self._y_datatype_selector)

        self._main_layout = QVBoxLayout()
        self._main_layout.addWidget(self._formatter_selector)
        self._main_layout.addWidget(horizontal_line())
        self._main_layout.addWidget(self._formats_stacked_widget)
        self._main_layout.addWidget(horizontal_line())
        self._main_layout.addLayout(datatypes_layout)

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
