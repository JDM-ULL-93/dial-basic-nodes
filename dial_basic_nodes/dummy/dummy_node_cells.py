import nbformat as nbf
from dial_core.notebook import NodeCells


class DummyNodeCells(NodeCells):
    """The DataAugmentationNodeCells class generates a block of code corresponding
    to the hyperparameters dictionary."""

    def _body_cells(self):
        return [nbf.v4.new_code_cell("# TODO: Implement later")]
