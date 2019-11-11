#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Create input."""

import random


MAX_SIZE = int(9e4)
cmds = list(zip(["1"] * MAX_SIZE, map(str, range(1, MAX_SIZE + 1))))
random.seed(100)
random.shuffle(cmds)
res = "\n".join(map(" ".join, cmds))
with open("input_large.txt", "w") as f:
    f.write("90000\n")
    f.write(res)
