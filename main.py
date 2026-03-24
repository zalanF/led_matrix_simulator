import sys
import led_matrix as lm
import shift_register as sr
from digital_logic import HIGH, LOW

def main():
    
    matrix = lm.led_matrix(16,16)
    matrix.display()
    
    #matrix.row_index[0] = HIGH
    #matrix.col_index[0:4] = HIGH

    #matrix.display()
    
    row_register = sr.shift_register(matrix.rows)
    row_register.SRCLR_ = HIGH # turn clear off
    col_register = sr.shift_register(matrix.cols)
    col_register.SRCLR_ = HIGH # turn clear off
    

    row_register.IN = HIGH
    col_register.IN = HIGH
    #Shift 1 into all registers
    for r in range(matrix.rows):
        row_register.SRCLK = HIGH
        row_register.SRCLK = LOW
        for c in range(matrix.cols):
            col_register.SRCLK = HIGH
            col_register.SRCLK = LOW

    #Latch outputs
    row_register.RCLK = HIGH
    row_register.RCLK = LOW
    col_register.RCLK = HIGH
    col_register.RCLK = LOW
    
    matrix.row_index = row_register.OUT
    matrix.col_index = col_register.OUT
    matrix.update()
    matrix.display()
    
if __name__ == "__main__":
    sys.exit(main())