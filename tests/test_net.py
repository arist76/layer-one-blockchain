import unittest
from layer1_blockchain import net


class TestNet(unittest.TestCase):
    def test_node_init(self):

        node = net.Node(6, "127.0.0.1", 5000)
        self.assertEqual(node.host, "127.0.0.1")
        self.assertEqual(node.port, 5000)
        self.assertEqual(node.node_id, 6)

        node2 = net.Node(7, "127.0.0.1", 5011)
        self.assertEqual(node2.host, "127.0.0.1")
        self.assertEqual(node2.port, 5011)
        self.assertEqual(node2.node_id, 7)
