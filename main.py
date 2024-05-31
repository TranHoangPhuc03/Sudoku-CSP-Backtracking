from SudokuSolver import SudokuSolver
from DosukuCaller import DosukuCaller
import backtracking
from copy import deepcopy
import time
from tabulate import tabulate
from multiprocessing import Process, Value, Manager

def is_valid_sudoku(board):
    size = len(board)
    box = size // 3
    value = []
    for row in board:
        value.append(row)
    for col in range(size):
        value.append(list(board[row][col] for row in range(size)))
    for box_row in range(box):
        for box_col in range(box):
            value.append(list(board[row + box_row*box][col + box_col*box] for row in range(box) for col in range(box)))
    for row in value:
        if len(row) != len(set(row)):
            return False
    return True

def test(board, solver):
    start_time = time.time()
    answer = solver.solve()
    execution_time = time.time() - start_time
    print(f'Execution time:  {execution_time} seconds')
    if answer:
        is_right_answer = is_valid_sudoku(answer)
        print('Is answer the right solution? ', is_right_answer)
        print('Answer: ')
        for row in answer:
            print(row)
        if not is_right_answer:
            print('Solution: ')
            for row in solution:
                print(row)
    else:
        print("Can't solve")
    return execution_time

def task(table, board, solver, stop_process):
    execution_time = test(board, solver)
    table.append(execution_time)
    stop_process.value = 1

if __name__ == '__main__':
    NUMBER_OF_TESTS = 10
    MAXIMUM_EXECUTION_TIME = 60  # seconds
    
    URL = f'https://sudoku-api.vercel.app/api/dosuku?query={{newboard(limit:{NUMBER_OF_TESTS}){{grids{{value,difficulty}}}}}}'
    dosuku_caller = DosukuCaller(URL)
    grids = dosuku_caller.GetGrids()
    
    manager = Manager()
    execution_time_algorithms = {
        'Forward Checking backtracking': manager.list(),
        'MAC backtracking' : manager.list(),
        'Heuristic backtracking': manager.list(),
        'Naive backtracking': manager.list()
    }
    
    for grid in grids:
        board = grid.get('value')
        
        print('The board: ')
        for row in board:
            print(row)
        
        solver = SudokuSolver(board)
        
        for algorithm, execution_time in execution_time_algorithms.items():
            print(f'--------------------\t{algorithm}\t--------------------')
            strategy = {
                'Forward Checking backtracking': backtracking.ForwardCheckingBacktracking(),
                'MAC backtracking' : backtracking.MACBacktracking(),
                'Heuristic backtracking': backtracking.HeuristicBacktracking(),
                'Naive backtracking': backtracking.NaiveBacktracking(),
            }.get(algorithm, None)
            
            solver.set_strategy(strategy) 
            
            stop_process = Value('i', 0)
            process = Process(target=task, args=(execution_time_algorithms[algorithm], board, solver, stop_process))
            process.start()
            start_time = time.time()
            while time.time() - start_time <= MAXIMUM_EXECUTION_TIME and not stop_process.value:
                pass
            if not stop_process.value:
                execution_time_algorithms[algorithm].append('None')
                print(f'Time limit exceed {MAXIMUM_EXECUTION_TIME}')
            process.terminate()
            print()
            
    print('--------------------\tStatistics--------------------')
    print(tabulate(
        tabular_data=execution_time_algorithms,
        headers='keys',
        showindex=[f'Grid {grid+1}' for grid in range(len(grids))],
        tablefmt='grid'
    ))
