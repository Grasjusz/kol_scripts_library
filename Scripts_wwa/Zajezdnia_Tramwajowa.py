from _ast import While

import jarray
import jmri
import sys


# Dodaj ścieżkę do katalogu, w którym znajduje się biblioteka Kollib.py
sys.path.append(r'C:\Users\LOK_7\JMRI\My_JMRI_Railroad.jmri\MyScrypt')
import Kollib #Biblioteka autorskich funkcji

#Sekwencyjne przypisywanie adresów sensorą
FirstSensorAdress = 33
NumberOfSensors = 16
SensorsList = []
SensorsList.append(0)
for i in range(FirstSensorAdress, FirstSensorAdress + NumberOfSensors):
    SensorsList.append(sensors.getSensor("LS"+str(i)))

print(SensorsList)

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


class Tramwaje(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration.
        print "Inside init(self)"

        # get loco address. For long address change "False" to "True"
        self.tramwaj_1= self.getThrottle(7, False)
        self.tramwaj_2= self.getThrottle(5, False)
        return

    def handle(self):
        # handle() is called repeatedly until it returns false.
        print "Inside handle(self)"
        print "Sensor 5:",SensorsList[5].getKnownState()
        print "Sensor 7:",SensorsList[7].getKnownState()

        for i in range(1,NumberOfTurnouts+1):
            TurnoutsList[i].setState(2)
            print "zwrotnica",i,"stan:",TurnoutsList[i].getKnownState()

        for i in range(1,NumberOfSensors+1):
            SensorsList[i].setState(4)

        print "Sensor 5:", SensorsList[5].getKnownState()
        print "Sensor 7:", SensorsList[7].getKnownState()
        self.tramwaj_1.setF1(False)

        while True:
            if SensorsList[5].getKnownState() != 2:

                print "Umiesc tramwaj_1 w zajezdni tor nr.3!"
                #self.tramwaj_1.setF4(True)
                self.waitMsec(500)
                #self.tramwaj_1.setF4(False)
                self.waitMsec(500)
            else:
                self.tramwaj_1.setSpeedSetting(0)
                print "tramwaj_1 na stacji"
                self.tramwaj_1.setF1(True)
                break

        if SensorsList[7].getKnownState() != 2:
            Kollib.drive_vehicle(self, self.tramwaj_2, 0.3, False)
            Kollib.stop_at_station(self, self.tramwaj_2, SensorsList[7], 2000)
            print "tramwaj_2 na stacji"
            self.tramwaj_2.setF1(True)
        else:
            self.tramwaj_2.setSpeedSetting(0)
            print "tramwaj_2 na stacji"
            self.tramwaj_2.setF1(True)

        Kollib.drive_vehicle(self, self.tramwaj_1, 0.5,True)
        self.waitSensorActive([SensorsList[8]])


        Kollib.drive_vehicle(self, self.tramwaj_2, 0.5, True)
        Kollib.delay_stop(self,self.tramwaj_2,SensorsList[13],12000)
        self.tramwaj_2.setF2(True)
        self.waitMsec(300)
        self.tramwaj_2.setF2(False)
        self.waitMsec(300)


        Kollib.speed_change(self,self.tramwaj_1,0.5)
        Kollib.delay_stop(self,self.tramwaj_1,SensorsList[10],4500)
        self.tramwaj_1.setF4(True)
        self.waitMsec(300)
        self.tramwaj_1.setF4(False)
        self.waitMsec(300)

        Kollib.drive_vehicle(self, self.tramwaj_2,0.5, False)
        Kollib.drive_vehicle(self, self.tramwaj_1, 0.5,True)
        Kollib.stop_at_station(self, self.tramwaj_2, SensorsList[7], 0)
        self.tramwaj_2.setF4(True)
        self.waitMsec(300)
        self.tramwaj_2.setF4(False)
        Kollib.delay_stop(self,self.tramwaj_1,SensorsList[12],1000)
        self.tramwaj_1.setF4(True)
        self.waitMsec(300)
        self.tramwaj_1.setF4(False)
        self.waitMsec(700)

        Kollib.drive_vehicle(self, self.tramwaj_1, 0.5,False)
        Kollib.drive_vehicle(self, self.tramwaj_2, 0.5,True)
        Kollib.delay_stop(self,self.tramwaj_2,SensorsList[13],12000)
        self.tramwaj_2.setF4(True)
        self.waitMsec(300)
        self.tramwaj_2.setF4(False)
        Kollib.stop_at_station(self, self.tramwaj_1, SensorsList[10], 0)
        self.tramwaj_1.setF4(True)
        self.waitMsec(300)
        self.tramwaj_1.setF4(False)
        self.waitMsec(700)
        TurnoutsList[1].setState(4)

        Kollib.drive_vehicle(self, self.tramwaj_1, 0.5,False)
        self.waitSensorActive([SensorsList[9]])
        Kollib.drive_vehicle(self, self.tramwaj_2, 0.5,False)
        while True:
            if SensorsList[6].getKnownState() == 2:
                Kollib.stop_at_station(self, self.tramwaj_1, SensorsList[6], 0)
                Kollib.stop_at_station(self,self.tramwaj_2,SensorsList[7],0)
                break
            elif SensorsList[7].getKnownState() == 2:
                Kollib.stop_at_station(self, self.tramwaj_2, SensorsList[7], 0)
                Kollib.stop_at_station(self,self.tramwaj_1,SensorsList[6],0)
                break

        Kollib.drive_vehicle(self, self.tramwaj_1, 0.5,False)
        Kollib.stop_at_station(self, self.tramwaj_1, SensorsList[1], 0)
        self.tramwaj_1.setF4(True)
        self.waitMsec(300)
        self.tramwaj_1.setF4(False)
        self.waitMsec(700)


        TurnoutsList[4].setState(4)
        Kollib.drive_vehicle(self, self.tramwaj_1, 0.5,True)
        Kollib.delay_stop(self, self.tramwaj_1, SensorsList[4], 1000)
        Kollib.drive_vehicle(self, self.tramwaj_1, 0.3,True)
        Kollib.drive_vehicle(self, self.tramwaj_2, 0.5,True)

        Kollib.delay_stop(self,self.tramwaj_2,SensorsList[13],12000)
        self.tramwaj_2.setF2(True)
        self.waitMsec(300)
        self.tramwaj_2.setF2(False)
        self.waitMsec(300)

        Kollib.delay_stop(self,self.tramwaj_1,SensorsList[10],0)
        self.tramwaj_1.setF4(True)
        self.waitMsec(300)
        self.tramwaj_1.setF4(False)
        self.waitMsec(700)


        Kollib.drive_vehicle(self, self.tramwaj_1, 0.5,True)
        Kollib.drive_vehicle(self, self.tramwaj_2, 0.5,False)

        while True:
            if SensorsList[12].getKnownState() == 2:
                Kollib.stop_at_station(self, self.tramwaj_1, SensorsList[12], 0)
                Kollib.stop_at_station(self, self.tramwaj_2, SensorsList[7], 0)
                break
            elif SensorsList[7].getKnownState() == 2:
                Kollib.stop_at_station(self, self.tramwaj_2, SensorsList[7], 0)
                Kollib.stop_at_station(self, self.tramwaj_1, SensorsList[12], 0)
                break

        Kollib.drive_vehicle(self, self.tramwaj_1, 0.5,False)
        TurnoutsList[1].setState(2)
        TurnoutsList[2].setState(2)
        Kollib.stop_at_station(self, self.tramwaj_1, SensorsList[5], 1000)



        return 1
Tramwaje().start()
