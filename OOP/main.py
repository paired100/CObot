import wifi
import sensores
#from wifi import Connection
con = wifi.Connection("Manitas","Splunk5*")
print(con)
if con.connectionWifi():
    
    print ("Conexión exitosa!")
    while True:
        sensor = sensores.Sensor()
        activate = sensor.sensorMQ2()
    #    activate = runSensor()
    #    thingSpeak(activate)
        if activate >= 350:
            print("En mq2")
    #        buzzer.freq(1047)
    #        buzzer.duty(50)
    #        oled.fill(0)
    #        oled.text("Alerta Incendio: ",0,10)
    #        oled.text(str(activate),0,20)
    #        oled.show()
    #        ledGreen.value(1)
    #        ledRed.value(0) 
    #        notification("C0bot_email",activate)
    #        notification("C0bot_telegram",activate)
    #        notification("C0bot_Alert",activate)
    #        notification("C0BotNotifier",activate)
    #        writeSheet("Alerta..de...incendio..presentada!!!")
    #             
        else:
            print("fuera mq2")
    #        writeSheet("Nivel..de..gas..normal")
    #        buzzer.duty(0)
    #        oled.fill(0)
    #        oled.text("Nivel de gas: ",0,10)
    #        oled.text(str(activate),0,20)
    #        oled.show()
    #        ledGreen.value(0)
    #        ledRed.value(1)   
    #        
else:
    print ("Imposible conectar")
#       miRed.active (False)
