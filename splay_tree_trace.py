#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright 2019 Andrey Petukhov

Splay tree.
"""

import inspect
import logging
import os

import pygraphviz as pgv

from splay_tree_orig import SplayTree


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

os.makedirs("graph", exist_ok = True)

def for_all_methods(decorator):
    """
    Add decorator to all class methods.

    :param decorator: decorator
    :return: decorated class
    """
    def decorate(cls):
        members = inspect.getmembers(cls, predicate=inspect.isfunction)
        for method_name, method_value in members:
            if method_name in ("__init__", "draw"):
                continue
            setattr(cls, method_name, decorator(method_value))
        return cls
    return decorate


def draw_decorator(func):
    """
    Draw state of tree.

    :param func: called function
    :return: decorated function
    """
    def wrapper(*args, **kwargs):
        assert len(args) > 0
        tree = args[0]
        assert isinstance(tree, SplayTree)
        func_name = func.__qualname__
        message = f"{func_name}{args[1:]}"
        draw(tree, " before " + message)
        res = func(*args, **kwargs)
        draw(tree, " after " + message)
        return res
    return wrapper

def draw(tree, message):
    """Draw state."""
    logger.debug(str(tree._step) + message)
    tree._step += 1

    A = pgv.AGraph()
    A.node_attr["style"] = "filled"
    A.node_attr["shape"] = "record"
    A.node_attr["fixedsize"] = "true"
    A.node_attr["fontsize"] = 12
    for node in tree._nodes:
        label = f"""<f0> {node.val}|<f1> {node.counter}"""
        A.add_node(id(node), label=label)
        n = A.get_node(id(node))
        if not node.parent:
            n.attr["fillcolor"] = "#CFC291"
    for node in tree._nodes:
        if node.parent:
            # красный
            A.add_edge(id(node), id(node.parent), color="#F15A5A")
        if node.left:
            # зеленый
            A.add_edge(id(node), id(node.left), color="#4EBA6F")
        if node.right:
            # синий
            A.add_edge(id(node), id(node.right), color="#2D95BF")

    A.layout()
    filename = os.path.join("graph", f"{tree._step:03}-{message}.dot")
    A.draw(filename)


class Worker:
    """Worker."""

    def __init__(self):
        """Worker init."""
        self.tree = for_all_methods(draw_decorator)(SplayTree)()

    def process(self, commands):
        """Process commands."""
        res = []

        for cmd_code, x in commands:
            if cmd_code == 1:
                pos = self.tree.insert(x)
                res.append(pos)
            elif cmd_code == 2:
                self.tree.remove(x)
            else:
                raise ValueError("Invalid Command")

        return res


if __name__ == "__main__":
    worker = Worker()
    n = int(input())
    commands = []
    for _ in range(n):
        command = list(map(int, input().strip().split()))
        commands.append(command)

    res = worker.process(commands)
    print("\n".join(map(str, res)))
