from CSP import CSP
from copy import deepcopy
from .Strategy import BacktrackingStrategy
from .HeuristicBacktracking import HeuristicBacktracking

class MACBacktracking(HeuristicBacktracking):
    def __init(self):
        self.csp = None
        
    def backtracking(self, csp : CSP):
        self.csp = csp
        self.csp.AC_3()
        return self.__backtracking({})
    
    def __MAC(self, variable, assignment):
        queue = []
        for constraint in self.csp.constraints:
            if variable in constraint.variables:
                for var in constraint.variables:
                    if var != variable and var not in assignment:
                        queue.append([var, variable])
        return self.csp.AC_3(queue)
    
    def __backtracking(self, assignment):
        if len(assignment) == len(self.csp.variables):
            return assignment
        
        variable = super()._select_unassign_variable(assignment)
        for value in super()._order_domain_values(variable, assignment):
            if self.csp.is_consistent(variable, value, assignment):
                assignment[variable] = value
                old_csp = deepcopy(self.csp)
                inferences = self.__MAC(variable, assignment)
                if inferences:
                    result = self.__backtracking(assignment)
                    if result is not None:
                        return result
                    self.csp = old_csp
                del assignment[variable]
        return None