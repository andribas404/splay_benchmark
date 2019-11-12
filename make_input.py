#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create input."""

import random


MAX_SIZE = int(9e4)


def create_input():
    """Create input file."""
    cmds = list(zip(["1"] * MAX_SIZE, map(str, range(1, MAX_SIZE + 1))))
    random.seed(100)
    random.shuffle(cmds)
    res = "\n".join(map(" ".join, cmds))
    with open("input_large.txt", "w") as f:
        f.write(f"{MAX_SIZE}\n")
        f.write(res)


if __name__ == "__main__":
    create_input()
