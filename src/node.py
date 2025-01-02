from pydantic import BaseModel
from typing import List
import httpx
import os


class Node(BaseModel):
    node_id: int
    host: str
    port: int

    async def broadcast(self, message):
        for node in self._remote_nodes():

            url = f"http://{node.host}:{node.port}/transaction"
            async with httpx.AsyncClient() as client:
                await client.post(url, json=message)

    @classmethod
    def _remote_nodes(cls) -> List["Node"]:

        remote_ports = os.getenv("REMOTE") or ""
        remote_ports = remote_ports.split(",")

        return [
            Node(node_id=int(port), host="localhost", port=int(port))
            for port in remote_ports
        ]

class NodeWithRemote(Node):
    remote_nodes : list[Node] = Node._remote_nodes()

