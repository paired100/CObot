import urequests


class Notification():
    def __init__(self,triggerName,activate):
        self.triggerName = triggerName
        self.activate = activate
    
    def notification(self):
        uri = "https://maker.ifttt.com/trigger/"+self.triggerName+"/with/key/c1dUFR3XfCXdNVvwslnU7R?" 
        response = urequests.get(uri+"&value1="+str(self.activate))
        print(response.text)
        print(response.status_code)
        response.close ()
        