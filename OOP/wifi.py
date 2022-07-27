import network, time
from utime import sleep

class Connection():
    def __init__(self,red,password):
        self.password = password
        self.red = red
    
    def connectionWifi(self):
        global miRed
        miRed = network.WLAN(network.STA_IF)     
        if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)
          miRed.connect(self.red, self.password)    #activa la interface
          print('Conectando a la red', self.red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
        return True,miRed
        