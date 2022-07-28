import urequests


class WriteSheet():
    def __init__(self,activate,message):
        self.message = message
        self.activate = activate
        
    
    def writeSheet(self):
        uri = "https://maker.ifttt.com/trigger/cobotWrite/with/key/c1dUFR3XfCXdNVvwslnU7R?"
        response = urequests.get(uri+"&value1="+"Nivel de gas"+"&value2="+str(self.activate)+"&value3="+str(self.message))
        print(response.text)
        print(response.status_code)
        
        