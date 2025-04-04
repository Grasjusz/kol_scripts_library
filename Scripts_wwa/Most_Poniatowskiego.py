import jarray
import jmri
import sys


# Dodaj ścieżkę do katalogu, w którym znajduje się biblioteka Kollib.py
sys.path.append(r'C:\Users\LOK_7\JMRI\My_JMRI_Railroad.jmri\MyScrypt')
import Kollib #Biblioteka autorskich funkcji

#Sekwencyjne przypisywanie adresów sensorą
FirstSensorAdress = 1
NumberOfSensors = 32
SensorsList = []
SensorsList.append(0)
for i in range(FirstSensorAdress, FirstSensorAdress + NumberOfSensors):
    SensorsList.append(sensors.getSensor("LS"+str(i)))

print(SensorsList)
"""for i in range(1,NumberOfSensors+1):
    SensorsList[i].setState(4)"""
sensor_start = sensors.getSensor("IS333")

FirstTurnoutAdress = 70
# Liczba zwrotnic do przypisania
NumberOfTurnouts = 4
# Lista przechowująca obiekty zwrotnic
TurnoutsList = []
# Pętla iteruje przez kolejne wartości adresów zwrotnic i tworzy ich listę
TurnoutsList.append(0)
for i in range(FirstTurnoutAdress, FirstTurnoutAdress + NumberOfTurnouts):
    TurnoutsList.append(turnouts.getTurnout("LT" + str(i)))  # Tworzenie adresu zwrotnicy np. LT1, LT2...
print(TurnoutsList)  # Drukowanie listy zwrotnic do sprawdzenia



'''
Jeśli czujniki nie są ułożone w sekwencji, możesz dodać je jako Sensor1 = sensors.getSensor("LS1") lub
SensorsList.append(sensors.getSensor("LS" + str(1))), jeśli chcesz umieścić je w liście.

Jeśli to możliwe, dopisz taki sam algorytm dla innych elementów.

Jeśli dany sensor nie znajduje się na liście sensorów w panelu "PanelPro" 
(jego wartość to None), skutkuje to wyłaczeniem watku w którym znajduje sie fukcja
odnoszaca sie do tego czujnika.
'''


"""class Tramwaje(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration.
        print "Inside init(self)"

        # get loco address. For long address change "False" to "True"
        self.tramwaj_1= self.getThrottle(6, False)
        self.tramwaj_2= self.getThrottle(8, False)
        return

    def handle(self):
        # handle() is called repeatedly until it returns false.
        print "Inside handle(self)"
        print "Sensor 29:",SensorsList[29].getKnownState(),"Sensor 30:", SensorsList[30].getKnownState()
        print "Sensor 17:",SensorsList[17].getKnownState(),"Sensor 18:", SensorsList[18].getKnownState()

        if SensorsList[29].getKnownState() != 2 and SensorsList[30].getKnownState() != 2:
            Kollib.drive_vehicle(self, self.tramwaj_1, 0.3, False)
            Kollib.stop_at_station(self, self.tramwaj_1, SensorsList[29], 5000)
            print "tramwaj_1 na stacji"
            self.tramwaj_1.setF1(True)
        else:
            self.tramwaj_1.setSpeedSetting(0)
            print "tramwaj_1 na stacji"
            self.tramwaj_1.setF1(True)

        if  SensorsList[18].getKnownState() != 2:
            Kollib.drive_vehicle(self, self.tramwaj_2, 0.45, False)
            Kollib.stop_at_station(self, self.tramwaj_2, SensorsList[18], 5000)
            print "tramwaj_2 na stacji"
            self.tramwaj_2.setF1(True)
        else:
            self.tramwaj_2.setSpeedSetting(0)
            print "tramwaj_2 na stacji"
            self.tramwaj_2.setF1(True)

        Kollib.drive_vehicle(self, self.tramwaj_1, 0.3,True)
        self.waitMsec(2000)



        self.waitSensorActive([SensorsList[27]])
        Kollib.drive_vehicle(self, self.tramwaj_2, 0.3, True)
        self.waitMsec(1500)



        Kollib.stop_at_station(self, self.tramwaj_1, SensorsList[26], 0)
        self.tramwaj_1.setF4(True)
        self.waitMsec(500)
        self.tramwaj_1.setF4(False)
        Kollib.speed_change(self,self.tramwaj_2,2)


        Kollib.stop_at_station(self,self.tramwaj_2,SensorsList[23],1000)


        Kollib.drive_vehicle(self, self.tramwaj_1, 0.3,False)
        self.waitMsec(2000)
        Kollib.speed_change(self,self.tramwaj_1,1)


        self.waitSensorActive([SensorsList[28]])
        Kollib.drive_vehicle(self, self.tramwaj_2, 0.3,False)
        self.waitMsec(2000)
        Kollib.speed_change(self,self.tramwaj_2,2)


        Kollib.stop_at_station(self,self.tramwaj_1,SensorsList[30],100)
        self.tramwaj_1.setF4(True)
        self.waitMsec(1000)
        self.tramwaj_1.setF4(False)



        self.waitSensorActive([SensorsList[19]])
        self.waitMsec(13000)
        Kollib.speed_change(self,self.tramwaj_2,0.5)
        Kollib.stop_at_station(self,self.tramwaj_2,SensorsList[18],1000)



        return 1"""

class Kolej(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration.
        print "Inside init(self)"

        # get loco address. For long address change "False" to "True"
        self.lokomotywa_1= self.getThrottle(3, False)
        return

    def handle(self):
        # handle() is called repeatedly until it returns false.
        print "Wait for sensor start"
        self.waitSensorActive([sensor_start])
        if SensorsList[1].getKnownState() != 2 and SensorsList[2].getKnownState() != 2:
            Kollib.drive_vehicle(self, self.lokomotywa_1, 0.45, True)
            Kollib.stop_at_station(self, self.lokomotywa_1, SensorsList[1], 1000)
            Kollib.drive_vehicle(self, self.lokomotywa_1, 0.45, False)
            Kollib.delay_stop(self, self.lokomotywa_1, SensorsList[8], 1000)

        else:
                Kollib.drive_vehicle(self, self.lokomotywa_1, 0.45, False)
                Kollib.delay_stop(self, self.lokomotywa_1, SensorsList[8], 1000)


        self.waitSensorActive([SensorsList[8]])
        self.lokomotywa_1.setSpeedSetting(0)
        Kollib.drive_vehicle(self, self.lokomotywa_1, 0.45,True)
        Kollib.stop_at_station(self, self.lokomotywa_1, SensorsList[1], 1000)
        Kollib.drive_vehicle(self, self.lokomotywa_1, 0.45,False)
        Kollib.delay_stop(self, self.lokomotywa_1, SensorsList[8], 1000)
        Kollib.drive_vehicle(self, self.lokomotywa_1, 0.45, True)
        Kollib.stop_at_station(self, self.lokomotywa_1, SensorsList[1], 1000)



#Tramwaje().start()
Kolej().start()
