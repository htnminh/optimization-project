from ortools.linear_solver.pywraplp import Solver


class RectFitMIP:
    def __init__(self) -> None:
        self.solver = Solver.CreateSolver("SCIP")

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
        Solver.Clear(self.solver)
        
        self.is_rotate = list()
        for i in range(N):
            self.is_rotate.append(Solver.IntVar(self.solver, 0, 1, f"R[{i}]"))
        
        # coordinates
        self.left = list()
        self.right = list()
        self.top = list()
        self.bottom = list()
        for i, (w, h) in enumerate(rect_sizes):
            self.left.append(Solver.IntVar(self.solver, 0, W, f"left[{i}]"))
            self.right.append(Solver.IntVar(self.solver, 0, W, f"right[{i}]"))

            Solver.Add(self.solver, self.right[i] == self.left[i] + w * (1 - self.is_rotate[i]) + h * self.is_rotate[i])

            self.top.append(Solver.IntVar(self.solver, 0, H, f"top[{i}]"))
            self.bottom.append(Solver.IntVar(self.solver, 0, H, f"bottom[{i}]"))

            Solver.Add(self.solver, self.bottom[i] == self.top[i] + h * (1 - self.is_rotate[i]) + w * self.is_rotate[i])
        
        M = 10000000
        
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
                    t.append(Solver.IntVar(self.solver, 0, 1, f't[{i}][{j}][{k}]'))
                    Solver.Add(self.solver, y <= M * (1 - t[-1]) + z)

                Solver.Add(self.solver, sum(t) >= 1)

    def __solve(self) -> bool:
        status = Solver.Solve(self.solver)
        if status == Solver.OPTIMAL or status == Solver.FEASIBLE:
            self.__print_solution()
            return True
        
        return False

    def __print_solution(self):
        N = len(self.is_rotate)
        for i in range(N):
            print(
                self.left[i].solution_value(),
                self.top[i].solution_value(),
                "->",  
                self.right[i].solution_value(),  
                self.bottom[i].solution_value(), 
                "::",
                self.is_rotate[i].solution_value(),
            )

rf = RectFitMIP()
print(rf.fit(3, 5, [(2, 2), (5, 1), (3, 2)]))