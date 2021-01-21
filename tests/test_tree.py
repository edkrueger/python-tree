"""Tests tree.py"""

import pytest
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
    assert non_circular_tree.is_circular() is False
    circular_tree = Tree.from_dict({"a": {"b": {}, "c": {"a": {}}}})
    assert circular_tree.is_circular() is True


def test_find_steps_from_root():
    """Tests if Tree.find_steps_from_root."""

    tree = Tree.from_dict({"a": {"b": {"d": {}}, "c": {"e": {"f": {}}}}})
    tree.find_steps_from_root()

    steps_lookup = {}
    tree.visit_all(lambda e: steps_lookup.update({e.node_id: e.steps_from_root}))
    assert steps_lookup["a"] == 0
    assert steps_lookup["b"] == 1
    assert steps_lookup["c"] == 1
    assert steps_lookup["d"] == 2
    assert steps_lookup["e"] == 2
    assert steps_lookup["f"] == 3

    circular_tree = Tree.from_dict({"a": {"b": {}, "c": {"a": {}}}})

    with pytest.raises(ValueError):
        circular_tree.find_steps_from_root()


def test_find_steps_from_leaf():
    """Tests if Tree.find_steps_from_root."""

    tree = Tree.from_dict({"a": {"b": {"d": {}}, "c": {"e": {"f": {}}}}})
    tree.find_steps_from_leaf()

    steps_lookup = {}
    tree.visit_all(lambda e: steps_lookup.update({e.node_id: e.steps_from_leaf}))
    assert steps_lookup["a"] == 2
    assert steps_lookup["b"] == 1
    assert steps_lookup["c"] == 2
    assert steps_lookup["d"] == 0
    assert steps_lookup["e"] == 1
    assert steps_lookup["f"] == 0

    circular_tree = Tree.from_dict({"a": {"b": {}, "c": {"a": {}}}})

    with pytest.raises(ValueError):
        circular_tree.find_steps_from_leaf()
