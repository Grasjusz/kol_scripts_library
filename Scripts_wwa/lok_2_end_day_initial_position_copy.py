import jarray
import jmri
import sys, os

# Dodaj ścieżke do katalogu, w którym znajduje sie biblioteka Kollib.py
sys.path.append(os.path.join(sys.path[0]))
import Kollib  # Biblioteka autorskich funkcji

# Sekwencyjne przypisywanie adresów sensorą - trasa tramwaj

FirstSensorAdress = 16
NumberOfSensors = 6
SensorsList1 = []
for i in range(FirstSensorAdress, FirstSensorAdress + NumberOfSensors):
    SensorsList1.append(sensors.getSensor("LS" + str(i + 1)))
print("Sensor List 1:", SensorsList1)

# Sekwencyjne przypisywanie adresów sensorą - trasa br80 towarowa
FirstSensorAdress = 22
NumberOfSensors = 9
SensorsList2 = []
for i in range(FirstSensorAdress, FirstSensorAdress + NumberOfSensors):
    SensorsList2.append(sensors.getSensor("LS" + str(i + 1)))
print("Sensor List 2:", SensorsList2)

# Reczne przypisywanie adresów sensorą
Sensor32 = sensors.getSensor("LS32")  # Mijanka/zatoczka na tramwaju
print("Sensor mijanka/wahadlo:", Sensor32)

FirstTurnoutAdress = 100
NumberOfTurnouts = 4
TurnoutsList_BCD = []
for i in range(FirstTurnoutAdress, FirstTurnoutAdress + NumberOfTurnouts):
    TurnoutsList_BCD.append(turnouts.getTurnout("LT" + str(i)))
print(TurnoutsList_BCD)

'''
Jeśli czujniki nie są ułożone w sekwencji, możesz dodać je jako Sensor1 = sensors.getSensor("LS1") lub
SensorsList.append(sensors.getSensor("LS" + str(1))), jeśli chcesz umieścić je w liście.

Jeśli to możliwe, dopisz taki sam algorytm dla innych elementów.

Jeśli dany sensor nie znajduje sie na liście sensorów w panelu "PanelPro" 
(jego wartość to None), skutkuje to wyłaczeniem watku w którym znajduje sie fukcja
odnoszaca sie do tego czujnika.
'''


