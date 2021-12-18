from ortools.sat.python import cp_model


class RectFit(cp_model.CpModel):
    def __init__(self):
        super().__init__()

        self.solver = cp_model.CpSolver()

    def fit(self, W: int, H: int, rect_sizes: list[tuple[int, int]]) -> bool:
        """
        Parameters
        ----------
            W: int
                width of car
            H: int
                height of car
            rect_sizes: list[tuple[int, int]]
                list of rectangle size, where size[0] is width and size[1] is height

        Returns
        -------
            return True if input rectangles can fit the car (W, H)
        """
        self.__set_up(W, H, rect_sizes)
        return self.__solve()

    def __set_up(self, W: int, H: int, rect_sizes: list[tuple[int, int]]):
        N = len(rect_sizes)
        self.ClearAssumptions()
        
        self.is_rotate = list()
        for i in range(N):
            self.is_rotate.append(self.NewIntVar(0, 1, f"R[{i}]"))
        
        # coordinates
        self.left = list()
        self.right = list()
        self.top = list()
        self.bottom = list()
        for i, (w, h) in enumerate(rect_sizes):
            self.left.append(self.NewIntVar(0, W, f"left[{i}]"))
            self.right.append(self.NewIntVar(0, W, f"right[{i}]"))

            self.Add(self.right[i] == self.left[i] + w).OnlyEnforceIf(self.is_rotate[i].Not())
            self.Add(self.right[i] == self.left[i] + h).OnlyEnforceIf(self.is_rotate[i])

            self.top.append(self.NewIntVar(0, H, f"top[{i}]"))
            self.bottom.append(self.NewIntVar(0, H, f"bottom[{i}]"))

            self.Add(self.bottom[i] == self.top[i] + h).OnlyEnforceIf(self.is_rotate[i].Not())
            self.Add(self.bottom[i] == self.top[i] + w).OnlyEnforceIf(self.is_rotate[i])

        # constraint of not overlaping
        for i in range(N - 1):
            for j in range(i + 1, N):

                constraints = [
                    (self.right[i], self.left[j]),
                    (self.right[j], self.left[i]),
                    (self.bottom[i], self.top[j]),
                    (self.bottom[j], self.top[i]),
                ]

                t = list()
                for k, (y, z) in enumerate(constraints):
                    t.append(self.NewIntVar(0, 1, f"t[{i}][{j}][{k}]"))
                    self.Add(y <= z).OnlyEnforceIf(t[k])

                self.Add(sum(t) >= 1)
    
    def __solve(self) -> bool:
        status = self.solver.Solve(self)
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            self.__print_solution()
            return True
        
        return False

    def __print_solution(self):
        N = len(self.is_rotate)
        for i in range(N):
            print(
                self.solver.Value(self.left[i]), 
                self.solver.Value(self.top[i]),
                "->",  
                self.solver.Value(self.right[i]),  
                self.solver.Value(self.bottom[i]),  
                "::",
                self.solver.Value(self.is_rotate[i])
            )

rf = RectFit()
print(rf.fit(3, 5, [(2, 2), (5, 1), (3, 2)]))
