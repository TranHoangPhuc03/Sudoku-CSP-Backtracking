import requests
import json

class DosukuCaller:
    def __init__(self, URL):
        self.URL = URL
        self.grids = []
        
    def GetGrids(self):
        request = requests.get(self.URL)
        response = request .json()
        new_board = response.get('newboard')
        self.grids = new_board.get('grids')
        return self.grids
            
    def PrintGrid(self):
        print(f'Number of grids: {len(self.grids)}')
        print(self.grids)