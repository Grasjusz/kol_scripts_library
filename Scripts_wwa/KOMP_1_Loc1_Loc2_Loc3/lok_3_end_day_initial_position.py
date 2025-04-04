import jarray
import jmri
import sys, os

# Dodaj ścieżke do katalogu, w którym znajduje sie biblioteka Kollib.py
sys.path.append(os.path.join(sys.path[0]))
import Kollib #Biblioteka autorskich funkcji

#Sekwencyjne przypisywanie adresów sensorą - trasa tramwaj
FirstSensorAdress = 32
NumberOfSensors = 16
SensorsList1 = []
for i in range(FirstSensorAdress, FirstSensorAdress + NumberOfSensors):
    SensorsList1.append(sensors.getSensor("LS"+str(i+1)))
#print("Sensor List 1:", SensorsList1)

FirstTurnoutAdress = 104
NumberOfTurnouts = 2
TurnoutsList_BCD = []
for i in range(FirstTurnoutAdress, FirstTurnoutAdress + NumberOfTurnouts):
    TurnoutsList_BCD.append(turnouts.getTurnout("LT"+str(i)))
#print("Turnout List 1:", TurnoutsList_BCD)

'''
Jeśli czujniki nie są ułożone w sekwencji, możesz dodać je jako Sensor1 = sensors.getSensor("LS1") lub
SensorsList.append(sensors.getSensor("LS" + str(1))), jeśli chcesz umieścić je w liście.

Jeśli to możliwe, dopisz taki sam algorytm dla innych elementów.

Jeśli dany sensor nie znajduje sie na liście sensorów w panelu "PanelPro" 
(jego wartość to None), skutkuje to wyłaczeniem watku w którym znajduje sie fukcja
odnoszaca sie do tego czujnika.
'''


class Lok3EndDay(jmri.jmrit.automat.AbstractAutomaton):

    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration.
        # get loco address. For long address change "False" to "True"
        self.throttle1 = self.getThrottle(11, False)  # Tramwaj


    def handle(self):
        # handle() is called repeatedly until it returns false.
        print("LOK3 funkcja awaryjna, ustawiam pociagi na pozycje startowe")
        self.throttle1.setSpeedSetting(0)  # Upewnia sie że kolejka jest zatrzymana
        speed_global = 0.4 # Ustawiamy jedną zmienna główną prędkosc
        def turnouts_initial_positions():
            """Sprawdź czy zwrotnice sa w odpowiednim polozeniu i ustaw na pozycje startowe"""
            # 2 dla CLOSED, #4 dla THROWN

            if TurnoutsList_BCD[0].getKnownState() == 2:
                TurnoutsList_BCD[0].setState(4)
                self.waitMsec(1000)
                print("LOK3 Przestawiam zwrotnice na THROWN:", TurnoutsList_BCD[0], TurnoutsList_BCD[0].getKnownState())

            elif TurnoutsList_BCD[1].getKnownState() == 2:
                TurnoutsList_BCD[1].setState(4)
                self.waitMsec(1000)
                print("LOK3 Przestawiam zwrotnice na THROWN:", TurnoutsList_BCD[1], TurnoutsList_BCD[0].getKnownState())
            else:
                TurnoutsList_BCD[0].setState(4)
                self.waitMsec(1000)
                print("LOK3 Przestawiam zwrotnice na THROWN:", TurnoutsList_BCD[0], TurnoutsList_BCD[0].getKnownState())
                TurnoutsList_BCD[1].setState(4)
                self.waitMsec(1000)
                print("LOK3 Przestawiam zwrotnice na THROWN:", TurnoutsList_BCD[1], TurnoutsList_BCD[0].getKnownState())

            return 0


        """Funkcja uruchomieniowa - awaryjny dojazd do stacji startowej jezeli pociag na niej sie nie znajduje
        co okolo sekunde uzywa sygnalu dziekowego - jezeli na niej sie znajduje - trabi 3 razy po 2 sekundy"""
        def drive_to_start_station_tram():
            print("LOK3 Pociag uruchamiam funkcje powrotu na stacje poczatkowe")
            self.throttle1.setSpeedSetting(0)  # Upewnia sie że kolejka jest zatrzymana
            self.waitMsec(1000)
            if SensorsList1[0] != ACTIVE:
                Kollib.drive_vehicle(self, self.throttle1, speed_global, False) # Rusza do tylu by wzbudzic pierwszy czujnik
                while SensorsList1[0].state != ACTIVE:
                    self.waitMsec(100)
                    self.throttle1.setF0(True)  # wlacz mruganie swiatlami
                    self.waitMsec(1000)
                    self.throttle1.setF0(False)  # wylacz mruganie swiatlami
                    self.waitMsec(100)
                    if SensorsList1[0].state == ACTIVE:
                        if SensorsList1[1].state != ACTIVE:
                            Kollib.drive_vehicle(self, self.throttle1, 0.0,False)
                            print("LOK3 Pociag dojechal na stacje startowa - koniec petli")
                            self.waitMsec(100)
                            self.throttle1.setF1(False)  # wylacz dzwiek silnika
                            self.throttle1.setF0(False)  # zgas światła
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
                            self.waitMsec(10000)
                            return 0

        """Funkcja wywolujaca funkcje uruchomieniowe dojazdu do stacji startowych"""
        def tram_initial_station_func():
            """Petla odpalajaca powrot do stacji startowej tramwaj"""
            if SensorsList1[0].state != ACTIVE:
                if SensorsList1[9].state != ACTIVE:
                    print("LOK3 Pociag uruchamiam funkcje powrotu na stacje poczatkowe")
                    turnouts_initial_positions() #sprawdz czy zwrotnice sa przestawione
                    drive_to_start_station_tram() # uruchom program powracajacy na stacje startowe
                    Kollib.drive_vehicle(self, self.throttle1, 0.0, False)
                    print("LOK3 pociag na stacji startowej - Koncze skrypt")
                    return 0
            else:
                if SensorsList1[0].state == ACTIVE:
                    if SensorsList1[1].state != ACTIVE:
                        if SensorsList1[9].state != ACTIVE:
                            turnouts_initial_positions()
                            Kollib.drive_vehicle(self, self.throttle1, 0.0, False)
                            print("LOK3 Pociag dojechal na stacje startowa - koniec petli")
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
                            self.waitMsec(10000)
                            return 0

        tram_initial_station_func()
        return 0


Lok3EndDay().start()

