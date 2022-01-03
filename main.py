import os
import random
from PIL import Image
from math import ceil
from utils import save_output, get_random_rgb, constrain, makedir, get_random_rgb_image

""" population should be a dictionary of {image: error} """

POPULATION_SIZE = 10

REPRODUCTION_FACTOR = 10
MUTATION_FACTOR = 10

def pixel_error(pixel, target):
    # print(pixel[0], target[0], (pixel[0] - target[0])**2)
    return sum((pixel[i] - target[i])**2 for i in range(3))

def image_error(image, target):
    """ image and target are 2D lists of colors """
    output = 0

    for y in range(len(image)):
        for x in range(len(image[0])):
            output += pixel_error(image[y][x], target[y][x])

    return output



# def save_gif():
#     im.save('out.gif', save_all=True, append_images=[im1, im2, ...])



def init_population(parent, size):
    """ returns a new population with given parent and size """
    output = [parent]

    for i in range(size):
        output.append(mutate(parent, 10))

    return output


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

def reproduce(population, num_offspring, num_mutations):
    new_offspring = []

    for i in range(num_offspring):
        parents = random.choices(population, k=2)
        new_offspring.append(cross(parents))

    for i in range(num_mutations):
        parent = random.choices(population)[0]
        new_offspring.append(mutate(parent, 1))
    
    population.extend(new_offspring)

    return population

def select(population, target, pop_size=None):
    """ return the top pop_size individuals in the population
        in sorted order with most fit being first """
    i = pop_size or ceil(len(population) / 2)
    return sorted(population, key=lambda item: image_error(item, target))[:i]


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


""" TODO

    init_population
    reproduce

"""


def fit(target, on_save, max_steps, starting_image=None):
    counter = 0
    time = 0

    starting_image = starting_image or get_random_rgb_image(len(target), len(target[0]))
    # population = init_population(starting_image, POPULATION_SIZE)
    population = [starting_image]
    most_fit = select(population, target)[0]
    error = image_error(most_fit, target)

    print("error", error)
    on_save(most_fit, time)

    while time < max_steps and error > 0:
        time += 1

        population = reproduce(population, REPRODUCTION_FACTOR, MUTATION_FACTOR)

        population = select(population, target, POPULATION_SIZE)

        new_most_fit = population[0]
        new_error = image_error(new_most_fit, target)

        if new_error < error:
            most_fit = new_most_fit
            error = new_error
            counter += 1

            print("error", error)
            if counter % 10 == 0:
                on_save(most_fit, time)
        

    print("error", error)
    on_save(most_fit, time)
    
def get_image_pixels(path):
    im = Image.open(path)
    pixels = list(im.getdata())
    width, height = im.size
    return [pixels[i * width:(i + 1) * width] for i in range(height)]


def main(target, output_dir, max_steps):

    makedir(output_dir)

    def on_save(image, time):
        """ what to do with images when they are saved """
        save_output(image, os.path.join(output_dir, f"{time}.jpeg"))

    print("width, height", len(target[0]), len(target))

    save_output(target, os.path.join(output_dir, "target.jpeg"))

    fit(target, on_save, max_steps, starting_image=None)

if __name__ == "__main__":
    # IMAGE_WIDTH = 10
    # IMAGE_HEIGHT = 10
    MAX_STEPS = 20000
    target = [
        [ (0, 255, 125) for i in range(100) ] for j in range(100)
    ]
    output_dir = "test"

    # image_name = 'puppy.png'
    # target = get_image_pixels(image_name)
    # output_dir = image_name.split(".")[0]

    main(target, output_dir, MAX_STEPS)