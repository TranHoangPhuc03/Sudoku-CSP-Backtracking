from abc import ABC, abstractmethod
from CSP import CSP

class BacktrackingStrategy(ABC):  
    @abstractmethod
    def backtracking(self, csp : CSP):
        pass