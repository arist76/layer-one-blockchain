from fastapi import FastAPI
import os

REDIS_NODE = "redis://127.0.0.1:6379/0"
app = FastAPI()

@app.get("/")
def node_details():
    port = os.getenv("LOCAL") or "0"
    return NodeWithRemote(
        node_id=int(port),
        host="localhost",
        port=int(port)
    )

