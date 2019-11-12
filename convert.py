#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Convert .dot files to png."""

import os
import subprocess

import imageio


def convert():
    files = os.listdir("graph")
    files.sort()

    os.makedirs("png", exist_ok=True)
    os.makedirs("final", exist_ok=True)

    images_names = []

    for file in files:
        print(file)
        new_file = file[:-3] + "png"
        rendered_file = os.path.join("final", new_file)
        args1 = ["dot", "-Tpng", "-Gsize=128,72\!", "-Gdpi=100", f"-opng/{new_file}", f"graph/{file}"]
        args2 = ["convert", f"png/{new_file}", "-depth", "8", "-alpha", "off", "-gravity", "center", "-background", "white", "-extent", "1280x720", f"final/{new_file}"]
        subprocess.run(args1)
        subprocess.run(args2)
        images_names.append(rendered_file)

    images = map(imageio.imread, images_names)
    imageio.mimsave("movie.gif", images)


if __name__ == "__main__":
    convert()