class Lok2EndDay(jmri.jmrit.automat.AbstractAutomaton):

    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration.
        print("Inside init(self)")

        # get loco address. For long address change "False" to "True"
        self.throttle1 = self.getThrottle(3, False)  # Tramwaj
        self.throttle2 = self.getThrottle(6, False)  # BR80, towarowy

    def handle(self):
        # handle() is called repeatedly until it returns false.
        print("Inside handle(self)")
        self.throttle1.setSpeedSetting(0)  # Upewnia sie że kolejka jest zatrzymana
        self.throttle2.setSpeedSetting(0)  # Upewnia sie że kolejka jest zatrzymana

        speed_global = 0.2 # Ustawiamy jedną zmienna główną prędkosc

        def turnouts_initial_positions():
            """Sprawdz czy zwrotnice sa w odpowiednim polozeniu i ustaw na pozycje startowe"""
            # 2 dla CLOSED, #4 dla THROWN
            TurnoutsList_BCD[0].setState(4)
            self.waitMsec(1000)
            print("Przestawiam zwrotnice na THROWN:", TurnoutsList_BCD[0], TurnoutsList_BCD[0].getKnownState())
            TurnoutsList_BCD[1].setState(4)
            self.waitMsec(1000)
            print("Przestawiam zwrotnice na THROWN:", TurnoutsList_BCD[1], TurnoutsList_BCD[0].getKnownState())
            TurnoutsList_BCD[2].setState(4)
            self.waitMsec(1000)
            print("Przestawiam zwrotnice na THROWN:", TurnoutsList_BCD[2], TurnoutsList_BCD[0].getKnownState())
            TurnoutsList_BCD[3].setState(4)
            self.waitMsec(1000)
            print("Przestawiam zwrotnice na THROWN:", TurnoutsList_BCD[3], TurnoutsList_BCD[0].getKnownState())

        """Funkcja uruchomieniowa - awaryjny dojazd do stacji startowej jezeli pociag na niej sie nie znajduje
        co okolo sekunde uzywa sygnalu dziekowego - jezeli na niej sie znajduje - trabi 3 razy po 2 sekundy"""
        def drive_to_start_station_tram():
            print("INSIDE DRIVE TO STATION FORWARD TRAM")
            self.throttle1.setSpeedSetting(0)  # Upewnia sie że kolejka jest zatrzymana
            self.waitMsec(1000)
            if SensorsList1[0] != ACTIVE:
                Kollib.drive_vehicle(self, self.throttle1, speed_global, True) # Rusza do przodu by wzbudzic pierwszy czujnik
                Kollib.speed_change(self, self.throttle1, 0.6)
                while SensorsList1[0].state != ACTIVE:
                    self.waitMsec(100)
                    self.throttle1.setF10(True)  # run make some noise
                    self.waitMsec(1000)
                    self.throttle1.setF10(False)  #end make some noise
                    self.waitMsec(100)
                    if SensorsList1[0].state == ACTIVE:
                        self.waitMsec(2000)
                        if SensorsList1[1].state != ACTIVE:
                            Kollib.drive_vehicle(self, self.throttle1, 0.0,True)
                            print("INSIDE DRIVE TO STATION - train arrived to station - end of loop")
                            self.throttle1.setF6(False)  # wylacz dzwiek silnika
                            self.throttle1.setF10(True)  # run make some noise
                            self.waitMsec(2000)
                            self.throttle1.setF10(False)  # end make some noise
                            self.waitMsec(100)
                            self.throttle1.setF10(True)  # run make some noise
                            self.waitMsec(2000)
                            self.throttle1.setF10(False)  # end make some noise
                            self.waitMsec(100)
                            self.throttle1.setF10(True)  # run make some noise
                            self.waitMsec(2000)
                            self.throttle1.setF10(False)  # end make some noise
                            self.waitMsec(10000)
                            pass
                pass

        """Funkcja wywolujaca funkcje uruchomieniowe dojazdu do stacji startowych"""
        def tram_initial_station_func():
            """Petla odpalajaca powrot do stacji startowej tramwaj"""
            if SensorsList1[0].state != ACTIVE:
                if SensorsList1[1].state != ACTIVE:
                    print("Pociag nie na stacji startowej - uruchamiam funkcje jedz do stacji startowej")
                    turnouts_initial_positions()
                    drive_to_start_station_tram()
                    Kollib.drive_vehicle(self, self.throttle1, 0.0, True)
                    print("Pociag na stacji startowej - Koncze skrypt")
                    pass
            else:
                if SensorsList1[0].state == ACTIVE:
                    if SensorsList1[1].state != ACTIVE:
                        turnouts_initial_positions()
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

        """Funkcja uruchomieniowa - awaryjny dojazd do stacji startowej jezeli pociag na niej sie nie znajduje
        co okolo sekunde uzywa sygnalu dziekowego - jezeli na niej sie znajduje - trabi 3 razy po 2 sekundy"""
        def drive_to_start_station_train():
            print("INSIDE DRIVE TO STATION FORWARD TRAIN")
            self.throttle2.setSpeedSetting(0)  # Upewnia sie że kolejka jest zatrzymana
            self.waitMsec(1000)
            if SensorsList2[8] != ACTIVE:
                Kollib.drive_vehicle(self, self.throttle2, speed_global,True)  # Rusza do przodu by wzbudzic pierwszy czujnik
                Kollib.speed_change(self, self.throttle2, 0.6)
                while SensorsList2[8].state != ACTIVE:
                    self.waitMsec(100)
                    self.throttle2.setF2(True)  # run make some noise
                    self.waitMsec(1000)
                    self.throttle2.setF2(False)  # end make some noise
                    self.waitMsec(100)
                    if SensorsList2[8].state == ACTIVE:
                        self.waitMsec(2000)
                        if SensorsList2[7].state != ACTIVE:
                            Kollib.drive_vehicle(self, self.throttle2, 0.0, True)
                            print("INSIDE DRIVE TO STATION - train arrived to station - end of loop")
                            self.throttle2.setF1(False)  # wylacz dzwiek silnika
                            self.throttle2.setF2(True)  # run make some noise
                            self.waitMsec(2000)
                            self.throttle2.setF2(False)  # end make some noise
                            self.waitMsec(100)
                            self.throttle2.setF2(True)  # run make some noise
                            self.waitMsec(2000)
                            self.throttle2.setF2(False)  # end make some noise
                            self.waitMsec(100)
                            self.throttle2.setF2(True)  # run make some noise
                            self.waitMsec(2000)
                            self.throttle2.setF2(False)  # end make some noise
                            self.waitMsec(10000)
                            pass
                pass

        """Funkcja wywolujaca funkcje uruchomieniowe dojazdu do stacji startowych"""
        def train_initial_station_func():
            """Petla odpalajaca powrot do stacji startowej pociag"""
            if SensorsList2[8].state != ACTIVE:
                if SensorsList2[7].state != ACTIVE:
                    print("Pociag nie na stacji startowej - uruchamiam funkcje jedz do stacji startowej")
                    turnouts_initial_positions()
                    drive_to_start_station_train()
                    Kollib.drive_vehicle(self, self.throttle2, 0.0, True)
                    print("Pociag na stacji startowej - Koncze skrypt")
                    pass
            else:
                if SensorsList2[8].state == ACTIVE:
                    if SensorsList2[7].state != ACTIVE:
                        turnouts_initial_positions()
                        Kollib.drive_vehicle(self, self.throttle2, 0.0, True)
                        print("INSIDE DRIVE TO STATION - train arrived to station - end of loop")
                        self.throttle2.setF1(False)  # wylacz dzwiek silnika
                        self.throttle2.setF2(True)  # run make some noise
                        self.waitMsec(2000)
                        self.throttle2.setF2(False)  # end make some noise
                        self.waitMsec(100)
                        self.throttle2.setF2(True)  # run make some noise
                        self.waitMsec(2000)
                        self.throttle2.setF2(False)  # end make some noise
                        self.waitMsec(100)
                        self.throttle2.setF2(True)  # run make some noise
                        self.waitMsec(2000)
                        self.throttle2.setF2(False)  # end make some noise
                        self.waitMsec(10000)
                        pass
                pass

        tram_initial_station_func()
        train_initial_station_func()
        print("Pociagi ustawione na stacjach - sprawdz na mapce zajetosc czujnikow i uruchom skrypt wlaczajacy wlasciwy skrypt")
        print("Sprawdz czy jest wlaczone zasilanie makiety")
        return 0


Lok2EndDay().start()

