import jarray
import jmri
import sys, os

# Dodaj ścieżke do katalogu, w którym znajduje sie biblioteka Kollib.py
sys.path.append(os.path.join(sys.path[0]))
import Kollib #Biblioteka autorskich funkcji

#Sekwencyjne przypisywanie adresów sensorą - trasa tramwaj
FirstSensorAdress = 0
NumberOfSensors = 7
SensorsList1 = []
for i in range(FirstSensorAdress, FirstSensorAdress + NumberOfSensors):
    SensorsList1.append(sensors.getSensor("LS"+str(i+1)))
print("Sensor List 1:", SensorsList1)

'''
Jeśli czujniki nie są ułożone w sekwencji, możesz dodać je jako Sensor1 = sensors.getSensor("LS1") lub
SensorsList.append(sensors.getSensor("LS" + str(1))), jeśli chcesz umieścić je w liście.

Jeśli to możliwe, dopisz taki sam algorytm dla innych elementów.

Jeśli dany sensor nie znajduje sie na liście sensorów w panelu "PanelPro" 
(jego wartość to None), skutkuje to wyłaczeniem watku w którym znajduje sie fukcja
odnoszaca sie do tego czujnika.
'''


class Lok1EndDay(jmri.jmrit.automat.AbstractAutomaton):

    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration.
        print("Inside init(self)")
        # get loco address. For long address change "False" to "True"
        self.throttle1 = self.getThrottle(6, False) #Tramwaj
        return

    def handle(self):
        # handle() is called repeatedly until it returns false.
        print("Inside handle(self)")

        speed_global = 0.4 # Ustawiamy jedną zmienna główną prędkosc

        """Funkcja uruchomieniowa - awaryjny dojazd do stacji startowej jezeli pociag na niej sie nie znajduje
        co okolo sekunde uzywa sygnalu dziekowego - jezeli na niej sie znajduje - trabi 3 razy po 2 sekundy"""
        def drive_to_start_station():
            print("INSIDE DRIVE TO STATION")
            self.throttle1.setSpeedSetting(0)  # Upewnia sie że kolejka jest zatrzymana
            self.waitMsec(1000)
            Kollib.drive_vehicle(self, self.throttle1, speed_global, True) # Rusza do przodu by wzbudzic pierwszy czujnik
            Kollib.speed_change(self, self.throttle1, 0.6)
            while SensorsList1[0].state != ACTIVE:
                self.waitMsec(100)
                self.throttle1.setF2(True)  # run make some noise
                self.waitMsec(1000)
                self.throttle1.setF2(False)  #end make some noise
                self.waitMsec(100)
                if SensorsList1[0].state == ACTIVE:
                    if SensorsList1[1].state != ACTIVE:
                        Kollib.drive_vehicle(self, self.throttle1, 0.0, True)
                        print("INSIDE DRIVE TO STATION - train arrived to station - end of loop")
                        self.throttle1.setF1(False)  # wylacz dzwiek silnika
                        self.throttle1.setF2(True)  # run make some noise
                        self.waitMsec(2000)
                        self.throttle1.setF2(False)  # end make some noise
                        self.waitMsec(100)
                        self.throttle1.setF2(True)  # run make some noise
                        self.waitMsec(2000)
                        self.throttle1.setF2(False)  # end make some noise
                        self.waitMsec(100)
                        self.throttle1.setF2(True)  # run make some noise
                        self.waitMsec(2000)
                        self.throttle1.setF2(False)  # end make some noise
                        self.waitMsec(100)
                        self.waitMsec(10000)
                        pass
            pass

        if SensorsList1[0].state != ACTIVE:
            if SensorsList1[1].state != ACTIVE:
                print("Pociag nie na stacji startowej - uruchamiam funkcje jedz do stacji startowej")
                drive_to_start_station()
                print("Pociag na stacji startowej - Koncze skrypt")
                return 0 
        else:
            if SensorsList1[0].state == ACTIVE:
                if SensorsList1[1].state != ACTIVE:
                    Kollib.drive_vehicle(self, self.throttle1, 0.0, True)
                    print("INSIDE DRIVE TO STATION - train arrived to station - end of loop")
                    self.throttle1.setF1(False)  # wylacz dzwiek silnika
                    self.throttle1.setF2(True)  # run make some noise
                    self.waitMsec(2000)
                    self.throttle1.setF2(False)  # end make some noise
                    self.waitMsec(100)
                    self.throttle1.setF2(True)  # run make some noise
                    self.waitMsec(2000)
                    self.throttle1.setF2(False)  # end make some noise
                    self.waitMsec(100)
                    self.throttle1.setF2(True)  # run make some noise
                    self.waitMsec(2000)
                    self.throttle1.setF2(False)  # end make some noise
                    self.waitMsec(100)
                    self.waitMsec(10000)
                    pass
            return 0


Lok1EndDay().start()

