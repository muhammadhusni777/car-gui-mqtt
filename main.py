######  PROGRAM MEMANGGIL WINDOWS PYQT5 ##########################

####### memanggil library PyQt5 ##################################
#----------------------------------------------------------------#
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtQml import * 
from PyQt5.QtWidgets import *
from PyQt5.QtQuick import *  
import sys
import paho.mqtt.client as paho

#broker="127.0.0.1"
broker="broker.emqx.io"
port = 1883
topic_test = ""
#----------------------------------------------------------------#
potensiometer = 0
temperature = 0
humidity = 0

parking_sensor = ""

########## mengisi class table dengan instruksi pyqt5#############
#----------------------------------------------------------------#
class table(QObject):    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.app = QApplication(sys.argv)
        self.engine = QQmlApplicationEngine(self)
        self.engine.rootContext().setContextProperty("backend", self)    
        self.engine.load(QUrl("main.qml"))
        sys.exit(self.app.exec_())
        
    @pyqtSlot(result=str)
    def battery(self):  return str(round(potensiometer,0))
    
    @pyqtSlot(result=str)
    def temperature(self):  return str(round(temperature,0))
    
    @pyqtSlot(result=str)
    def humidity(self):  return str(round(humidity,0))
    
    @pyqtSlot(result=str)
    def infrared(self):  return str(parking_sensor)
    
    
#----------------------------------------------------------------#

#----------------------------------------------------------------#


def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    t = str(message.topic)

    if(msg[0] == 'c'):
        val =  1
    else:
        val = (msg)
    
    if (t == "trainer_iot_upi_01/potensiometer"):
        global potensiometer
        potensiometer = float(msg)/4096 * 100
        #print(potensiometer)

    if (t == "trainer_iot_upi_01/temperature"):
        global temperature
        temperature = float(msg)
        
    if (t == "trainer_iot_upi_01/humidity"):
        global humidity
        humidity = float(msg)
        
    if (t == "trainer_iot_upi_01/infrared"):
        global parking_sensor
        parking_sensor = (msg)

########## memanggil class table di mainloop######################
#----------------------------------------------------------------#    
if __name__ == "__main__":
    
    client= paho.Client("GUI")
    client.on_message=on_message

    print("connecting to broker ",broker)
    client.connect(broker,port)#connect
    print(broker," connected")
    
    client.loop_start()
    print("Subscribing")

    client.subscribe("trainer_iot_upi_01/potensiometer")
    client.subscribe("trainer_iot_upi_01/temperature")
    client.subscribe("trainer_iot_upi_01/humidity")
    client.subscribe("trainer_iot_upi_01/infrared")

    
    
    main = table()
    
    
#----------------------------------------------------------------#