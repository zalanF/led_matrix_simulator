import numpy as np
from digital_logic import HIGH, LOW
 
class led_matrix:
    def __init__(self, rows=2, cols=2):
        self.rows = rows
        self.cols = cols
        
        self.row_index = np.zeros(rows, dtype=int)
        self.col_index = np.zeros(cols, dtype=int)
         
        self._matrix = np.zeros((rows, cols), dtype=int)
        
    def display(self):
        self.update()
        print(self._matrix)
        print()
    
    def update(self):
        for r in range(self.rows):
            for c in range(self.cols):
                #clear 
                self._matrix[r, c] = LOW
                
                #re-calc
                if self.row_index[r] == HIGH and self.col_index[c] == HIGH:
                    self._matrix[r, c] = HIGH