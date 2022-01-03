import os
import random
from PIL import Image

def save_output(data, filename):
    height = len(data)
    width = len(data[0])
    # print("h,w", height, width)
    image = Image.new("RGB", (width, height), (0, 0, 0))
    pixels = image.load()

    for x in range(width):
        for y in range(height):
            pixels[x, y] = data[y][x]

    image.save(filename)

def get_random_rgb():
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
        )

def get_random_rgb_image(height, width):
    return [
        [ get_random_rgb() for i in range(width) ] for j in range(height)
    ]

def constrain(x, a, b):
    return min(max(x, a), b)


def makedir(path):
    if not os.path.exists(path):
        os.mkdir(path)