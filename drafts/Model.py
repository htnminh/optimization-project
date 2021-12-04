from ortools.sat.python import cp_model


class Model(cp_model.CpModel):
    def __init__(self) -> None:
        super().__init__()
        
        self.n_blocks = None
        self.n_cars = None
        self.blocks = list()
        self.cars = list()

        self._read_input()
        
        self.x: list(list(self.NewIntVar)) = list()

        self._initialize_variables()
        self._initialize_constraints()

    def _read_input(self, file_name='drafts\data.txt'):
        with open(file_name, 'r') as f:
            self.n_blocks, self.n_cars = map(int, f.readline().split())

            for _ in range(self.n_blocks):
                self.blocks.append(tuple(map(int, f.readline().split())))

            cars = list() # todo
            for _ in range(self.n_cars):
                self.cars.append(tuple(map(int, f.readline().split())))

        
    def _initialize_variables(self):
        for c in range(self.n_cars):
            self.x.append(list())
            
            for b in range(self.n_blocks):
                self.x[c].append(self.NewIntVar(0, 1, f"x[{c}][{b}]"))
        
    def _initialize_constraints(self):
        for b in range(self.n_blocks):
            sum_in_cars = cp_model.LinearExpr.Sum(
                                [self.x[c][b] for c in range(self.n_cars)])
            self.Add(sum_in_cars == 1)
        
        for c in range(self.n_cars):
            self.NewBoolVar('b')
            sum_in_blocks = cp_model.LinearExpr.Sum(
                                [self.x[c][b] for b in range(self.n_blocks)])

if __name__ == '__main__':
    model = Model()
    spaces = ' ' * 12
    print(f'n_blocks =\n{spaces}{model.n_blocks}')
    print(f'blocks =\n{spaces}{model.blocks}')
    print(f'n_cars =\n{spaces}{model.n_cars}')
    print(f'cars =\n{spaces}{model.cars}')
    print()
    print(model.ModelStats())
    

            

