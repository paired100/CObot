import network, time, urequests
from machine import Pin , I2C, ADC
from ssd1306 import SSD1306_I2C
from utime import sleep


led = Pin(2, Pin.OUT)

def initOled():
    ancho = 128
    alto = 64
    i2c = I2C(0, scl=Pin(22), sda=Pin(21))
    oled = SSD1306_I2C(ancho, alto, i2c)
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
        



def runSensor():
    sensorName = ADC(Pin(35))
    sensorName.width(ADC.WIDTH_10BIT)
    sensorName.atten(ADC.ATTN_11DB)
    sleep(4)
    lectura = sensorName.read()
    if lectura > 0:
        print ( "Nivel de gas =  {} % ".format(lectura))
    return lectura



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


def notification(triggerName,activate):
    uri = "https://maker.ifttt.com/trigger/"+triggerName+"/with/key/c1dUFR3XfCXdNVvwslnU7R?" 
    response = urequests.get(uri+"&value1="+str(activate))
    print(response.text)
    print(response.status_code)
    response.close ()
    

if conectaWifi ("Manitas", "Splunk5*"):

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
      
    while True:
        activate = runSensor()
        if activate >= 150:
            notification("C0bot_email",activate)
            led.value(1)
            
        else:
            led.value(0)
        
 
else:
       print ("Imposible conectar")
       miRed.active (False)
