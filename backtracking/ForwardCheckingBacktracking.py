from CSP import CSP
from copy import deepcopy
from .Strategy import BacktrackingStrategy
from .HeuristicBacktracking import HeuristicBacktracking

class ForwardCheckingBacktracking(HeuristicBacktracking):
    def __init__(self):
        self.cs = None
    
    def backtracking(self, csp : CSP):
        self.csp = csp
        self.csp.AC_3()
        return self.__backtracking({})
    
    def __forward_checking(self, variable, value):
        for constraint in self.csp.constraints:
            if variable in constraint.variables:
                for var in constraint.variables:
                    if var == variable:
                        continue
                    if value in self.csp.domains[var]:
                        self.csp.domains[var].remove(value)
                    if len(self.csp.domains[var]) == 0:
                        return False
        return True
    
    def __backtracking(self, assignment):
        if len(assignment) == len(self.csp.variables):
            return assignment
        
        variable = super()._select_unassign_variable(assignment)
        for value in super()._order_domain_values(variable, assignment):
            if self.csp.is_consistent(variable, value, assignment):
                assignment[variable] = value
                old_csp = deepcopy(self.csp)
                inferences = self.__forward_checking(variable, value)
                if inferences:
                    result = self.__backtracking(assignment)
                    if result is not None:
                        return result
                    self.csp = old_csp
                del assignment[variable]
        return None