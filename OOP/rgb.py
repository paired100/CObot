from machine import Pin , I2C, ADC
import machine


class Rgb():
    def __init__(self, activate):
        self.activate = activate
    
    def startRGB(self):
        ledRed = Pin(14, Pin.OUT)
        ledGreen = Pin(13, Pin.OUT)

        if self.activate >= 350:
            ledGreen.value(1)
            ledRed.value(0)
        else:
            ledGreen.value(0)
            ledRed.value(1)   
            
            
            
    
    