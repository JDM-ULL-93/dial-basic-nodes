
import os
from typing import List


import dependency_injector.providers as providers
from dial_core.utils import log

LOGGER = log.get_logger(__name__)

from PySide2.QtUiTools import loadUiType
from PySide2.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "./Dummy.ui"))

class DummyWidget(Form, Base):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setupUi(self)

        self.myButton.clicked.connect(self.onClickMyButton)
        return

    def onClickMyButton(self,event):
        LOGGER.debug("Me has pulsado!!")
        return

DummyWidgetFactory = providers.Factory(DummyWidget)
