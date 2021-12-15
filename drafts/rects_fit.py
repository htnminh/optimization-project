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
                width of rect
            H: int
                height of rect
            rect_sizes: list[tuple[int, int]]
                list of rectangle size, where size[0] is width and size[1] is height

        Returns
        -------
            return True if input rectangles can fit the rectangle (W, H)
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

                # self.Add(
                #     self.right[i] <= self.left[j] 
                #     or self.right[j] <= self.left[i]
                #     or self.bottom[i] <= self.top[j]
                #     or self.bottom[j] <= self.top[i]
                # )

                b1 = self.NewBoolVar(f"b1[{i}][{j}]")
                t1 = self.NewIntVar(0, 1, f"t1[{i}][{j}]")
                self.Add(self.right[i] <= self.left[j]).OnlyEnforceIf(b1)
                self.Add(t1 == 1).OnlyEnforceIf(b1)
                self.Add(t1 == 0).OnlyEnforceIf(b1.Not())

                b2 = self.NewBoolVar(f"b2[{i}][{j}]")
                t2 = self.NewIntVar(0, 1, f"t2[{i}][{j}]")
                self.Add(self.right[j] <= self.left[i]).OnlyEnforceIf(b2)
                self.Add(t2 == 1).OnlyEnforceIf(b2)
                self.Add(t2 == 0).OnlyEnforceIf(b2.Not())

                b3 = self.NewBoolVar(f"b3[{i}][{j}]")
                t3 = self.NewIntVar(0, 1, f"t3[{i}][{j}]")
                self.Add(self.bottom[i] <= self.top[j]).OnlyEnforceIf(b3)
                self.Add(t3 == 1).OnlyEnforceIf(b3)
                self.Add(t3 == 0).OnlyEnforceIf(b3.Not())

                b4 = self.NewBoolVar(f"b3[{i}][{j}]")
                t4 = self.NewIntVar(0, 1, f"t4[{i}][{j}]")
                self.Add(self.bottom[j] <= self.top[i]).OnlyEnforceIf(b4)
                self.Add(t4 == 1).OnlyEnforceIf(b4)
                self.Add(t4 == 0).OnlyEnforceIf(b4.Not())

                self.Add(t1 + t2 + t3 + t4 >= 1)
    
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
print(rf.fit(3, 5, [(2, 3), (5, 1), (3, 2)]))
