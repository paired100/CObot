from machine import Pin, I2C, ADC 
from ssd1306 import SSD1306_I2C
from utime import sleep
import machine

p23 = machine.Pin(15, machine.Pin.OUT)


sleep(2)

sensorG = ADC(Pin(35))
sensorG.width(ADC.WIDTH_10BIT)
sensorG.atten(ADC.ATTN_11DB)
file = open("test.txt", "w")

ancho = 128
alto = 64

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(ancho, alto, i2c)
print(type(i2c.scan()))
scannerOled = (len(i2c.scan()))

if scannerOled > 0:
    oled.text('Bienvenidos !!!', 0, 0)
    oled.text('a Cobot un', 0, 10)
    oled.text('dispositivo para', 0, 20)
    oled.text('el control', 0, 30)
    oled.text('de gas', 0, 40)
    oled.show()
    sleep(5)
    oled.fill(0)
    oled.text('Fundacion ', 0, 0)
    oled.text('Universitaria ', 0, 10)
    oled.text('del Area Andina', 0, 20)
    oled.text('Julio de 2022', 0, 30)
    oled.show()
    sleep(5)
    oled.fill(0)
    oled.text('Estudiantes:', 0, 0)
    oled.text('Maria L Solano Meneses', 0, 10)
    oled.text('Edward E Vargas N', 0, 20)
    oled.text('Control de Nivel de gas', 0, 30)
    oled.text('de gas', 0, 40)
    oled.show()
    sleep(5)
 
buzzer = machine.PWM(p23)
 
while True:
    
    
    sleep(2)
    lectura = sensorG.read()
    if lectura >= 250:
        
        buzzer.freq(1047)
        buzzer.duty(50)
        file.write(str( "Nivel de gas =  {} % ".format(lectura)))
        file.flush()
        oled.fill(0)
        oled.text("Alerta Incendio: ",0,10)
        oled.text(str(lectura),0,20)
        oled.show()
    
        print("Nivel de gas: ",lectura)
        sleep(0.25)
    else:
        buzzer.duty(0)
        file.write(str( "Nivel de gas =  {} % ".format(lectura)))
        file.flush()
        oled.fill(0)
        oled.text("Nivel de gas: ",0,10)
        oled.text(str(lectura),0,20)
        oled.show()
    
        print("Nivel de gas: ",lectura)
        sleep(0.25)
        