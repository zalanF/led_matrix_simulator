import sys
import led_matrix as lm
import shift_register as sr
import matrix_controller as mc
from digital_logic import HIGH, LOW
import numpy as np

import tkinter as tk
from tkinter import ttk

class led_matrix_gui(ttk.Frame):
    def __init__(self, master=None, controller=mc.matrix_controller()):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.master.title("Led Matrix")

        self.controller = controller
        self._rows = controller.matrix.rows
        self._cols = controller.matrix.cols
        self.led_size = 50 #Pixels
        self.leds = []

        self.createWidgets()
        
        #self.after(50, self.update_matrix)
        
    def createWidgets(self):
        width = self._rows*self.led_size
        height = self._cols*self.led_size
        background_colour = 'white'
        self.canvas = tk.Canvas(self, width=width, height=height, bg=background_colour)
        self.canvas.grid(row=0, column=0, columnspan=3)
        
        #Draw matrix
        for r in range(self._rows):
            rows = []
            for c in range(self._cols):
                x0 = r*self.led_size
                y0 = c*self.led_size
                x1 = (r+1)*self.led_size
                y1 = (c+1)*self.led_size
                fill = 'red' if self.controller.matrix._matrix[r, c] == HIGH else 'black'  
                led = self.canvas.create_oval(x0, y0, x1, y1, fill=fill, outline=background_colour)
                rows.append(led)       
            self.leds.append(rows)


        self.btn_col = ttk.Button(self, text="Step Col", command=self.step_col)
        self.btn_col.grid(row=1, column=0)

        self.btn_row = ttk.Button(self, text="Step Row", command=self.step_row)
        self.btn_row.grid(row=1, column=1)

        self.btn_step = ttk.Button(self, text="Step", command=self.step)
        self.btn_step.grid(row=1, column=2)
        

    def update_matrix(self):
        for r in range(self._rows):
            for c in range(self._cols):
                fill = 'red' if self.controller.matrix._matrix[r, c] == HIGH else 'black'
                self.canvas.itemconfig(self.leds[c][r], fill=fill)

    def step_col(self):
        self.controller.step_col()
        self.controller.latch()
        self.update_matrix()

    def step_row(self):
        for c in range(self._cols):
            self.controller.step_col()
        self.controller.step_row()
        self.update_matrix()
    
    def step(self):
        self.controller.step()
        self.update_matrix()

    #def update(self):
'''
def controller(matrix: lm.led_matrix, row_register: sr.shift_register, col_register: sr.shift_register, data):
    row_register.IN = HIGH
    for r in range(matrix.rows):
        row_register.SRCLK = HIGH
        row_register.SRCLK = LOW
        row_register.display()
        for c in range(matrix.cols):
            col_register.IN = data[r,c]
            col_register.SRCLK = HIGH
            col_register.SRCLK = LOW

        #Latch
        row_register.RCLK = HIGH
        row_register.RCLK = LOW
        col_register.RCLK = HIGH
        col_register.RCLK = LOW
        # defining matrix row/col connections
        matrix.row_index = row_register.OUT
        matrix.col_index = col_register.OUT
        
        matrix.update()
        matrix.display()
        
        row_register.IN = LOW
'''
def main():
    matrix = lm.led_matrix(16,16)
    matrix.display()

    #row_register.IN = HIGH
    #col_register.IN = HIGH
    data_raw = [
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
       [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0,],
       [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0,],
       [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,],
       [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0,],
       [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0,],
       [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0,],
       [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0,],
       [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0,],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,],
    ]
    data = np.array(data_raw) #only doing this because numpy arrays have better indexing
    data = np.identity(matrix.rows, dtype=int)
    data = np.ones((matrix.rows, matrix.cols), dtype=int)

    controller = mc.matrix_controller(matrix)
    controller.data = data
    
    gui = led_matrix_gui(controller=controller)
    gui.mainloop()
    
if __name__ == "__main__":
    sys.exit(main())