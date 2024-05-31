from CSP import CSP
from copy import deepcopy
from .Strategy import BacktrackingStrategy

class HeuristicBacktracking(BacktrackingStrategy):
    def __init__(self):
        self.csp = None
    
    def backtracking(self, csp : CSP):
        self.csp = csp
        self.csp.AC_3()
        return self.__backtracking({})
    
    def _select_unassign_variable(self, assignment):
        unassign_variables = [variable for variable in self.csp.variables if variable not in assignment]
        
        def count_constraint(variable):
            counter = 0
            for value in self.csp.domains[variable]:
                counter += self.csp.is_consistent(variable, value, assignment)
            return counter
        
        unassign_variables.sort(key=count_constraint)
        return unassign_variables[0]
    
    def _order_domain_values(self, variable, assignment):
        new_domain_order = deepcopy(self.csp.domains[variable])
        def count_constraint(value):
            constraint_set = set()
            for constraint in self.csp.constraints:
                if variable in constraint.variables:
                    constraint_set.update(var for var in constraint.variables if value in self.csp.domains[var])
            constraint_set.remove(variable)
            return len(constraint_set)
        new_domain_order.sort(key=count_constraint)
        return new_domain_order
    
    def __backtracking(self, assignment):
        if len(assignment) == len(self.csp.variables):
            return assignment
        
        variable = self._select_unassign_variable(assignment)
        for value in self._order_domain_values(variable, assignment):
            if self.csp.is_consistent(variable, value, assignment):
                assignment[variable] = value
                result = self.__backtracking(assignment)
                if result is not None:
                    return result
                del assignment[variable]
        return None