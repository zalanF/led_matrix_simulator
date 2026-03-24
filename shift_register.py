import numpy as np
from digital_logic import HIGH, LOW


#Defines a serial in, parallel out shift regisiters of specifed size
class shift_register:
    def __init__(self, size):
        self._size = size
        
        #Input
        self.IN      = LOW  # serial data input 
        self._RCLK   = LOW  # storage register clock, i.e, latch
        self._SRCLK  = LOW  # shift register clock
        self._OE_    = LOW  # Active low; Shift register ON by default
        self._SRCLR_ = LOW  # Active low; clears by default
        
        #Internal        
        # For rising edge detection, store previous pin states
        # this is simplistic rising edge detection that doesn't consider timing 
        self._prev_RCLK = LOW
        self._prev_SRCLK = LOW
        self._registers = np.zeros(self.size)
        
        #Output
        self.OUT = np.zeros(self.size) #parallel data output
    
    def display_registers(self):
        print(f"Registers: {self._registers}")
    
    def display_output(self):
        print(f"   Output: {self.OUT}")
        
    def display_pin_state(self):
        print(f"IN: {self.IN}, RCLK: {self.RCLK}, SRCLK: {self.SRCLK}, OE: {self.OE_}, SRCLR: {self.SRCLR_}")
    
    def display(self):
        self.display_pin_state()
        self.display_registers()
        self. display_output()
        print()
    
    def update(self):
        #Output enable
        #exit the function without doing anything
        if self.OE_ == HIGH:
            return
        
        #Shift storage register
        if self._detect_rising_edge(self.SRCLK, self._prev_SRCLK):
            #copy first four registers to forward one position
            self._registers[1:] = self._registers[:self.size-1]
            #replace first register with new value
            self._registers[0] = self.IN

        #Latch output
        if self._detect_rising_edge(self.RCLK, self._prev_RCLK):
            self.OUT = self._registers.copy()

        #Clear storage register
        if self.SRCLR_ == LOW:
            self._registers.fill(0)
            
    
    def _detect_rising_edge(self, curr, prev):
        return curr == HIGH and prev == LOW
    
    @property
    def size(self):
        return self._size

    #Latch
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

    #Shift
    @SRCLK.setter
    def SRCLK(self, srclk):
        self._prev_SRCLK = self._SRCLK
        self._SRCLK = srclk
        self.update()

    #Output Enable
    @property
    def OE_(self):
        return self._OE_
     
    @OE_.setter
    def OE_(self, oe):
        self._OE_ = oe
        self.update()

    #Clear
    @property
    def SRCLR_(self):
        return self._SRCLR_
     
    @SRCLR_.setter
    def SRCLR_(self, srclr):
        self._SRCLR_ = srclr
        self.update()