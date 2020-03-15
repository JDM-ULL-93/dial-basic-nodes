from dial_core.node_editor import Node

class TestNode(Node):
    def __init__(self):
        super().__init__(title="Test Node", inner_widget=None)

        self.add_input_port("test_in", port_type=int)
        self.add_output_port("test_out", port_type=int)

        self.outputs["test_out"] = self.print_out

    def print_out(self) -> int:
        print("Out port was called!!!!")

        return 1

    def __reduce__(self):
        return (self.__class__, ())
