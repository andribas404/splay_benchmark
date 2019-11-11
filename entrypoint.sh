#!/usr/bin/env bash
cmake .
make
python setup.py build_ext --inplace
python make_input.py

export PATH=$PATH:/opt/benchmark

exec gosu benchmarker "$@";
