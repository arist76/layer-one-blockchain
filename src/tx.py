from typing import Optional
from pydantic import BaseModel
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
import base64


def filter_utxos(address, spent=False) -> list["UTXO"]:
    return [
        # private key = xz8XHacl+NPTmTSXWEXeQKQnYc8yQg4rKEBqv3UG15Y=
        UTXO(
            utxo_id="utxo0",
            tx_id="tx0",
            owner="0x27ZXaqHrynvRZ/fdYKMRwN2nyPwxcZn8QGVzVrHeLkQ=",
            amount=100,
            spent=False,
        )
    ]


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
    inputs: list[UTXO]
    outputs: Optional[list[UTXO]]
    hash: Optional[str]
    signature: str

    def create(self, sender: str, receiver: str, amount: float, signature: str):
        input_utxos = filter_utxos(sender)
        total_input_amount = sum([utxo.amount for utxo in input_utxos])

        # validate signature
        if not self.verify_signature(sender):
            raise TransactionException("Invalid signature")

        # validate amount
        if total_input_amount <= amount:
            raise TransactionException("Not enough funds")

        output_utxos = [
            UTXO(
                utxo_id="utxo1",
                tx_id=self.tx_id,
                owner=receiver,
                amount=amount,
                spent=False,
            ),
            UTXO(
                utxo_id="utxo2",
                tx_id=self.tx_id,
                owner=sender,
                amount=total_input_amount - amount,
                spent=False,
            ),
        ]

        self.inputs = input_utxos
        self.outputs = output_utxos
        self.sender = sender
        self.receiver = receiver

        self.hash = self.hash_tx()
        self.signature = signature

    def verify_signature(self, public_key: str) -> bool:
        public_key_bytes = base64.b64decode(public_key[1:])
        pk = Ed25519PublicKey.from_public_bytes(public_key_bytes)

        try:
            pk.verify(
                self.__to_bytes(self.signature), self.__to_bytes(self.tx_to_sign())
            )
            return True
        except InvalidSignature:
            return False

    def hash_tx(self) -> str:
        msg = self.__to_bytes(self.tx_to_hash())
        digest = hashes.Hash(hashes.SHA256())
        digest.update(msg)
        return self.__from_bytes(digest.finalize())

    def tx_to_hash(self):
        return self.model_dump_json(exclude={"hash"})

    def tx_to_sign(self):
        return self.model_dump_json(exclude={"signature", "hash", "output"})

    def __to_bytes(self, message) -> bytes:
        return base64.b64decode(message)

    def __from_bytes(self, byte_message: bytes) -> str:
        return base64.b64encode(byte_message).decode("utf-8")


class TransactionException(Exception):
    pass
