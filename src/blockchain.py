from .types import UTXO, Block, Transaction, Node
from hashlib import sha256


# Blockchain Implementation
class Blockchain:
    def __init__(self):
        self.chain: list[Block] = []
        self.current_block = []
        self.mempool : list[Transaction]
        self.local_node: Node = Node(node_id=0, host="localhost", port=5000)
        self.remote_nodes: list[Node] = self.local_node.connect_to_network()

    def create_block(self):
        pass

    def verify_block(self, block):
        pass

    def mine_block(self):
        pass

    def previous_utxos(self, address: str) -> list[UTXO]:
        utxos = []
        for block in self.chain:
            for tx in block.transactions:
                for output in tx.outputs:
                    if output.owner == address:
                        utxos.append(output)
        return utxos
