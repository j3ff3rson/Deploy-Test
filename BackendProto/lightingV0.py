import gpiozero
from gpiozero import DigitalOutputDevice
from gpiozero import PWMLED
import time

#Lighting Control Basic Function

ledMainPwr = DigitalOutputDevice(18)
#need to add comments


class LedMain(PWMLED):
    
    def __init__(self, guid):
        super().__init__(guid)
    def dim(self,level):
        if ledMainPwr.is_active == False:
            ledMainPwr.on()
        self.Dim(level)
  
    def off(self):
        ledMainPwr.off()
   
ledGrow = LedMain(25)
ledSuppOne = PWMLED(10)
ledSuppTwo = PWMLED(24)



