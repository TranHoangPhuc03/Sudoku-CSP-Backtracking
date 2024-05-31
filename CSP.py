from copy import deepcopy
from abc import ABC, abstractmethod

class Constraint:
    def __init__(self, variables):
        self.variables = variables
    
    @abstractmethod
    def satisfied(self, assignment):
        pass

class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        
    def is_consistent(self, variable, value, assignment):
        copy_assignment = deepcopy(assignment)
        copy_assignment[variable] = value
        for constraint in self.constraints:
            if variable in constraint.variables and not constraint.satisfied(copy_assignment):
                return False
                
        return True
    
    def revise(self, x, y):
        revised = False
        for x_value in self.domains[x]:
            counter = 0
            for y_value in self.domains[y]:
                counter += self.is_consistent(y, y_value, {x : x_value})
            if counter == 0:
                self.domains[x].remove(x_value)
                revised = True
        return revised
    
    def AC_3(self, queue = []):
        if len(queue) == 0:
            for constraint in self.constraints:
                for x in constraint.variables:
                    for y in constraint.variables:
                        if x != y:
                            queue.append([x, y])
                            
        while len(queue):
            x, y = queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                
                for constraint in self.constraints:
                    if x in constraint.variables:
                        queue.extend([[k, x] for k in constraint.variables if k != x and k != y])
        return True