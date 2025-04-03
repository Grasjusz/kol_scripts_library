import jarray
import jmri
import sys, os
#Pobiera relatywną ścieżkę do skryptu (czyli przeszukuje katalog główny w ktorym jest uruchamiany skrypt)
sys.path.append(os.path.join(sys.path[0]))
from Scripts_wwa.KOMP_1 import Kollib

#Sekwencyjne przypisywanie adresów sensorą 
FirstSensorAdress = 9 #Wpisz numer pierwszego czujnika danej sekcji
NumberOfSensors = 25 #wpisz ilość czujników (-1 pierwszy wpisany wyżej)
SensorsList = []
for i in range(FirstSensorAdress, FirstSensorAdress + NumberOfSensors):
    SensorsList.append(sensors.getSensor("LS"+str(i-1)))
print(SensorsList)



'''
Jeśli czujniki nie są ułożone w sekwencji, możesz dodać je jako Sensor1 = sensors.getSensor("LS1") lub
SensorsList.append(sensors.getSensor("LS" + str(1))), jeśli chcesz umieścić je w liście.

Jeśli to możliwe, dopisz taki sam algorytm dla innych elementów.

Jeśli dany sensor nie znajduje się na liście sensorów w panelu "PanelPro" 
(jego wartość to None), skutkuje to wyłaczeniem watku w którym znajduje sie fukcja
odnoszaca sie do tego czujnika.
'''


def init(self):
    # init() is called exactly once at the beginning to do
    # any necessary configuration.
    print ("Inside init(self)")
    # get loco address. For long address change "False" to "True"
    self.throttle = self.getThrottle(3, False)  # short address 14
    return

def handle(self):
    # handle() is called repeatedly until it returns false.
    print ("Inside handle(self)")
    self.throttle.setSpeedSetting(0)# Upewnia sie że kolejka jest zatszymana
    self.throttle.setF0(True)
    self.throttle.setF1(True)
    Kollib.drive_vehicle(self, 0.3, True)
    self.waitMsec(1000)
    Kollib.sc_station(self, SensorsList[28], 2)
    self.waitMsec(1000)
    Kollib.sc_station(self, SensorsList[27], 0.5)
    Kollib.stop_at_station(self, SensorsList[26], 5000)
    Kollib.drive_vehicle(self, 0.3, False)
    Kollib.sc_station(self, SensorsList[27], 1.5)
    Kollib.stop_at_station(self, SensorsList[29], 1000)
    Kollib.drive_vehicle(self, 0.4, True)
    Kollib.delay_stop(self, SensorsList[28], 20000)
    Kollib.drive_vehicle(self, 0.3, False)
    Kollib.stop_at_station(self, SensorsList[29], 5000)
    self.throttle.setF1(False)
    print ("End of Loop")
    return 1