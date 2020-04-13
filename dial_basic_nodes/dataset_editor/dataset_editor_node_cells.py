# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import nbformat as nbf
from dial_core.notebook import NodeCells


class DatasetEditorNodeCells(NodeCells):
    def _body_cells(self):
        value_cell = nbf.v4.new_code_cell(
            (
                f'{self.node.outputs["Train Dataset"].word_id()}\n'
                f'{self.node.outputs["Test Dataset"].word_id()}'
            )
        )

        return [value_cell]
