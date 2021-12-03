from copy import deepcopy

class FitSolutionFound(Exception):
    pass

# input 
with open('drafts\data.txt', 'r') as f:
    number_of_goods, number_of_cars = map(int, f.readline().split())

    goods = list()
    for _ in range(number_of_goods):
        goods.append(tuple(map(int, f.readline().split())))

    cars = list()
    for _ in range(number_of_cars):
        cars.append(tuple(map(int, f.readline().split()[:2])))
    

def fitable(good, a, i, j):
    for row in range(i, i+good[0]):
        for col in range(j, j+good[1]):
            try:
                if a[row][col] == 1:
                    return False
            except IndexError:
                return False
    return True

def insert_remove(good, a, i, j, value=1):
    a = deepcopy(a)
    for row in range(i, i+good[0]):
        for col in range(j, j+good[1]):
            a[row][col] = value
    return a

# all inputs are tuples of size


def fit(goods_indices, car_index):
    def fit_size(goods_left:list, car:tuple, a:list):
        nonlocal res
        if not res:
            if not goods_left:
                res = True
                raise FitSolutionFound('FOUND A FIT')
            else:
                good = goods_left.pop(0)
                for i in range(car[0]):
                    for j in range(car[1]):
                        if fitable(good, a, i, j):
                            a = deepcopy(insert_remove(good, a, i, j, value=1))
                            fit_size(goods_left, car, a)
                            a = deepcopy(insert_remove(good, a, i, j, value=0))
                goods_left.append(good)

    res = False
    car = cars[car_index]

    a=[[0]*car[1] for _ in range(car[0])]

    try:
        fit_size(goods_left=[goods[index] for index in goods_indices],
                        car=car,
                        a=a,
        )
    except FitSolutionFound:
        # print('Found a solution')
        pass

    return res


if __name__ == '__main__':
    print('Goods, Cars')
    print(number_of_goods, number_of_cars)
    print('Goods')
    print(*goods, sep='\n')
    print('Cars')
    print(*cars, sep='\n')

    print(fit(goods_indices=[0,1,2],
            car_index=0))