"""
Copyright 2019 Andrey Petukhov

Setup.

python setup.py build_ext --inplace
"""

from distutils.core import setup

from Cython.Build import cythonize

setup(ext_modules=cythonize('splay_tree.pyx'))
