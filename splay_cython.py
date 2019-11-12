#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Splay tree cython."""

import splay_tree as st


class Worker:
    """Worker."""

    def __init__(self):
        """Worker init."""
        self.tree = st.SplayTree()

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
