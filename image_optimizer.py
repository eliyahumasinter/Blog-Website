# Image size reducer
from PIL import Image
import PIL
import os
import glob


def optomize(picture):
    path = "static/images/" + str(picture)
    im = Image.open(path)
    size = im.size
    print(im.size)
    while size[0] >= 500 or size[1] >= 700:
        im = im.resize((int(size[0] / 2), int(size[1] / 2)))
        size = im.size

    print(im.size)
    im.save(path)


optomize("IMG-1287.jpg")
