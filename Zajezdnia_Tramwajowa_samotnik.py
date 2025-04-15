from json.decoder import WHITESPACE_STR

import jarray
import jmri
import sys


# Dodaj ścieżkę do katalogu, w którym znajduje się biblioteka Kollib.py
sys.path.append(r'C:\Users\LOK_7\JMRI\My_JMRI_Railroad.jmri\MyScrypt')
import Kollib #Biblioteka autorskich funkcji

#Sekwencyjne przypisywanie adresów sensorą
FirstSensorAdress = 33
NumberOfSensors = 16
SensorsListZA = []
SensorsListZA.append(0)
for i in range(FirstSensorAdress, FirstSensorAdress + NumberOfSensors):
    SensorsListZA.append(sensors.getSensor("LS"+str(i)))

print(SensorsListZA)
StartSignal=sensors.getSensor("IS333")
NA_STACJI_ZAJEZDNIA = sensors.getSensor("IS336")


for i in range(1, NumberOfSensors + 1):
    if SensorsListZA[i] != None:
        SensorsListZA[i].setKnownState(4)

FirstTurnoutAdress = 70
# Liczba zwrotnic do przypisania
NumberOfTurnouts = 4
# Lista przechowująca obiekty zwrotnic
TurnoutsListZA = []
# Pętla iteruje przez kolejne wartości adresów zwrotnic i tworzy ich listę
TurnoutsListZA.append(0)
for i in range(FirstTurnoutAdress, FirstTurnoutAdress + NumberOfTurnouts):
    TurnoutsListZA.append(turnouts.getTurnout("LT" + str(i)))  # Tworzenie adresu zwrotnicy np. LT1, LT2...
print(TurnoutsListZA)  # Drukowanie listy zwrotnic do sprawdzenia



'''
Jeśli czujniki nie są ułożone w sekwencji, możesz dodać je jako Sensor1 = sensors.getSensor("LS1") lub
SensorsListZA.append(sensors.getSensor("LS" + str(1))), jeśli chcesz umieścić je w liście.

Jeśli to możliwe, dopisz taki sam algorytm dla innych elementów.

Jeśli dany sensor nie znajduje się na liście sensorów w panelu "PanelPro" 
(jego wartość to None), skutkuje to wyłaczeniem watku w którym znajduje sie fukcja
odnoszaca sie do tego czujnika.
'''


class TramwajeZA(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration.
        print("Inside init(self)")

        # get loco address. For long address change "False" to "True"
        self.tramwaj_3= self.getThrottle(5, False)
        return

    def handle(self):
        print("Inside handle(self)")
        self.tramwaj_3.setF3(True)
        if StartSignal.getKnownState() != 2:
            self.tramwaj_3.setSpeedSetting(0)
            self.tramwaj_3.setF0(False)
            self.tramwaj_3.setF6(False)
            self.tramwaj_3.setF3(True)
            NA_STACJI_MOST.setKnownState(2)
            if NA_STACJI_ZAJEZDNIA.getKnownState() == 2 and NA_STACJI_MOST.getKnownState() == 2 and NA_STACJI_ZAJEZDNIA.getKnownState() == 2:
                sensors.getSensor("IS332").setKnownState(2)
        print("Wait for sensor start",self, "START_SIGNAL state:", START_SIGNAL.getKnownState())
        self.waitSensorActive([StartSignal])


        self.tramwaj_3.setSpeedSetting(0)
        Kollib.funkcja_tramwaj_odjazd(self,self.tramwaj_3)
        Kollib.drive_vehicle(self, self.tramwaj_3, 0.6, True)
        self.waitSensorActive([SensorsListZA[11]])
        self.tramwaj_3.setSpeedSetting(0.45)

        Kollib.delay_stop(self,self.tramwaj_3,SensorsListZA[12],3500)
        self.waitMsec(3000)
        self.tramwaj_3.setF3(False)
        self.waitMsec(3000)

        Kollib.funkcja_tramwaj_odjazd(self,self.tramwaj_3)
        self.waitMsec(500)
        self.tramwaj_3.setF3(True)
        Kollib.drive_vehicle(self, self.tramwaj_3, 0.45,False)
        self.waitSensorActive([SensorsListZA[11]])
        self.tramwaj_3.setSpeedSetting(0.6)
        self.waitMsec(9000)
        self.tramwaj_3.setSpeedSetting(0.45)

        Kollib.delay_stop(self, self.tramwaj_3, SensorsListZA[10], 1000)





        return 1
TramwajeZA().start()
