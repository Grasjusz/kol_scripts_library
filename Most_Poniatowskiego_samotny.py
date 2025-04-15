from math import trunc

import jarray
import jmri
import sys

# Dodaj ścieżkę do katalogu, w którym znajduje się biblioteka Kollib.py
sys.path.append(r'C:\Users\LOK_7\JMRI\My_JMRI_Railroad.jmri\MyScrypt')
import Kollib  # Biblioteka autorskich funkcji

# Sekwencyjne przypisywanie adresów sensorą
FirstSensorAdress = 1
NumberOfSensors = 32
SensorsList = []
SensorsList.append(0)
for i in range(FirstSensorAdress, FirstSensorAdress + NumberOfSensors):
    SensorsList.append(sensors.getSensor("LS" + str(i)))
print(SensorsList)

START_SIGNAL = sensors.getSensor("IS333")
START_SIGNAL.setKnownState(4)
NA_STACJI_MOST = sensors.getSensor("IS334")
NA_STACJI_KOLEJ = sensors.getSensor("IS335")

FirstTurnoutAdress = 1
NumberOfTurnouts = 1
TurnoutsList = []
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


class Tramwaje(jmri.jmrit.automat.AbstractAutomaton):
    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration.
        print("Inside init(self)")
        # get loco address. For long address change "False" to "True"
        self.tramwaj_2 = self.getThrottle(11, False)
        self.i =True
        return

    def handle(self):
        # handle() is called repeatedly until it returns false.
        print("Inside handle(self)")
        self.tramwaj_2.setSpeedSetting(0)

        print("Wait for sensor start",self, "START_SIGNAL state:", START_SIGNAL.getKnownState())
        if START_SIGNAL.getKnownState() != 2:
            self.tramwaj_2.setSpeedSetting(0)
            self.tramwaj_2.setF0(False)
            self.tramwaj_2.setF1(False)
            self.tramwaj_2.setF3(True)
            NA_STACJI_MOST.setKnownState(2)
            if NA_STACJI_KOLEJ.getKnownState() == 2 and NA_STACJI_MOST.getKnownState() == 2:
                sensors.getSensor("IS332").setKnownState(2)


        self.waitSensorActive([START_SIGNAL])
        NA_STACJI_MOST.setKnownState(4)
        self.tramwaj_2.setF1(True)
        self.tramwaj_2.setF3(False)
        while self.i:
            print("Sensor 21:", SensorsList[21].getKnownState(), "Sensor 22:", SensorsList[22].getKnownState())
            if SensorsList[21].getKnownState() != 2 and SensorsList[22].getKnownState() != 2:
                Kollib.funkcja_tramwaj_odjazd(self, self.tramwaj_2)
                Kollib.drive_vehicle(self, self.tramwaj_2, 0.30, True)
                Kollib.stop_at_station(self, self.tramwaj_2, SensorsList[21], 5000)
                self.tramwaj_2.setF3(False)
                self.waitMsec(3000)
                print("tramwaj_2 na stacji")
                self.i = False

            else:
                self.tramwaj_2.setSpeedSetting(0)
                print("tramwaj_2 na stacji")
                self.i = False
        self.tramwaj_2.setSpeedSetting(0)
        self.waitSensorActive([SensorsList[21]])
        self.tramwaj_2.setSpeedSetting(0)

        Kollib.funkcja_tramwaj_odjazd(self,self.tramwaj_2)
        Kollib.drive_vehicle(self, self.tramwaj_2, 0.35, False)
        Kollib.stop_at_station(self, self.tramwaj_2, SensorsList[18], 3000)
        self.tramwaj_2.setSpeedSetting(0)
        self.tramwaj_2.setF3(False)
        self.waitMsec(5000)

        Kollib.funkcja_tramwaj_odjazd(self, self.tramwaj_2)
        Kollib.drive_vehicle(self, self.tramwaj_2, 0.35, True)
        Kollib.stop_at_station(self, self.tramwaj_2, SensorsList[21], 3000)
        self.tramwaj_2.setSpeedSetting(0)
        self.tramwaj_2.setF3(False)
        self.waitMsec(5000)
        return 1


class Kolej(jmri.jmrit.automat.AbstractAutomaton):
    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration.
        print("Inside init(self)")
        # get loco address. For long address change "False" to "True"
        self.lokomotywa_1 = self.getThrottle(128, True)
        self.i = True
        return

    def handle(self):
        # handle() is called repeatedly until it returns false.
        print("Wait for sensor start",self,"START_SIGNAL state:", START_SIGNAL.getKnownState())
        if START_SIGNAL.getKnownState() != 2:
            self.lokomotywa_1.setSpeedSetting(0)
            self.lokomotywa_1.setF0(False)
            self.lokomotywa_1.setF6(False)
            NA_STACJI_KOLEJ.setKnownState(2)
            if NA_STACJI_KOLEJ.getKnownState() == 2 and NA_STACJI_MOST.getKnownState() == 2 and NA_STACJI_ZAJEZDNIA.getKnownState() == 2:
                sensors.getSensor("IS332").setKnownState(2)
        self.waitSensorActive([START_SIGNAL])
        while self.i:
            if SensorsList[8].getKnownState() != 2:
                self.lokomotywa_1.setSpeedSetting(0)
                Kollib.drive_vehicle(self,self.lokomotywa_1,0.45,False)
                Kollib.stop_at_station(self,self.lokomotywa_1,SensorsList[8],3000)
                self.lokomotywa_1.setF0(True)
                self.lokomotywa_1.setF6(True)
                self.i=False
            elif SensorsList[8].getKnownState() == 1:
                print("UWAGA!")
            else:
                self.lokomotywa_1.setSpeedSetting(0)
                self.lokomotywa_1.setF0(True)
                self.lokomotywa_1.setF6(True)
                self.i = False


        self.lokomotywa_1.setSpeedSetting(0)
        self.waitSensorActive([SensorsList[8]])
        self.lokomotywa_1.setSpeedSetting(0)


        Kollib.drive_vehicle(self, self.lokomotywa_1, 0.45, True)

        self.waitSensorActive([SensorsList[6]])
        self.lokomotywa_1.setSpeedSetting(0.2)
        self.waitMsec(5000)
        self.lokomotywa_1.setSpeedSetting(0.1)

        Kollib.delay_stop(self, self.lokomotywa_1, SensorsList[2], 10000)
        self.lokomotywa_1.setSpeedSetting(0)
        self.waitMsec(30000)
        self.lokomotywa_1.setIsForward(False)
        self.lokomotywa_1.setIsForward(False)
        self.lokomotywa_1.setF1(True)
        self.waitMsec(100)
        self.lokomotywa_1.setF1(False)


        Kollib.drive_vehicle(self, self.lokomotywa_1, 0.3, False)

        self.waitSensorActive([SensorsList[6]])
        self.lokomotywa_1.setSpeedSetting(0.45)

        self.waitSensorActive([SensorsList[7]])
        self.lokomotywa_1.setSpeedSetting(0.2)

        Kollib.stop_at_station(self, self.lokomotywa_1, SensorsList[8], 3000)
        self.lokomotywa_1.setSpeedSetting(0)
        self.waitMsec(30000)
        self.lokomotywa_1.setIsForward(True)
        self.lokomotywa_1.setIsForward(False)
        self.lokomotywa_1.setF1(True)
        self.waitMsec(100)
        self.lokomotywa_1.setF1(False)


        return 1


Tramwaje().start()
Kolej().start()