from typing import Optional
from pydantic import BaseModel
from hashlib import sha256
from src.cryptography import sign_message, verify_signature


class Node(BaseModel):
    id: str
    address: str

    @staticmethod
    def discover_nodes() -> list["Node"]:
        return []


class Block(BaseModel):
    index: int
    timestamp: float
    transactions: list["Transaction"]
    nonce: int
    previous_hash: str


class UTXO(BaseModel):
    utxo_id: str
    tx_id: str
    owner: str
    amount: float
    spent: bool


class Transaction(BaseModel):
    tx_id: str
    sender: str
    receiver: str
    amount: float
    inputs: list[UTXO]
    outputs: list[UTXO]
    hash: str
    signature: str

    @staticmethod
    def new(tx_id, sender, receiver, amount, inputs, signature) -> "Transaction":
        """
        Creates a new transaction.
        """
        assert len(inputs) > 0
        assert amount > 0

        tx = Transaction(
            tx_id=tx_id,
            sender=sender,
            receiver=receiver,
            amount=amount,
            inputs=inputs,
            outputs=[],
            hash="",
            signature=signature,
        )

        if tx.is_amount_valid():
            raise TransactionException("Not enough funds")

        if tx.is_signature_valid():
            raise TransactionException("Invalid signature")

        total_input_utxos = tx.total_input_utxos()
        new_output_utxo = UTXO(
            utxo_id=f"0@{tx.tx_id}",
            tx_id=tx.tx_id,
            owner=tx.receiver,
            amount=tx.amount,
            spent=False,
        )
        change_utxo = UTXO(
            utxo_id=f"1@{tx.tx_id}",
            tx_id=tx.tx_id,
            owner=tx.sender,
            amount=total_input_utxos - tx.amount,
            spent=False,
        )
        tx.outputs = [new_output_utxo, change_utxo]
        tx.hash = tx.hash_tx()

        return tx

    def is_valid(self) -> bool:
        return (
            self.is_amount_valid()
            and self.is_hash_valid()
            and self.is_signature_valid()
            and len(self.inputs) > 0
            and self.amount > 0
        )

    def is_amount_valid(self) -> bool:
        total_input_utxos = self.total_input_utxos()
        return total_input_utxos < self.amount

    def is_signature_valid(self) -> bool:
        if self.signature == "":
            return False

        is_signature_valid = verify_signature(
            self.sender, self.tx_to_sign(), self.signature
        )
        return not is_signature_valid

    def is_hash_valid(self) -> bool:
        return self.hash == self.hash_tx()

    def hash_tx(self) -> str:
        return sha256(self.tx_to_hash().encode()).hexdigest()

    def sign_tx(self) -> str:
        return sign_message(self.sender, self.tx_to_sign())

    def verify_signature(self, public_key: str) -> bool:
        return verify_signature(public_key, self.tx_to_sign(), self.signature)

    def tx_to_hash(self):
        return self.model_dump_json(exclude={"hash"})

    def tx_to_sign(self):
        return self.model_dump_json(exclude={"signature", "hash", "output"})

    def total_input_utxos(self):
        total = 0
        for input in self.inputs:
            total += input.amount

        return total


class TransactionException(Exception):
    pass
