# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


from typing import Optional

import dependency_injector.providers as providers
from PySide2.QtCore import QSize, Signal
from PySide2.QtWidgets import QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget

from dial_core.datasets import TTVSets
from dial_core.datasets.io import TTVSetsFormatsContainer, TTVSetsIO
from dial_core.utils import log

from .ttv_sets_list import PredefinedTTVSetsListDialogFactory, TTVSetsListDialog

LOGGER = log.get_logger(__name__)


class TTVSetsImporterWidget(QWidget):
    ttv_loaded = Signal(TTVSets)

    def __init__(
        self, ttv_sets_dialog: "TTVSetsListDialog", parent: "QWidget" = None,
    ):
        super().__init__(parent)

        # Components
        self._ttv: Optional["TTVSets"] = None

        self._ttv_sets_dialog = ttv_sets_dialog

        # Widgets
        self._directory_picker_button = QPushButton("Load TTV from file...")
        self._directory_picker_button.clicked.connect(self._load_ttv_from_filesys)

        self._predefined_load_button = QPushButton("Load predefined datasets...")
        self._predefined_load_button.clicked.connect(self._load_predefined_datasets)

        self._name_label = QLabel("Name:")
        self._train_label = QLabel("Train:")
        self._test_label = QLabel("Test:")
        self._validation_label = QLabel("Validation:")

        self._main_layout = QVBoxLayout()
        self._main_layout.addWidget(self._directory_picker_button)
        self._main_layout.addWidget(self._predefined_load_button)
        self._main_layout.addWidget(self._name_label)
        self._main_layout.addWidget(self._train_label)
        self._main_layout.addWidget(self._test_label)
        self._main_layout.addWidget(self._validation_label)

        self.setLayout(self._main_layout)

    def get_ttv(self) -> "TTVSets":
        """Returns the loaded TTVSets object."""
        return self._ttv

    def set_ttv(self, ttv: "TTVSets"):
        self._ttv = ttv
        self._update_labels_text()
        self.ttv_loaded.emit(self._ttv)

        LOGGER.info(f"TTVSets loaded! {ttv}")

    def _load_ttv_from_filesys(self):
        LOGGER.debug("Picking a TTV Directory...")
        selected_ttv_dir = QFileDialog.getExistingDirectory(
            parent=self,
            caption="TTV Folder",
            options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )

        if not selected_ttv_dir:
            LOGGER.debug("Loading cancelled...")
            return

        try:
            ttv = TTVSetsIO.load(selected_ttv_dir, TTVSetsFormatsContainer)

            self.set_ttv(ttv)

            # if self._cache_dir:
            #     TTVSetsIO.save(
            #         TTVSetsFormatsContainer.NpzFormat, self._cache_dir, self._ttv,
            #     )
            #     LOGGER.debug("Loaded dir cached. {self}")
            # else:
            #     LOGGER.debug(
            #         "No cache dir specified for {self}. Define a Project directory"
            #     )

        except IOError as err:
            LOGGER.exception("Couldn't load TTV Sets!", err)

    def _load_predefined_datasets(self):
        exit_code = self._ttv_sets_dialog.exec_()

        if exit_code != 1:
            LOGGER.debug("Loading cancelled...")
            return

        ttv = self._ttv_sets_dialog.selected_loader().load()
        self.set_ttv(ttv)

    def _save_on_cache(self, cache_dir):
        if not cache_dir:
            LOGGER.debug(f"Can't save, empty directory: {cache_dir}")
            return

        TTVSetsIO.save(
            TTVSetsFormatsContainer.NpzFormat(), cache_dir, self._ttv,
        )

        LOGGER.debug(f"TTV Saved on cached directory {cache_dir}")

    def _update_labels_text(self):
        self._name_label.setText(f"Name: {self._ttv.name if self._ttv else ''}")
        self._train_label.setText(
            f"Train: {str(self._ttv.train if self._ttv else None)}"
        )
        self._test_label.setText(f"Test: {str(self._ttv.test if self._ttv else None)}")
        self._validation_label.setText(
            f"Validation: {str(self._ttv.validation if self._ttv else None)}"
        )

    def sizeHint(self) -> "QSize":
        """Optimal size of the widget."""
        return QSize(100, 150)

    def __getstate__(self):
        return {"ttv_name": self._ttv.name if self._ttv else ""}

    def __setstate__(self, new_state):
        name = new_state["ttv_name"]

    def __reduce__(self):
        return (
            TTVSetsImporterWidget,
            (self._ttv_sets_dialog, None),
            self.__getstate__(),
        )


TTVSetsImporterWidgetFactory = providers.Factory(
    TTVSetsImporterWidget, ttv_sets_dialog=PredefinedTTVSetsListDialogFactory,
)
