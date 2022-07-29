import lib.wifi
import lib.sensores
import lib.notification
import lib.thingspeak
import lib.writesheet
import lib.rgb
import machine
from machine import Pin , I2C, ADC
from ssd1306 import SSD1306_I2C
from utime import sleep

con = wifi.Connection("Manitas","Splunk5*")
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



port = machine.Pin(15, machine.Pin.OUT)
buzzer = machine.PWM(port)
if con.connectionWifi():
    sensor = sensores.Sensor()    
    activate = sensor.sensorMQ2()
    print ("Conexión exitosa!")
    #oledStart = oled.Oled(activate)
    #oledOn = oledStart.OledOn()
    while True:
        #sensor = sensores.Sensor()
        #activate = sensor.sensorMQ2()
        startRGB = rgb.Rgb(activate)
        rgbF = startRGB.startRGB()

        
    #    activate = runSensor()
    #    thingSpeak(activate)
        if activate >= 350:
            print("En mq2")
            buzzer.freq(1047)
            buzzer.duty(50)
            oled.fill(0)
            oled.text("Alerta Incendio: ",0,10)
            oled.text(str(activate),0,20)
            oled.show()
            email = notification.Notification("C0bot_email",activate)
            alertEmail = email.notification()
            telegram = notification.Notification("C0bot_telegram",activate)
            alertTelegram = telegram.notification()
            sms = notification.Notification("C0bot_Alert",activate)
            alertSms = sms.notification()
            cellPhone = notification.Notification("C0BotNotifier",activate)
            alertCellphone = cellPhone.notification()
            
            thing = thingspeak.Telemetry(activate)
            thingSpeakCall = thing.thingSpeak()
            
            write = writesheet.WriteSheet(activate,"Alerta..de...incendio..presentada!!!")
            writeSheet = write.writeSheet()
            
            
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
            write = writesheet.WriteSheet(activate,"Nivel..de..gas..normal!!!")
            writeSheet = write.writeSheet()
            oled.fill(0)
            oled.text("Nivel de gas: ",0,10)
            oled.text(str(activate),0,20)
            oled.show()
            buzzer.duty(0)
    #        ledGreen.value(0)
    #        ledRed.value(1)   
    #        
else:
    print ("Imposible conectar")
#       miRed.active (False)
