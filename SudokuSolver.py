from CSP import CSP, Constraint
from backtracking import BacktrackingStrategy
from copy import deepcopy

class AllDiffConstraint(Constraint):
    def satisfied(self, assignment):
        values = [value for variable, value in assignment.items() if variable in self.variables]
        return len(values) == len(set(values))

class SudokuSolver:
    def __init__(self, board):
        self.board = board
        self.size = len(board)
        self.box_size = int(self.size ** 0.5)
        self.variables = [(i, j) for i in range(self.size) for j in range(self.size)]
        self.domains = {(i, j): list(range(1, self.size + 1)) if self.board[i][j] == 0\
                                else [self.board[i][j]] for i, j in self.variables}
        self.constraints = self.generate_constraints()
        self.csp = CSP(self.variables, self.domains, self.constraints)
        self.backtracking_strategy = None
        
    def generate_constraints(self):
        constraints = []
        for i in range(self.size):
            related_vars_row = [(i, j) for j in range(self.size)]
            constraints.append(AllDiffConstraint(related_vars_row))
        for j in range(self.size):
            related_vars_col = [(i, j) for i in range(self.size)]
            constraints.append(AllDiffConstraint(related_vars_col))
        for i in range(0, self.size, self.box_size):
            for j in range(0, self.size, self.box_size):
                related_vars_box = [(self.box_size * (i // self.box_size) + r,\
                                    self.box_size * (j // self.box_size) + c)\
                                    for r in range(self.box_size) for c in range(self.box_size)]
                constraints.append(AllDiffConstraint(related_vars_box))
        return constraints

    def set_strategy(self, strategy : BacktrackingStrategy):
        self.backtracking_strategy = strategy

    def solve(self):
        solution = self.backtracking_strategy.backtracking(deepcopy(self.csp))
        
        if solution:
            complete_board = [[solution[(i, j)] for j in range(self.size)] for i in range(self.size)]
            return complete_board
        else:
            return None