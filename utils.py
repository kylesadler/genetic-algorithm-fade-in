import os
import random
from PIL import Image

def to_image(data):
    height = len(data)
    width = len(data[0])
    # print("h,w", height, width)
    image = Image.new("RGB", (width, height), (0, 0, 0))
    pixels = image.load()

    for x in range(width):
        for y in range(height):
            pixels[x, y] = data[y][x]

    return image

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


def resize(image, scale):
    width, height = image.size
    size = (width*scale, height*scale)
    return image.resize(size, resample=Image.BOX)


def add_white_boarder(image):
    WHITE = (255, 255, 255)
    output = [
        [WHITE]*(len(image[0])+2)
    ]

    for row in image:
        output.append([WHITE] + row + [WHITE])

    output.append([WHITE]*(len(image[0])+2))
    return output

# to convert to mp4
# ffmpeg -i %d.png -vcodec mpeg4 output.mp4
