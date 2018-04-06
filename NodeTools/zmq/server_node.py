from anonymizing_chains.common.zmq.base_node import BaseNode


SERVER_NODE_ID = 0


class ServerNode(BaseNode):
    def __init__(self, iname, port):
        super().__init__(iname, port, SERVER_NODE_ID)

    def process_message(self):
        pass
