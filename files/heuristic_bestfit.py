def read_input(file_path):
    with open(file_path) as f:
        rect_count, car_count = map(int, f.readline().split())
        rects, cars = list(), list()

        for _ in range(rect_count):
            rects.append(tuple(map(int, f.readline().split())))

        for _ in range(car_count):
            cars.append(tuple(map(int, f.readline().split())))

    return rect_count, car_count, rects, cars

if __name__ == '__main__':
    rect_count, car_count, rects, cars = read_input('files/generated_data/0009.txt')
    print(rect_count)
    print(rects)
    print(car_count)
    print(cars)