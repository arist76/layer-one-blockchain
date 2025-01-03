from fastapi import FastAPI
from pydantic import BaseModel
from hashlib import sha256
from typing import List, Optional
from time import time
from uuid import uuid4
import httpx


# FastAPI Setup
app = FastAPI()
blockchain = Blockchain()

@app.get("/chain")
def get_chain():
    return {"chain": blockchain.chain, "length": len(blockchain.chain)}

@app.post("/transactions/new")
def new_transaction(transaction: Transaction):
    index = blockchain.add_transaction(transaction.sender, transaction.recipient, transaction.amount)
    return {"message": f"Transaction will be added to Block {index}"}

@app.post("/mine")
def mine():
    last_block = blockchain.last_block
    last_proof = last_block.proof
    proof = blockchain.proof_of_work(last_proof)

    blockchain.add_transaction(sender="0", recipient="node_identifier", amount=1)

    block = blockchain.create_block(proof, blockchain.hash(last_block))
    return {
        "message": "New Block Forged",
        "block": block,
    }

@app.post("/nodes/register")
def register_nodes(nodes: List[str]):
    for node_address in nodes:
        blockchain.register_node(node_address)
    return {"message": "New nodes have been added", "total_nodes": [node.address for node in blockchain.nodes]}

@app.get("/nodes/resolve")
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        return {"message": "Chain was replaced", "new_chain": blockchain.chain}
    return {"message": "Chain is authoritative", "chain": blockchain.chain}










