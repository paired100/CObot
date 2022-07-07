#Importación de modulos y libreria
import network, time, urequests
import sh1106
import umail
import utime
import time as tiempo
import framebuf
from machine import Pin,ADC,I2C



#Inicializacion libreria sh1106 Pantalla OLED
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c)
display.sleep(False)
display.fill(0)
display.rotate(True)

#Lectura PIN Sonido Buzzer.
BUZZER=Pin(4, Pin.OUT)
BUZZER.off()

#lectura Sensor MQ2
sensor = ADC(Pin(35))
sensor.width(ADC.WIDTH_10BIT)
sensor.atten(ADC.ATTN_11DB)

#Captura de hora y fecha.
now = utime.gmtime()

#Tamaño del border de la pantalla.
width=128
height=64

#Nombre y contraseña de la Red Wifi
red = "GEORGINA"
password = "*1065652573*"

#Api envio de datos en tiempo Real a thingspeak
url = "https://api.thingspeak.com/update?api_key=N8P9PVEK8DXDCXB7"

#Api para  envio de alerta Via Email en tiempo Real a maker.ifttt.com
url2 = "https://maker.ifttt.com/trigger/Alarma/with/key/dl2ms9_oR6sAmjoMsl87ly?"

#Funcion para mostrar imagen de Bienvenida
def buscar_icono(ruta):
    dibujo= open(ruta, "rb")  # Abrir en modo lectura de bist
    dibujo.readline() # metodo para ubicarse en la primera linea de los bist
    xy = dibujo.readline() # ubicarnos en la segunda linea
    x = int(xy.split()[0])  # split  devuelve una lista de los elementos de la variable solo 2 elemetos
    y = int(xy.split()[1])
    icono = bytearray(dibujo.read())  # guardar en matriz de bites
    dibujo.close()
    return framebuf.FrameBuffer(icono, x, y, framebuf.MONO_HLSB)

display.blit(buscar_icono("Images/Prueba.pbm"), 0, 0) # ruta y sitio de ubicación
display.show()  #mostrar
time.sleep(5)


#Funcion para armar el Border de la pantalla.
def border(width, height):
    display.hline(0, 0, width - 1, 1) # top edge
    display.hline(0, height - 2, width - 1, 1) # bottom edge
    display.vline(0, 0, height - 1, 1) # left edge
    display.vline(width - 1, 0, height - 1, 1)

#Funcion para la conexion a la Red Wifi.
def conectaWifi (red, password):
    global miRed
    miRed = network.WLAN(network.STA_IF)
    if not miRed.isconnected():              #Si no está conectado…
        miRed.active(True)                   #activa la interface
        miRed.connect(red, password)         #Intenta conectar con la red
        #print('Conectando a la red', red +"…")
        timeout = time.time ()
        while not miRed.isconnected():           #Mientras no se conecte..
            if (time.ticks_diff (time.time (), timeout) > 10):
                return False
    return True



if conectaWifi ("GEORGINA", "*1065652573*"):
    display.show()
    while (True):

        #Ciclo para mostrar datos de lectura en la pantalla, envio de datos por medio de las Api
        while True:
            display.fill(0)
            border(width, height)
            SensorMQ2_value = float(sensor.read())
            display.text(' Sensor MQ2 GAS', 0, 5)
            display.text('   PPM:'+ str(SensorMQ2_value), 0,20)
            respuesta = urequests.get(url+"&field1="+str(SensorMQ2_value))
            respuesta.close ()
            if SensorMQ2_value > 400:
                display.text('     ALERTA', 0,35)
                display.text('   Fuga de Gas', 0,50)
                #Encediendo el Buzzer
                BUZZER.on()
                display.show()
                respuesta = urequests.get(url2+"&value1="+str(SensorMQ2_value))
                respuesta.close ()

            display.show()
            BUZZER.off()
            time.sleep (0.25)

else:
    miRed.active (False)



