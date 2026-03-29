import led_matrix as lm
import shift_register as sr
import numpy as np
from digital_logic import HIGH, LOW

class matrix_controller:
    def __init__(self, led_matrix=lm.led_matrix()):
        self.matrix = led_matrix
        
        self.row_register = sr.shift_register(self.matrix.rows)
        self.col_register = sr.shift_register(self.matrix.cols)
        self.row_register.SRCLR_ = HIGH
        self.col_register.SRCLR_ = HIGH
        
        self.curr_row = 0
        self.curr_col = 0
        
        self.data = np.zeros((self.matrix.rows, self.matrix.cols), dtype=int)

    def increment_row(self):
        self.curr_row += 1
        if self.curr_row == self.matrix.cols:
            self.curr_row = 0

    
    def increment_col(self):
        self.curr_col += 1
        if self.curr_col == self.matrix.cols:
            self.curr_col = 0

    def step_row(self):
        if self.curr_row == 0:
            self.row_register.IN = HIGH

        self.row_register.SRCLK = HIGH
        self.row_register.SRCLK = LOW

        #for c in range(self.matrix.cols):
        #    self.step_col()
        
        self.row_register.IN = LOW
        self.increment_row()
        
        self.latch()
        self.matrix.display()

    def step_col(self):
        #first value of shift register gets pushed to the end
        #therefore, we have to start at the last value in the row of the data
        #and push that to the back to avoid flipping the image
        col = self.matrix.cols-1 - self.curr_col
        self.col_register.IN = self.data[self.curr_row, col]
        self.col_register.SRCLK = HIGH
        self.col_register.SRCLK = LOW
        self.increment_col()

    
    def latch(self):
        #Latch
        self.row_register.RCLK = HIGH
        self.row_register.RCLK = LOW
        self.col_register.RCLK = HIGH
        self.col_register.RCLK = LOW
        # defining matrix row/col connections
        self.matrix.row_index = self.row_register.OUT
        self.matrix.col_index = self.col_register.OUT

    def step(self):
        for r in range(self.matrix.rows - self.curr_row):
            for c in range(self.matrix.cols - self.curr_col):
                self.step_col()
                
            self.step_row()

if __name__ == "__main__":
    matrix = lm.led_matrix(4,4)
    controller = matrix_controller(matrix)
    data = np.identity(matrix.rows, dtype=int)
    controller.data = data
    print(data)
    matrix.display()
    controller.step()
    matrix.display()
