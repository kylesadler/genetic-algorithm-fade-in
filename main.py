import os
import random
import subprocess
from PIL import Image
from math import ceil
from utils import *

# per step
POPULATION_SIZE = 10
NUM_OFFSPRING = 10
NUM_MUTATIONS = 10
CHANGES_PER_MUTATION = 1

def image_error(image, target):
    """ image and target are 2D lists of colors """
    output = 0

    for y in range(len(image)):
        for x in range(len(image[0])):
            output += pixel_error(image[y][x], target[y][x])

    return output

def pixel_error(pixel, target):
    # print(pixel[0], target[0], (pixel[0] - target[0])**2)
    return sum((pixel[i] - target[i])**2 for i in range(3))

def reproduce(population, num_offspring, num_mutations, changes_per_mutation):
    new_offspring = []

    for i in range(num_offspring):
        parents = random.choices(population, k=2)
        new_offspring.append(cross(parents))

    for i in range(num_mutations):
        parent = random.choices(population)[0]
        new_offspring.append(mutate(parent, changes_per_mutation))
    
    population.extend(new_offspring)

    return population

def cross(parents):
    """ return the crossbreed of parent images """
    output = []
    for y in range(len(parents[0])):
        row = []
        for x in range(len(parents[0][0])):
            # print(random.choices(parents))
            parent_of_choice = parents[random.choices(range(len(parents)))[0]]
            row.append(parent_of_choice[y][x])
        output.append(row)

    return output

def mutate(parent, num_mutations):
    width = len(parent[0])
    height = len(parent)

    for i in range(num_mutations):
        y = random.randint(0, height - 1)
        x = random.randint(0, width - 1)
        # y = random.randint(0, 3)
        # x = random.randint(0, 3)
        
        index = random.randint(0, 2)
        magnitude = 20
        rand_direction = random.randint(-magnitude, magnitude)
        
        if index == 0:
            new_color = (
                constrain(parent[y][x][0] + rand_direction, 0, 255),
                parent[y][x][1],
                parent[y][x][2]
            )
        elif index == 1:
            new_color = (
                parent[y][x][0],
                constrain(parent[y][x][1] + rand_direction, 0, 255),
                parent[y][x][2]
            )
        else:
            new_color = (
                parent[y][x][0],
                parent[y][x][1],
                constrain(parent[y][x][2] + rand_direction, 0, 255)
            )

        parent[y][x] = new_color
        # parent[y][x] = get_random_rgb()
    
    return parent

def select(population, target, pop_size=None):
    """ return the top pop_size individuals in the population
        in sorted order with most fit being first """
    i = pop_size or ceil(len(population) / 2)
    return sorted(population, key=lambda item: image_error(item, target))[:i]

def run_genetic_algorithm(starting_image, target, on_save, max_steps=None):
    counter = 0
    time = 0

    population = [starting_image]
    most_fit = starting_image
    error = image_error(most_fit, target)

    print("error", error)
    on_save(most_fit, counter)

    while (max_steps is None or time < max_steps) and error > 0:
        time += 1

        population = reproduce(population, NUM_OFFSPRING, NUM_MUTATIONS, CHANGES_PER_MUTATION)

        population = select(population, target, POPULATION_SIZE)

        new_most_fit = population[0]
        new_error = image_error(new_most_fit, target)

        if new_error < error:
            most_fit = new_most_fit
            error = new_error
            counter += 1

            print("error", error)
            on_save(most_fit, counter)
        

    print("error", error)
    on_save(most_fit, counter, last=True)


def generate_timelapse(target, output_dir, video_resolution=10, scale=None, max_steps=None, starting_image=None):
    """ returns path to timelapse mp4 """
    height = len(target)
    width = len(target[0])

    scale = scale or ceil(300 / min(height, width))
    starting_image = starting_image or get_random_rgb_image(height, width)

    makedir(output_dir)

    def save_image(data, filename):
        data = add_white_boarder(data, thickness=1)
        data = to_image(data)
        data = resize(data, scale)
        data.save(filename)

    def on_save(image, counter, last=None):
        """ what to do with images when they are saved """
        if counter % video_resolution == 0 or last:
            if last:
                counter += 1
            save_image(image, os.path.join(output_dir, f"{ceil(counter/video_resolution)}.png"))

    print("width, height", width, height)
    save_image(target, os.path.join(output_dir, "target.png"))
    save_image(starting_image, os.path.join(output_dir, "start.png"))

    run_genetic_algorithm(starting_image, target, on_save, max_steps)

    video_path = os.path.join(output_dir, 'output.mp4')
    image_path_format = os.path.join(output_dir, '%d.png')
    subprocess.run(['ffmpeg', '-i', image_path_format, '-vcodec', 'mpeg4', video_path])

    return video_path

# generate custom target images
def mario():
    """ 16 tall x 13 wide """
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (236, 71, 38)
    BLUE = (3, 45, 210)
    YELLOW = (255, 253, 84)
    BROWN = (114, 63, 19)
    SKIN = (247, 205, 160)

    return [
        [WHITE]*3 + [RED]*6 + [WHITE]*4,
        [WHITE]*2 + [RED]*10 + [WHITE]*1,
        [WHITE]*2 + [BROWN]*3 + [SKIN]*3 + [BLACK]*1 + [SKIN]*1 + [WHITE]*3,
        [WHITE, BROWN, SKIN, BROWN] + [SKIN]*4 + [BLACK]*1 + [SKIN]*3 + [WHITE]*1,
        [WHITE, BROWN, SKIN, BROWN, BROWN] + [SKIN]*4 + [BLACK]*1 + [SKIN]*3,
        [WHITE, BROWN, BROWN] + [SKIN]*5 + [BLACK]*4 + [WHITE]*1,
        [WHITE]*3 + [SKIN]*8 + [WHITE]*2,
        [WHITE]*2 + [RED]*2 + [BLUE]*1 + [RED]*4 + [WHITE]*4,
        [WHITE] + [RED]*3 + [BLUE]*1 + [RED]*2 + [BLUE]*1 + [RED]*3 + [WHITE]*2,
        [RED]*4 + [BLUE]*4 + [RED]*4 + [WHITE],
        [SKIN]*2 + [RED, BLUE, YELLOW, BLUE, BLUE, YELLOW, BLUE, RED] + [SKIN]*2 + [WHITE],
        [SKIN]*3 + [BLUE]*6 + [SKIN]*3 + [WHITE],
        [SKIN]*2 + [BLUE]*8 + [SKIN]*2 + [WHITE],
        ([WHITE]*2 + [BLUE]*3)*2 + [WHITE]*3,
        [WHITE]*1 + [BROWN]*3 + [WHITE]*4 + [BROWN]*3 + [WHITE]*2,
        [BROWN]*4 + [WHITE]*4 + [BROWN]*4 + [WHITE]*1,
    ]


def main():
    # target = generate_solid_image(
    #     color=(0, 255, 125),
    #     height=20,
    #     width=20
    # )
    # output_dir = f"test_{get_current_time_ms()}"

    # image_name = 'puppy.png'
    # target = load_image_pixels(image_name)
    # output_dir = image_name.split(".")[0]

    target = mario()
    output_dir = "mario"

    video_path = generate_timelapse(
        target,
        output_dir,
        video_resolution=10,
        max_steps=300000,
        starting_image=None
    )

    print(f"Video created: {video_path}")

if __name__ == "__main__":
    main()
    