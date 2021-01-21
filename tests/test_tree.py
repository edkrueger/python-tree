"""Tests tree.py"""

from resc.tree import Tree


def test_tree_from_constructor():
    """Tests a tree when generated from the constructor."""

    tree = Tree("a", [Tree("b"), Tree("c", [Tree("d")])])

    first_node = set()
    tree.visit(lambda e: first_node.add(e.node_id))
    assert first_node == {"a"}

    all_nodes = set()
    tree.visit_all(lambda e: all_nodes.add(e.node_id))
    assert all_nodes == {"a", "b", "c", "d"}


def test_tree_from_dict():
    """Tests a tree when generated from dict."""

    tree = Tree.from_dict({"a": {"b": {}, "c": {"d": {}}}})

    first_node = set()
    tree.visit(lambda e: first_node.add(e.node_id))
    assert first_node == {"a"}

    all_nodes = set()
    tree.visit_all(lambda e: all_nodes.add(e.node_id))
    assert all_nodes == {"a", "b", "c", "d"}


def test_is_circular():
    """Tests if Tree.is_circular works."""

    non_circular_tree = Tree.from_dict({"a": {"b": {}, "c": {"d": {}}}})
    assert not non_circular_tree.is_circular()
    circular_tree = Tree.from_dict({"a": {"b": {}, "c": {"a": {}}}})
    assert circular_tree.is_circular()
