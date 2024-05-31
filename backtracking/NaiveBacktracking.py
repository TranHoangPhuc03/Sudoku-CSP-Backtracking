from CSP import CSP
from .Strategy import BacktrackingStrategy

class NaiveBacktracking(BacktrackingStrategy):
    def __init__(self):
        self.csp = None
        
    def backtracking(self, csp : CSP):
        self.csp = csp
        self.csp.AC_3()
        return self.__backtracking({})
    
    def __backtracking(self, assignment):
        if len(assignment) == len(self.csp.variables):
            return assignment
        
        variable = next(variable for variable in self.csp.variables if variable not in assignment)
        for value in self.csp.domains[variable]:
            if self.csp.is_consistent(variable, value, assignment):
                assignment[variable] = value
                result = self.__backtracking(assignment)
                if result is not None:
                    return result
                del assignment[variable]
        return None