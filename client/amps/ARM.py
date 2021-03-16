import gpiozero
import time
from time import sleep




class Stepper():
    '''Stepper Class is to control the stepper motor using stepper controller DM322E

    gpioARMEna: set the raspberry pi pin for Enable on controller
    gpioARMDir: set the raspberry pi pin for Direction on controller
    gpioARMPul: set the raspberry pi pin for Pulse on controller
    gpioARMEndL: set the raspberry pi pin for Left Limit Sensor on controller
    gpioARMEndR: set the raspberry pi pin for Right Limit Sensor on controller
    '''
    ARMSleepTime = 0.25 # internal sleep variable

    def __init__(self,gpioARMEna,gpioARMDir,gpioARMPul,gpioARMEndL,gpioARMEndR,ARMLoc=0,ARML2RTotalStps=100000,ARMRevolution=400):
        self.ARMPins = [gpioARMEna, gpioARMDir, gpioARMPul]
        self.ARMEna = gpiozero.OutputDevice(gpioARMEna)
        self.ARMDir = gpiozero.OutputDevice(gpioARMDir)
        self.ARMPul = gpiozero.OutputDevice(gpioARMPul)
        self.ARMEndL = gpiozero.InputDevice(gpioARMEndL ,pull_up= True)
        self.ARMEndR = gpiozero.InputDevice(gpioARMEndR ,pull_up= True)
        self.ARMLoc = ARMLoc
        self.ARML2RTotalStps = ARML2RTotalStps
        self.ARMRevolution = ARMRevolution

    def Callibrate(self,state):
        '''Callibration routine to set the zero position and max step position.
        Note: zero postion gets callibrated everytime left proximity is triggered.'''
        # While State
        while ( self.ARMEndL == False):
            self.Pulsate(dir='L')
        # LEDMAIN(Alert)
        self.ARML2RTotalStps =  0
        self.ARMLoc = 0
        while(self.ARMEndL == False):
            self.Pulsate(dir='R')
            self.ARML2RTotalStps +=  1
            self.ARMLoc += 1
        # LEDMAIN(Alert)

        # moveTo(pos=0)
        # LEDMAIN(Homage)


    def Pulsate(self,dir):
        '''to move the stepper one step in a direction assigned every time it is called'''
        self.ARMEna.on()
        if dir == 'L':
            if (self.ARMEndL == False): # Check if ARM has reached far left
                if self.ARMDir.is_active == False: #check the status of direction pin and set it accordingly
                    sleep(0.25)
                    self.ARMDir.on()
                    sleep(0.25)
                    # set pulse pin on and off
                self.ARMPul.off()
                sleep(Stepper.ARMSleepTime)
                self.ARMPul.on()
                self.ARMLoc -= 1
                sleep(Stepper.ARMSleepTime)
        if dir == 'R':
            if (self.ARMEndR == False):
                if self.ARMDir.is_active == True:
                    sleep(Stepper.ARMSleepTime)
                    self.ARMDir.off()
                    sleep(Stepper.ARMSleepTime)
                self.ARMPul.off()
                sleep(Stepper.ARMSleepTime)
                self.ARMPul.on()
                sleep(Stepper.ARMSleepTime)
                self.ARMLoc += 1

        else :
            print ('Direction ')



    def goToLoc(self,location,speed):

        if location != 0:
            actualSteps = int((location * self.ARML2RTotalStps)/100)
        else :
            actualSteps = 0
        pause = 1

        if speed == 0 :
            pause = 1
        elif speed>200:
            pause = 200
        else:
            pause= speed

        pause= (0.00025)/pause

        if actualSteps > self.ARMLoc :
            while actualSteps >=  self.ARMLoc :
                self.Pulsate(dir='R')
                sleep(pause)
        elif actualSteps < self.ARMLoc:
            while actualSteps <=  self.ARMLoc :
                self.Pulsate(dir='L')
                sleep(pause)








    # def Left(self, steps, speed = 100):
    # '''Move arm left a desired number of motor steps.
    # steps: how many motor steps to move, 400 steps is one rotation
    # speed: how fast to move between 1 and 100'''
    # # Check for speed input speed will define the sleep time in the function
    #     if speed <= 0:
    #         speed = 1
    #     elif speed > 200:
    #         speed = 200
    #     pause = (0.00025)/speed


gpioARMEna = 10
gpioARMDir = 24
gpioARMPul = 21
gpioARMEndL = 8
gpioARMEndR = 11

armMaker = Stepper(gpioARMEna,gpioARMDir,gpioARMPul,gpioARMEndL,gpioARMEndR)