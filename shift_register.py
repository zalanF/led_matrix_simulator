import numpy as np
from digital_logic import HIGH, LOW


#Defines a serial in, parallel out shift regisiters of specifed size
class shift_register:
    def __init__(self, size):
        self._size =  size
        
        #Input
        self.IN = LOW #serial input input
        self._RCLK =  LOW #storage register clock, i.e, latch
        self._SRCLK = LOW #shift register clock
        
        #Internal        
        #For rising edge detection, store previous pin states
        self._prev_RCLK = LOW
        self._prev_SRCLK = LOW
        self._curr_register = 0
        self._registers = np.zeros(self.size)
        
        #Output
        self.OUT = np.zeros(self.size) #parallel out
    
    def display_registers(self):
        print(f"Registers: {self._registers}")
    
    def display_output(self):
        print(f"   Output: {self.OUT}")
        
    def display_pin_state(self):
        print(f"IN: {self.IN}, RCLK: {self._RCLK}, SRCLK: {self._SRCLK}, Curr Reg: {self._curr_register}")
    
    def display(self):
        self.display_pin_state()
        self.display_registers()
        self. display_output()
        print()
    
    def update(self):
        #Latch
        if self._detect_rising_edge(self.RCLK, self._prev_RCLK):
            self._registers[self._curr_register] = self.IN
            self._prev_RCLK = self._RCLK
        
        #Shift register clock
        if self._detect_rising_edge(self.SRCLK, self._prev_SRCLK):
            self.OUT[self._curr_register] = self._registers[self._curr_register]
            self._increment_register()
            self._prev_SRCLK = self._SRCLK
    
    #wrap the length of registers
    def _increment_register(self):
        self._curr_register += 1
        if self._curr_register == self.size:
            self._curr_register = 0
    
    
    def _detect_rising_edge(self, curr, prev):
        return curr == HIGH and prev == LOW
    
    @property
    def size(self):
        return self._size
    
    @property
    def RCLK(self):
        return self._RCLK
    
    @RCLK.setter
    def RCLK(self, rclk):
        self._prev_RCLK = self._RCLK
        self._RCLK = rclk
        self.update()
    
    @property
    def SRCLK(self):
        return self._SRCLK
     
    @SRCLK.setter
    def SRCLK(self, srclk):
        self._prev_SRCLK = self._SRCLK
        self._SRCLK = srclk
        self.update()
    
    def pulse(self, pin):
        pin = HIGH
        pin = LOW