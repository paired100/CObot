from machine import ADC ,Pin
from utime import sleep
import utime

class Sensor():
    def __init__(self):
        self.lectura = 0
    
    
    def sensorMQ2(self):
        sensorName = ADC(Pin(35))
        sensorName.width(ADC.WIDTH_10BIT)
        sensorName.atten(ADC.ATTN_11DB)
        sleep(4)
        lectura = sensorName.read()
        self.lectura = lectura
        print ( "Nivel de gas =  {} % ".format(lectura))

        return lectura