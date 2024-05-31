# Sudoku Solver using Constraint Satisfaction Problem (CSP) and Backtracking Search

## Algorithms
* Naive backtracking
* Backtracking with Minimum Remaining Values (MRV) and Least Constraint Values (LCV) heuristics
* Backtracking with Forward Checking
* Backtracking with Maintaining Arc Consistency

## Requirements

To install the required dependencies, run the following command:

```
    pip install -r requirements.txt
```

## Example
```
    sudoku_board = ... # can custom or call api in DosukuCaller.py
    solver = SudokuSolver(sudoku_board) # init the sudoku solver
    strategy_backtracking = ForwardCheckingBacktracking() # select which algorithm is used
    solver.set_strategy(strategy_backtracking)
    answer = solver.solve()
```