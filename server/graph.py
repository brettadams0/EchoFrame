# server/graph.py
# 🌐 Simple graph manager for tracking recursive thought nodes

import uuid
from generator import expand_thought


class Node:
    def __init__(self, content, parent_id=None):
        self.id = str(uuid.uuid4())
        self.content = content
        self.parent_id = parent_id
        self.children = []

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "parent": self.parent_id,
            "children": [child.id for child in self.children]
        }


class ThoughtGraph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, content, parent_id=None):
        node = Node(content, parent_id)
        self.nodes[node.id] = node
        if parent_id and parent_id in self.nodes:
            self.nodes[parent_id].children.append(node)
        return node

    def expand_node(self, node_id):
        if node_id not in self.nodes:
            return []

        base_node = self.nodes[node_id]
        branches = expand_thought(base_node.content)
        new_nodes = [self.add_node(b, parent_id=node_id) for b in branches]
        return [n.to_dict() for n in new_nodes]

    def get_full_graph(self):
        return [node.to_dict() for node in self.nodes.values()]

    def get_root(self):
        for node in self.nodes.values():
            if node.parent_id is None:
                return node
        return None
