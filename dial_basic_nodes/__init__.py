# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""This package has the basic nodes that can be placed on the Node Editor.

From editing datasets to compiling models, this nodes should satisfy most of the needs
when working with classical Deep Learning problems.
"""

from dial_core.node_editor import NodeRegistrySingleton

from .test_node import TestNode


def initialize_plugin():
    node_registry = NodeRegistrySingleton()

    node_registry.register_node("Test Node", TestNode)


__all__ = ["TestNode", "initialize_plugin"]
