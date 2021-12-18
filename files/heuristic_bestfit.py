from copy import deepcopy
import time


# -------------------------------- FIT --------------------------------
class FitSolutionFound(Exception):
    pass


class TimeExceededError(Exception):
    pass


def fitable_not_rotated(rect, a, i, j):
    for row in range(i, i+rect[0]):
        for col in range(j, j+rect[1]):
            try:
                if a[row][col] == 1:
                    return False
            except IndexError:
                return False
    return True


def fitable_rotated(rect, a, i, j):
    for row in range(i, i+rect[1]):
        for col in range(j, j+rect[0]):
            try:
                if a[row][col] == 1:
                    return False
            except IndexError:
                return False
    return True


def fitable(rect, a, i, j):
    '''
    return None if not fit,
    return True if don't need to rotate
    return False if need to rotate
    '''
    if fitable_not_rotated(rect, a, i, j):
        return True
    elif fitable_rotated(rect, a, i, j):
        return False
    else:
        return None


def insert_remove(rect, a, i, j, not_rotate, value=1):
    a = deepcopy(a)
    if not_rotate:
        for row in range(i, i+rect[0]):
            for col in range(j, j+rect[1]):
                a[row][col] = value
    else:
        for row in range(i, i+rect[1]):
            for col in range(j, j+rect[0]):
                a[row][col] = value
    return a


def fit(rects_to_fit, car_to_fit):
    global GLOBAL_time_start, GLOBAL_time_end

    def fit_size(rects_left:list, car:tuple, a:list):
        nonlocal res
        if not res:
            if not rects_left:
                res = True
                raise FitSolutionFound
            else:
                rect = rects_left.pop(0)

                for i in range(car[0]):
                    for j in range(car[1]):
                        GLOBAL_time_end = time.time()
                        if GLOBAL_time_end - GLOBAL_time_start > GLOBAL_TIME_LIMIT:
                            raise TimeExceededError

                        fitable_var = fitable(rect, a, i, j)
                        if fitable_var is not None:
                            a = deepcopy(insert_remove(rect, a, i, j, fitable_var, value=1))
                            fit_size(rects_left, car, a)
                            a = deepcopy(insert_remove(rect, a, i, j, fitable_var, value=0))
                rects_left.append(rect)

    res = False

    a=[[0]*car_to_fit[1] for _ in range(car_to_fit[0])]

    try:
        fit_size(rects_left=rects_to_fit,
                        car=car_to_fit,
                        a=a,
        )
    except FitSolutionFound:
        # print('Found a solution')
        pass

    return res


# -------------------------------- READ INPUT --------------------------------
def read_input(file_path):
    with open(file_path) as f:
        rect_count, car_count = map(int, f.readline().split())
        rects, cars = list(), list()

        for _ in range(rect_count):
            rects.append(tuple(map(int, f.readline().split())))

        for _ in range(car_count):
            cars.append(tuple(map(int, f.readline().split())))

    return rect_count, car_count, rects, cars


# -------------------------------- UTILITIES --------------------------------
def area(tup):
    return tup[0] * tup[1]


def fee_per_area(tup):
    return tup[2] / (tup[0]*tup[1])


def used_cars(rects_contained):
    return [index for index, lst in enumerate(rects_contained) if lst]


def total_cost(cars, used_cars):
    return sum(car[2] for index, car in enumerate(cars) if index in used_cars)


# -------------------------------- MAIN --------------------------------
if __name__ == '__main__':

    # -------------------------------- READ INPUT --------------------------------
    rect_count, car_count, rects, cars = read_input('files/generated_data/0150.txt')
    print(rect_count)
    print(rects)
    print(car_count)
    print(cars)
    print()

    # -------------------------------- SORT --------------------------------
    # rects: area descending order
    rects.sort(key=area, reverse=True)
    print(rects)

    # cars: fee per area ascending order
    cars.sort(key=fee_per_area)
    print(cars)
    print()

    # -------------------------------- INITIALIZE --------------------------------
    areas_left = [area(car) for car in cars]
    rects_contained = [list() for _ in range(len(cars))]
    
    # -------------------------------- RUN BEST-FIT HEURISTIC --------------------------------
    while rects:
        # -------------------------------- TAKE A RECT --------------------------------
        print(f'Number of rects left: {len(rects)}')

        rect = rects.pop(0)
        area_rect = area(rect)

        # -------------------------------- ITERATE THROUGH CARS --------------------------------
        for index, (car, area_left, rects_contained_in_car) in \
                enumerate(zip(cars, areas_left, rects_contained)):
            if area_left < area_rect:
                continue
            
            # GLOBAL_TIME_LIMIT should be >= 0.01, or the algorithm might be so bad, 
            # or worst, running infinitely. 
            # A good time limit should be between 0.1 and 10 seconds.
            GLOBAL_TIME_LIMIT = 0.1
            GLOBAL_time_start = time.time()
            GLOBAL_time_end = time.time()

            try:
                if fit(rects_contained_in_car+[rect], car):
                    areas_left[index] -= area_rect
                    rects_contained[index].append(rect)
                    break
            except TimeExceededError:
                print(f'#{index} Iteration, #{len(rects)+1} rect: The iteration exceeded {GLOBAL_TIME_LIMIT} second(s) limit, skipped a potential better solution')
                continue

    # -------------------------------- PRINT SOLUTION --------------------------------
    print()
    print('THE SOLUTION FOUND:')
    print(rects_contained)

    used_cars_var = used_cars(rects_contained)
    print('NUMBER OF CARS USED:')
    print(len(used_cars_var))
    
    print('COST:')
    print(total_cost(cars, used_cars_var))
    
