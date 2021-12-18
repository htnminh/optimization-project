'''
Generate 74 different input files with number of rectangles of:

    10 easy
        5, 6, 7,.., 14
         
    10 medium
        15, 11, 12,.., 24

    10 hard
        25, 21, 22,.., 34

    10 severe
        35, 36, 37,.., 44
    
    10 might be impossible without heuristics
        45, 46, 47,.., 54
    
    10 test the limit of heuristics
        60, 90, 120,.., 330
    
    10 might be impossible
        350, 400, 450,.., 800
    
    4 impossible
        850, 900, 950, 1000

Randomizing algorithm:

    Each rectangle will have a randomized size, each side
        from 1 to 5 (so the area is from 1 to 25)

    Randomize a certain amount of rectangles based on
        difficulty (above)

    Pick some (from 2 to 5) random rectangles. The first one
        is putted in the upper-left corner, then randomly put each
        of the remaining next to (right or below) of any existing
        rectangle, make sure that it fits.
                The maximum side of the car is
                    5 (rectangles) x 5 (side of each rectangle) = 25.
                    Area: 25 x 25

    After putting rectangles in, "cut off" (actually by reducing the size)
        any row or column that was not used (from the lower-most row -> up,
        from the right-most column -> left)
    
    Keep doing that until there is no rectangle left.

    Randomly generate a few more car (ceil of 1/5 number of the cars used).

    Completely randomize the cost of cars (from 100 to 2000).
'''


from math import ceil
import random as rd
from copy import Error, deepcopy
import sys

import numpy as np
import matplotlib.pyplot as plt


def plot_full_car_and_cut_car(car_array, removed_array, shape, len_cars):
    plt.plot([0, shape[1], shape[1]], [shape[0], shape[0], 0], 'red')
    plt.imshow(car_array, cmap='turbo', extent=(0,25,25,0), vmin=-1, vmax=5)
    plt.savefig(f'files/generated_figures/{len_cars}_A')
    plt.clf()

    plt.imshow(removed_array, cmap='turbo', extent=(0,shape[1],shape[0],0), vmin=-1, vmax=5)
    plt.savefig(f'files/generated_figures/{len_cars}_B')
    plt.clf()


def plot_building_solution(car_array, available_places):
    plt.imshow(car_array, cmap='turbo', extent=(0,25,25,0), vmin=-1, vmax=5)
    for place in available_places:
        plt.text(place[1]+0.5, place[0], 'x', ha='center', va='top', c='white')
    plt.savefig(f'files/generated_figures/{len(available_places)}')
    plt.clf()


def rd_a_rect() -> tuple[int, int]:
    '''random a rectangle, return size'''
    return rd.randrange(1, 6), rd.randrange(1, 6)


def rd_some_rects(rect_count: int) -> list[tuple[int, int]]:
    '''random rect_count rectangles, return a list of sizes'''
    return [rd_a_rect() for _ in range(rect_count)]


def rd_pick_some_rects(rects) -> tuple[list, list]:
    '''
    randomly pick and remove some rectangles from rects,
    return a tuple of 2 lists:
        the first list is the reduced list of rectangles,
        the second list is the picked rectangles
    '''
    rect_count = rd.randrange(2, 6)
    reduced_rects = deepcopy(rects)

    # shuffle the list, then take rectangles from top
    rd.shuffle(reduced_rects)
    picked_rects = reduced_rects[:rect_count]
    reduced_rects = reduced_rects[rect_count:]

    return reduced_rects, picked_rects


def rd_put(rects, save_figures=False) -> np.array:
    '''
    randomly put each rectangle next to each other, as described
    '''
    car_array = np.full((25, 25), fill_value=-1, dtype=int)
    available_places = [(0, 0)]

    for rect_index, rect in enumerate(rects):
        while True:
            # pick a random place to put
            rd.shuffle(available_places)
            place = available_places.pop(0)

            x_start, y_start = place
            x_end, y_end = x_start + rect[0], y_start + rect[1]

            # only put if puttable
            check_area_to_put = car_array[x_start : x_end, y_start : y_end] == -1
            if check_area_to_put.all():
                car_array[x_start : x_end, y_start : y_end] = rect_index
                break
        
        # remove old places
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                try:
                    available_places.remove((x, y))
                except ValueError:
                    pass

        # add new places
        new_avalable_places = [(x_end, y) for y in range(y_start, y_end)]
        new_avalable_places += [(x, y_end) for x in range(x_start, x_end)]

        available_places += new_avalable_places

        # plot if save_figures
        if save_figures:
            plot_building_solution(car_array, available_places)

    return car_array


def shape_after_remove_redundant(car_array: np.array) -> tuple:
    '''size remove redundant row and col, which are filled by -1'''
    array_size = list(car_array.shape)

    current_row_index = -1  # init by lowest row
    while True:
        if (car_array[current_row_index] == -1).all():
            array_size[0] -= 1
            current_row_index -= 1
        else:
            break
    
    current_col_index = -1  # init by right most col
    while True:
        if (car_array[:, current_col_index] == -1).all():
            array_size[1] -= 1
            current_col_index -= 1
        else:
            break

    return tuple(array_size)
    

def remove_redundant(car_array: np.array, shape: tuple):
    return car_array[:shape[0], :shape[1]]


def rd_car_cost():
    '''from 100 to 1000, step is 50'''
    return rd.randrange(100, 1001, 50)


def rd_car_size():
    '''from 1 to 25 each side, used only after fitting previous cars'''
    return rd.randrange(1, 26), rd.randrange(1, 26)





if __name__ == '__main__':
    if input('Type Y to generate: ') not in ['y', 'Y']:
        raise Error('Type Y to generate')

    np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)

    # numbers of rectangles based on difficulty (index)
    rect_counts = [i for i in range(5, 55)] + \
                  [i for i in range(60, 331, 30)] + \
                  [i for i in range(350, 1001, 50)]
    print('rect_counts:', rect_counts)
    print('len:', len(rect_counts))
    print()

    # seed
    seed = 69420
    rd.seed(seed)
    print('RANDOMIZING with seed:', seed)
    print()

    # generate and save
    for index_difficulty, rect_count in enumerate(rect_counts):
        # create rects randomly
        rects = rd_some_rects(rect_count)

        # create cars with rects
        copy_rects = deepcopy(rects)  # save to recover later
        cars = list()  # list of tuples of size, cost not included

        while rects:
            # save figures of: BUILD 6TH CAR OF DIFFICULTY 25
            rects, picked_rects = rd_pick_some_rects(rects)
            car_array = rd_put(picked_rects,
                               save_figures=index_difficulty==25 and len(cars)==5)
            shape = shape_after_remove_redundant(car_array)
            cars.append(shape)

            # save figures of: all cars of difficulty 25
            if index_difficulty == 25:
                plot_full_car_and_cut_car(car_array, remove_redundant(car_array, shape), shape, len(cars))

        cars += [rd_car_size() for _ in range(ceil(len(cars)/5))]

        rects = copy_rects

        # write to files
        directory = 'files/generated_data'
        file_path = f'{directory}/{str(rect_count).zfill(4)}.txt'

        with open(file_path, 'w') as f:
            f.write(f'{rect_count} {len(cars)}\n')
            for rect in rects:
                f.write(f'{rect[0]} {rect[1]}\n')
            for car in cars:
                f.write(f'{car[0]} {car[1]} {rd_car_cost()}\n')
    
    print('DONE')