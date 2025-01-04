from .types import Block, Transaction, Node
from hashlib import sha256


# Blockchain Implementation
class Blockchain:
    def __init__(self):
        self.chain: list[Block] = []
        self.current_transactions: list[Transaction] = []
        self.remote_nodes: list[Node] = []
        self.local_node: Node = Node(node_id=0, host="localhost", port=5000)

    def create_block():
        pass

    def verify_block(self, block):
        pass

    def mine_block(self):
        pass
