"""Implements a tree."""


class Tree:
    """A tree. Technically a tree node. Potentially contains cycles."""

    # children will not be modified by the method, so it is not dangerous
    def __init__(self, node_id, children=[]):  # pylint: disable=dangerous-default-value
        """Constructs a tree.
        node_id is used to identify the tree node, ideally it is hashable.
        children is a list of Trees."""

        self.node_id = node_id
        self.children = children

    @classmethod
    def from_dict(cls, tree_dict):
        """Constructs a tree from a dictionary of this form:
        {"a": {"b": {}, "c": {"d": {}}}}"""
        root = list(tree_dict.keys())[0]
        children = [cls.from_dict({k: v}) for k, v in tree_dict[root].items()]
        return cls(root, children)

    def visit(self, callback):
        """Visits a node and calls callback on it."""
        callback(self)

    def visit_all(self, callback):
        """Recursively visits all nodes breath first and calls the callback on them."""
        self.visit(callback)
        for child in self.children:
            child.visit_all(callback)

    def is_circular(self):
        """Checks if a tree is circular."""
        visited = set()
        stack = []

        stack.append(self)

        while stack:
            node = stack.pop()
            if node.node_id in visited:
                return True
            visited.add(node.node_id)
            for child in node.children:
                stack.append(child)

        return False
