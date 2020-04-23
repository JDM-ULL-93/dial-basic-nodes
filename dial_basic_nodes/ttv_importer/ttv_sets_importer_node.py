# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import os
from typing import TYPE_CHECKING

import dependency_injector.providers as providers

from dial_core.datasets import TTVSets
from dial_core.datasets.io import TTVSetsFormatsContainer, TTVSetsIO
from dial_core.node_editor import Node
from dial_core.utils import find_parent_of, log
from dial_gui.project import ProjectGUI

from .ttv_sets_importer_widget import TTVSetsImporterWidgetFactory

if TYPE_CHECKING:
    from .ttv_sets_importer_widget import TTVSetsImporterWidget

LOGGER = log.get_logger(__name__)


class TTVSetsImporterNode(Node):
    """The TTVSetsImporterNode class provides several methods for loading datasets (from
    the file system or predefined datasets)"""

    def __init__(self, ttv_importer_widget: "TTVSetsImporterWidget", parent=None):
        super().__init__(
            title="TTV Importer Node", inner_widget=ttv_importer_widget, parent=parent
        )

        self.add_output_port(name="TTV Sets", port_type=TTVSets)
        self.outputs["TTV Sets"].set_generator_function(self.inner_widget.get_ttv)

        self.inner_widget.ttv_loaded.connect(self._save_ttv_on_cache)
        self.inner_widget.ttv_loaded.connect(lambda: self.outputs["TTV Sets"].send())

    def _save_ttv_on_cache(self, ttv: "TTVSets"):
        """Saves the loaded ttv object on the cache directory (Project directory)"""
        project = find_parent_of(self, ProjectGUI)
        project_dir = project.directory() if project else None

        if not project_dir:
            LOGGER.debug(f"Can't save, empty directory: {project_dir}")
            return

        TTVSetsIO.save(
            TTVSetsFormatsContainer.NpzFormat(), project_dir, ttv,
        )

        LOGGER.debug(f"TTV Saved on cached directory {project_dir}")

    def __getstate__(self):
        state = super().__getstate__()

        ttv = self.inner_widget.get_ttv()
        ttv_name = ttv.name if ttv else None

        state["ttv_name"] = ttv_name

        return state

    def __setstate__(self, new_state):
        super().__setstate__(new_state)

        if new_state["ttv_name"]:
            project = find_parent_of(self, ProjectGUI)
            project_dir = project.directory() if project else None

            print("Project: ", project)
            print("Parent //////", self.parent)

            if not project:
                print("NOTTT PROJECT")
                return

            self.inner_widget.load_ttv_from_dir(
                project_dir + os.path.sep + new_state["ttv_name"]
            )
            print("Loaded?")

    def __reduce__(self):
        return (TTVSetsImporterNode, (self.inner_widget,), self.__getstate__())


TTVSetsImporterNodeFactory = providers.Factory(
    TTVSetsImporterNode, ttv_importer_widget=TTVSetsImporterWidgetFactory
)
