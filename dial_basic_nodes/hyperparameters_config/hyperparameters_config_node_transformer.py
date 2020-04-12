# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import json

import nbformat as nbf
from dial_core.notebook import NodeTransformer


class HyperparametersConfigNodeTransformer(NodeTransformer):
    def _body_cells(self):
        value_cell = nbf.v4.new_code_cell(
            (
                f"{self.node.outputs['Hyperparameters'].word_id()} = "
                f"{json.dumps(self.node.get_hyperparameters(), indent=2)}"
            )
        )

        return [value_cell]
