#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Do benchmark."""

from collections import OrderedDict
import os
import pandas as pd
import subprocess
import time

RUNS = 5

args_python = [
    "python",
    "splay_tree_orig.py",
]

args_pypy = [
    "pypy3",
    "splay_tree_orig.py",
]

args_cython = [
    "python",
    "splay_cython.py",
]

args_cpp = [
    "st",
]

ARGS = [
    args_python,
    args_pypy,
    args_cython,
    args_cpp,
]

NAMES = [
    "python",
    "pypy",
    "cython",
    "cpp",
]


def avg(arr):
    """Count average."""
    return sum(arr) / float(len(arr))


def do_benchmark():
    """Benchmark programs."""
    with open('input_large.txt') as f:
        myinput = f.read().encode()

    rows = []

    for name, arg_list in zip(NAMES, ARGS):
        timer = []
        print(name, end="")
        for run in range(RUNS):
            start = time.perf_counter()
            subprocess.run(arg_list, input=myinput, stdout=subprocess.DEVNULL)
            finish = time.perf_counter()
            delta = finish - start
            timer.append(delta)
            print(".", end="")
        print("OK")
        row = OrderedDict()
        row["name"] = name
        row["avg"] = avg(timer)
        row.update(enumerate(timer))
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv("results.csv", index=False, float_format="%.3f")


if __name__ == "__main__":
    do_benchmark()
