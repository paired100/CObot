import network, time, urequests
from machine import Pin , I2C, ADC
from ssd1306 import SSD1306_I2C
from utime import sleep
import machine

ledRed = Pin(14, Pin.OUT)
ledGreen = Pin(13, Pin.OUT)

 
ancho = 128
alto = 64
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(ancho, alto, i2c)
scannerOled = (len(i2c.scan()))
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


def runSensor():
    sensorName = ADC(Pin(35))
    sensorName.width(ADC.WIDTH_10BIT)
    sensorName.atten(ADC.ATTN_11DB)
    sleep(4)
    lectura = sensorName.read()
    print ( "Nivel de gas =  {} % ".format(lectura))

    return lectura

def notification(triggerName,activate):
    uri = "https://maker.ifttt.com/trigger/"+triggerName+"/with/key/c1dUFR3XfCXdNVvwslnU7R?" 
    response = urequests.get(uri+"&value1="+str(activate))
    print(response.text)
    print(response.status_code)
    response.close ()
    
def thingSpeak(activate):
    url = "https://api.thingspeak.com/update?api_key=9VC4A7TEJ3GD1K9L"
    respuesta = urequests.get(url+"&field1="+str(activate))
    print(respuesta.status_code)
    respuesta.close ()
    

def writeSheet(message):
    uri = "https://maker.ifttt.com/trigger/cobotWrite/with/key/c1dUFR3XfCXdNVvwslnU7R?"
    response = urequests.get(uri+"&value1="+"Nivel de gas"+"&value2="+str(activate)+"&value3="+str(message))
    print(response.text)
    print(response.status_code)
           

def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect(red, password)         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True

    
port = machine.Pin(15, machine.Pin.OUT)
buzzer = machine.PWM(port)
if conectaWifi ("Manitas", "Splunk5*"):

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    while True:
        activate = runSensor()
        thingSpeak(activate)

        if activate >= 350:
            buzzer.freq(1047)
            buzzer.duty(50)
            oled.fill(0)
            oled.text("Alerta Incendio: ",0,10)
            oled.text(str(activate),0,20)
            oled.show()
            ledGreen.value(1)
            ledRed.value(0) 
            notification("C0bot_email",activate)
            notification("C0bot_telegram",activate)
            notification("C0bot_Alert",activate)
            notification("C0BotNotifier",activate)
            writeSheet("Alerta..de...incendio..presentada!!!")
                 
        else:
            writeSheet("Nivel..de..gas..normal")
            buzzer.duty(0)
            oled.fill(0)
            oled.text("Nivel de gas: ",0,10)
            oled.text(str(activate),0,20)
            oled.show()
            ledGreen.value(0)
            ledRed.value(1)   
            
else:
       print ("Imposible conectar")
       miRed.active (False)
