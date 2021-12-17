from ortools.sat.python import cp_model


def input_data(file_path):
    with open(file_path) as f:
        n_rectangles, n_cars = [int(x) for x in f.readline().split()]
        rectangles, cars = [], []

        for _ in range(n_rectangles):
            # width and weight of rectangle
            rectangles.append([int(x) for x in f.readline().split()])

        for _ in range(n_cars):
            # width, height and cost of car
            cars.append([int(x) for x in f.readline().split()])

    return n_rectangles, n_cars, rectangles, cars

if __name__ == '__main__':
    n_rectangles, n_cars, rectangles, cars = input_data("Test_data/2d bin packing.txt")
    max_width, max_height = max(cars, key=lambda x: x[0])[0], max(cars, key=lambda x: x[1])[1]

    model = cp_model.CpModel()

    # car[i] = 1 iff it is used
    is_use_car = [model.NewIntVar(0, 1, f'is_use_car[{i}]') for i in range(n_cars)]

    # rotate[i] = 1 iff rectangle[i] rotates 90 degree
    rotate = [model.NewIntVar(0, 1, f'rotate[{i}]') for i in range(n_rectangles)]

    # car_index[i] is the index of the car in which rectangle[i] should be placed
    car_index = [model.NewIntVar(0, n_cars - 1, f'car_index[{i}]') for i in range(n_rectangles)]

    # coordinates
    left = []
    right = []
    top = []
    bottom = []

    for i in range(n_rectangles):
        left.append(model.NewIntVar(0, max_width, f'left[{i}]'))
        right.append(model.NewIntVar(0, max_width, f'right[{i}]'))
        top.append(model.NewIntVar(0, max_height, f'top[{i}]'))
        bottom.append(model.NewIntVar(0, max_height, f'bottom[{i}]'))

        model.Add(right[i] == left[i] + rectangles[i][0]).OnlyEnforceIf(rotate[i].Not())
        model.Add(right[i] == left[i] + rectangles[i][1]).OnlyEnforceIf(rotate[i])
        model.Add(top[i] == bottom[i] + rectangles[i][1]).OnlyEnforceIf(rotate[i].Not())
        model.Add(top[i] == bottom[i] + rectangles[i][0]).OnlyEnforceIf(rotate[i])

    for i in range(n_rectangles - 1):
        for j in range(i + 1, n_rectangles):
            b1 = model.NewBoolVar(f'b1[{i}][{j}]')
            t1 = model.NewIntVar(0, 1, f't1[{i}][{j}]')
            model.Add(right[i] <= left[j]).OnlyEnforceIf(b1)
            model.Add(t1 == 1).OnlyEnforceIf(b1)
            model.Add(t1 == 0).OnlyEnforceIf(b1.Not())

            b2 = model.NewBoolVar(f"b2[{i}][{j}]")
            t2 = model.NewIntVar(0, 1, f"t2[{i}][{j}]")
            model.Add(right[j] <= left[i]).OnlyEnforceIf(b2)
            model.Add(t2 == 1).OnlyEnforceIf(b2)
            model.Add(t2 == 0).OnlyEnforceIf(b2.Not())

            b3 = model.NewBoolVar(f"b3[{i}][{j}]")
            t3 = model.NewIntVar(0, 1, f"t3[{i}][{j}]")
            model.Add(top[i] <= bottom[j]).OnlyEnforceIf(b3)
            model.Add(t3 == 1).OnlyEnforceIf(b3)
            model.Add(t3 == 0).OnlyEnforceIf(b3.Not())

            b4 = model.NewBoolVar(f"b4[{i}][{j}]")
            t4 = model.NewIntVar(0, 1, f"t4[{i}][{j}]")
            model.Add(top[j] <= bottom[i]).OnlyEnforceIf(b4)
            model.Add(t4 == 1).OnlyEnforceIf(b4)
            model.Add(t4 == 0).OnlyEnforceIf(b4.Not())

            # non-overlap
            b0 = model.NewBoolVar('b0')
            model.Add(car_index[i] == car_index[j]).OnlyEnforceIf(b0)
            model.Add(car_index[i] != car_index[j]).OnlyEnforceIf(b0.Not())
            model.Add(t1 + t2 + t3 + t4 >= 1).OnlyEnforceIf(b0)
            model.Add(t1 + t2 + t3 + t4 == 0).OnlyEnforceIf(b0.Not())

    for i in range(n_rectangles):
        for j in range(n_cars):
            c = model.NewBoolVar('c')
            model.Add(car_index[i] == j).OnlyEnforceIf(c)
            model.Add(car_index[i] != j).OnlyEnforceIf(c.Not())
            model.Add(right[i] <= cars[j][0]).OnlyEnforceIf(c)
            model.Add(top[i] <= cars[j][1]).OnlyEnforceIf(c)

    for j in range(n_cars):
        is_put_to_car = [model.NewIntVar(0, 1, f'{i}') for i in range(n_rectangles)]
        for i in range(n_rectangles):
            d = model.NewBoolVar('d')
            model.Add(car_index[i] == j).OnlyEnforceIf(d)
            model.Add(is_put_to_car[i] == 1).OnlyEnforceIf(d)
            model.Add(car_index[i] != j).OnlyEnforceIf(d.Not())
            model.Add(is_put_to_car[i] == 0).OnlyEnforceIf(d.Not())
        e = model.NewBoolVar('e')
        model.Add(sum(is_put_to_car) == 0).OnlyEnforceIf(e)
        model.Add(is_use_car[j] == 0).OnlyEnforceIf(e)
        model.Add(sum(is_put_to_car) != 0).OnlyEnforceIf(e.Not())
        model.Add(is_use_car[j] == 1).OnlyEnforceIf(e.Not())

    # Objective
    cost = sum(is_use_car[j] * cars[j][2] for j in range(n_cars))
    model.Minimize(cost)

    # Creates solver and solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f'Min cost: {solver.ObjectiveValue()}')
        for i in range(n_rectangles):
            print(f'put rectangle{i + 1} in car{solver.Value(car_index[i]) + 1} with rotate: {solver.Value(rotate[i])}, at left: {solver.Value(left[i])} and bottom: {solver.Value(bottom[i])}')