from typing import Optional
from pydantic import BaseModel
from hashlib import sha256
from src.blockchain import Blockchain
from src.cryptography import sign_message, verify_signature
import base64


class Node(BaseModel):
    id: str
    address: str


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
    outputs: Optional[list[UTXO]]
    hash: Optional[str]
    signature: str

    @staticmethod
    def new(tx_id, sender, receiver, amount, signature) -> "Transaction":
        inputs = []
        outputs = []

        total_input_utxos = 0
        for input in inputs:
            total_input_utxos += input.amount

        if total_input_utxos < amount:
            raise TransactionException("Not enough funds")

        return Transaction(
            tx_id=tx_id,
            sender=sender,
            receiver=receiver,
            amount=amount,
            inputs=inputs,
            outputs=None,
            hash=None,
            signature=signature,
        )

    def generate_outputs(self):
        is_signature_valid = verify_signature(
            self.sender, self.tx_to_sign(), self.signature
        )

        if not is_signature_valid:
            raise TransactionException("Invalid signature")

        total_input_utxos = self.total_input_utxos(self.inputs)

        new_output_utxo = UTXO(
            utxo_id=f"0@{self.tx_id}",
            tx_id=self.tx_id,
            owner=self.receiver,
            amount=self.amount,
            spent=False,
        )
        change_utxo = UTXO(
            utxo_id=f"1@{self.tx_id}",
            tx_id=self.tx_id,
            owner=self.sender,
            amount=total_input_utxos - self.amount,
            spent=False,
        )

        self.outputs = [new_output_utxo, change_utxo]

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

    def total_input_utxos(self, inputs: list[UTXO]):
        total = 0
        for input in inputs:
            total += input.amount

        return total


def filter_utxos(address, spent=False) -> list["UTXO"]:
    return [
        UTXO(
            utxo_id="utxo0",
            tx_id="tx0",
            owner="0x27ZXaqHrynvRZ/fdYKMRwN2nyPwxcZn8QGVzVrHeLkQ=",
            amount=100,
            spent=False,
        )
    ]


class TransactionException(Exception):
    pass
