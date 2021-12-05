# Image size reducer
from PIL import Image
from PIL import ImageFile
import PIL
import os
import glob


ImageFile.LOAD_TRUNCATED_IMAGES = True


def optomize(picture):
    file, ending = picture.split(".")
    filename = file + ".jpeg"
    path = "static\\images\\"

    if ending == "PNG":
        try:
            im = Image.open(path + str(picture))
            im = im.convert('RGB')
            im.save(path + file + ".jpeg")
            os.remove(os.path.join(os.getcwd(), path, str(picture)))
            return str(filename)
        except FileNotFoundError:
            return str(filename)

    return str(picture)
    # size = im.size

    # while size[0] >= 300 or size[1] >= 500z
    #     im = im.resize((int(size[0] / 2), int(size[1] / 2)), resample=4)
    #     size = im.size

    # print(im.format, im.size, im.mode, os.stat(path).st_size)

    # im.save(path, optimize=True, quality=60)
    # print(im.format, im.size, im.mode, os.stat(path).st_size)
