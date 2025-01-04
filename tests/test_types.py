import unittest
from src.types import UTXO, Transaction, TransactionException
from src.cryptography import generate_key, verify_signature, sign_message


class TestTransaction(unittest.TestCase):
    def setUp(self):
        """"""
        self.addr1_sk, self.addr1_pk = generate_key()
        self.addr2_sk, self.addr2_pk = generate_key()
        self.addr3_sk, self.addr3_pk = generate_key()

        self.initial_utxo = UTXO(
            utxo_id="0@0",
            tx_id="0",
            owner=self.addr1_pk,
            amount=100,
            spent=False,
        )

    def test_new_fails(self):
        with self.assertRaises(TransactionException) as context:
            self.new_tx(amount=101)

        self.assertEqual(str(context.exception), "Not enough funds")

        with self.assertRaises(TransactionException) as context:
            self.new_tx(signature="invalid_signature")

        self.assertEqual(str(context.exception), "Invalid signature")

    def test_new_succeeds(self):
        tx = self.new_tx(
            amount=99,
        )
        signature = sign_message(self.addr1_sk, tx.tx_to_sign())
        tx.signature = signature

        self.assertEqual(tx.sender, self.addr1_pk)
        self.assertEqual(tx.receiver, self.addr2_pk)
        self.assertEqual(tx.amount, 99)
        self.assertEqual(tx.inputs, [self.initial_utxo])
        # self.assertEqual(tx.outputs, None)
        self.assertEqual(tx.outputs[0].amount, 99)
        self.assertEqual(tx.outputs[1].amount, 1)
        self.assertIsNotNone(tx.hash)
        self.assertEqual(tx.signature, signature)

        # Test signatures while you are at it
        self.assertTrue(verify_signature(self.addr1_pk, tx.tx_to_sign(), signature))
        self.assertFalse(verify_signature(self.addr2_pk, tx.tx_to_sign(), signature))

    def new_tx(
        self,
        tx_id="0",
        sender=None,
        receiver=None,
        amount=50,
        inputs=None,
        signature="",
    ):
        if not sender:
            sender = self.addr1_pk

        if not receiver:
            receiver = self.addr2_pk

        if not inputs:
            inputs = [self.initial_utxo]

        return Transaction.new(
            tx_id=tx_id,
            sender=sender,
            receiver=receiver,
            amount=amount,
            inputs=inputs,
            signature=signature,
        )
