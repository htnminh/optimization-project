from ortools.sat.python import cp_model


class Model(cp_model.CpModel):
    def __init__(self, n_cars: int, n_blocks: int) -> None:
        super().__init__()
        
        self.n_cars = n_cars
        self.n_blocks = n_blocks
        
        self.contains = list()

        self._initialize_variables()
        self._initialize_constraints()
        
    def _initialize_variables(self):
        for c in range(self.n_cars):
            self.contains.append(list())
            
            for b in range(self.n_blocks):
                self.contains[c].append(self.NewIntVar(1, 1, f"c[{c}][{b}]"))
        
    def _initialize_constraints(self):
        for b in range(self.n_blocks):
            linear_expr = cp_model.LinearExpr.Sum(
                                [self.contains[c][b] for c in range(self.n_cars)])
            self.AddLinearConstraint(linear_expr, 0, 1)

