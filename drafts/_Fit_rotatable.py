from copy import deepcopy


class FitSolutionFound(Exception):
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