
import unittest
import json
from layer1_blockchain.tx import Transaction, filter_utxos
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


class TestTransaction(unittest.TestCase):
    def setUp(self):
        sk = Ed25519PrivateKey.generate()
        self.addr1 = sk.public_key().public_bytes(
            encoding=Ed25519PublicKey,
            format=Ed25519PublicKey.PEM
        )
        self.addr1_sk = ""

        self.addr2 = "0xSu9B9dW6bm2LNw66koItXPwn5UMQg3+et2a37/zIYo8="
        self.addr2_sk  = "puO/xkwECSOheHl4o3xGjSt+BNRhqZnHaldaC1Xttog="

    def test_create(self):
        input_utxo = filter_utxos(self.addr1)[0]
        tx_dict = {
            "tx_id" : "tx2",
            "sender" : self.addr1,
            "receiver" : self.addr2, 
            "inputs" : [input_utxo.model_dump_json()],
        }
        tx_json = json.dumps(tx_dict)
        print("TX JSON: ", tx_json)

        # sign the tx



    def test_verify_signature(self):
        pass


