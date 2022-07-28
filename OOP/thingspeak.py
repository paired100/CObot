import urequests
from utime import sleep

class Telemetry():
    def __init__(self,activate):
        self.activate = activate
    
    
    def thingSpeak(self):
        url = "https://api.thingspeak.com/update?api_key=9VC4A7TEJ3GD1K9L"
        respuesta = urequests.get(url+"&field1="+str(self.activate))
        print(respuesta.status_code)
        respuesta.close ()
        
        