from .types import Block, Transaction, Node
from hashlib import sha256


# Blockchain Implementation
class Blockchain:
    def __init__(self):
        self.chain: list[Block] = []
        self.current_transactions: list[Transaction] = []
        self.nodes: list[Node] = []
        self.create_block(proof=100, previous_hash="1")  # Genesis block

