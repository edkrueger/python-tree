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
        self.steps_from_root = None
        self.min_steps_from_leaf = None
        self.max_steps_from_leaf = None

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

    def find_steps_from_root(self):
        """Finds and sets the steps_from_root attribute for each node.
        Only works on non-circular trees."""

        if self.is_circular():
            raise ValueError("Cannot call compute_steps_from_root on a circular Tree.")

        visited = set()
        queue = []

        queue.append((self, 0))

        while queue:
            node, steps = queue.pop(0)

            if node.node_id not in visited:
                visited.add(node.node_id)
                node.steps_from_root = steps

                for child in node.children:
                    queue.append((child, steps + 1))

    def _find_steps_from_leaf(self, min_max):
        """Finds and sets steps_from_leaf for each node in a non-circular tree.
        steps_from_leaf is the minimum / maximum number of steps form a leaf."""

        if self.children == []:

            if min_max == "min":
                self.min_steps_from_leaf = 0
            if min_max == "max":
                self.max_steps_from_leaf = 0

        else:

            children_steps = []

            for child in self.children:

                # pylint: disable=protected-access
                child._find_steps_from_leaf(min_max=min_max)

                if min_max == "min":
                    children_steps.append(child.min_steps_from_leaf)
                if min_max == "max":
                    children_steps.append(child.max_steps_from_leaf)

            if min_max == "min":
                self.min_steps_from_leaf = min(children_steps) + 1
            if min_max == "max":
                self.max_steps_from_leaf = max(children_steps) + 1

    def find_steps_from_leaf(self, min_max):
        """Finds and sets the min/max steps_from_leaf for each node.
        The  result is set in the min_steps_from_leaf / max_steps_from_leaf attr.
        Only works on non-circular trees."""

        if self.is_circular():
            raise ValueError("Cannot call compute_steps_from_root on a circular Tree.")

        self._find_steps_from_leaf(min_max=min_max)
