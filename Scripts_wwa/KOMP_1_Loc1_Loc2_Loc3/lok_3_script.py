import jarray
import jmri
import sys, os

# Dodaj ścieżke do katalogu, w którym znajduje sie biblioteka Kollib.py
sys.path.append(os.path.join(sys.path[0])) #szuka biblioteczki w tym samym folderze w ktorym jest uruchamiany skrypt
import Kollib #Biblioteka autorskich funkcji

#Funkcja wzbudzajaca czujniki
def activate_sensors(sensors_list):
    for sensor in sensors_list:
        sensor.setState(INACTIVE)

#Sekwencyjne przypisywanie adresów sensorą - trasa tramwaj
FirstSensorAdress = 32
NumberOfSensors = 16
SensorsList1 = []
for i in range(FirstSensorAdress, FirstSensorAdress + NumberOfSensors):
    SensorsList1.append(sensors.getSensor("LS"+str(i+1)))
#print("Sensor List 1:", SensorsList1)

#Wywolaj czujniki jako nieaktywne by je wzbudzić
activate_sensors(SensorsList1)

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


class Lok3(jmri.jmrit.automat.AbstractAutomaton):
    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration.
        print("LOK3 Program tramwaj wisla uruchomiony...  Czekam na sensor IS3.. ze skryptu startup..")
        self.waitMsec(6000)
        """Sensor wirtualny uruchamiajacy makiete - czekam na odpowiedz z startup_script.py"""
        self.startup_sensor = sensors.getSensor("IS3")  # Pozycja startowa tramwaj wisla
        self.waitSensorActive([self.startup_sensor])

        # get loco address. For long address change "False" to "True"
        self.throttle1 = self.getThrottle(11, False) #Tramwaj
        #self.throttle2 = self.getThrottle(11, False) #Tramwaj 2 na wahadlo z 1
        return

    def handle(self):
        # handle() is called repeatedly until it returns false.
        print("LOK3 Program LOK3_HANDLE uruchomiony")

        speed_global = 0.4 # Ustawiamy jedną zmienna główną prędkosc

        def turnouts_initial_positions():
            """Sprawdź czy zwrotnice sa w odpowiednim polozeniu i ustaw na pozycje startowe"""
            """#2 dla CLOSED, #4 dla THROW"""

            if TurnoutsList_BCD[0].getKnownState() == 2:
                TurnoutsList_BCD[0].setState(4)
                self.waitMsec(1000)
                print("LOK3 Przestawiam zwrotnice na THROWN:", TurnoutsList_BCD[0], TurnoutsList_BCD[0].getKnownState())

            elif TurnoutsList_BCD[1].getKnownState() == 2:
                TurnoutsList_BCD[1].setState(4)
                self.waitMsec(1000)
                print("LOK3 Przestawiam zwrotnice na THROWN:", TurnoutsList_BCD[1], TurnoutsList_BCD[1].getKnownState())

            else:
                TurnoutsList_BCD[0].setState(4)
                self.waitMsec(1000)
                print("LOK3 Przestawiam zwrotnice na THROWN:", TurnoutsList_BCD[0], TurnoutsList_BCD[0].getKnownState())
                TurnoutsList_BCD[1].setState(4)
                self.waitMsec(1000)
                print("LOK3 Przestawiam zwrotnice na THROWN:", TurnoutsList_BCD[1], TurnoutsList_BCD[1].getKnownState())
            return 0

        while True:
            def check_stop():
                """Sensor wirtualny zatrzymujacy lub uruchamiajacy z powrotem makiete"""
                self.startup_sensor = sensors.getSensor("IS3")  # Pozycja startowa tramwaj wisla
                suspend = self.waitSensorActive([self.startup_sensor])

                if suspend == ACTIVE:
                    pass
                elif suspend != ACTIVE:
                    print("LOK3 Pociagi zatrzymane LOK_3_wisla")
                    Kollib.drive_vehicle(self, self.throttle1, 0, True)
                    print("LOK3 Pauza wlaczona..")
                return

            """Jedzie do przodu - wozek napedowy z przodu"""
            def forward_train():
                #print("STATE: ", SensorsList1[0].state)
                print("LOK3 TRASA DO LOTNISKA")
                self.throttle1.setSpeedSetting(0)  # Upewnia sie że kolejka jest zatrzymana
                self.waitMsec(500)
                if SensorsList1[0].state == ACTIVE:
                    #print("STATE1: ", SensorsList1[0].state)
                    #print("Czujnik zajety: ", SensorsList1[0])
                    self.waitMsec(100)
                    print("LOK3 Start ze stacji 1 - LOK3 TRASA DO LOTNISKA")
                    self.throttle1.setF1(True) # wlacz dzwiek silnika
                    self.waitMsec(8000)
                    self.throttle1.setF0(True)# Zapal światła
                    self.waitMsec(100)
                    self.throttle1.setF4(True) # Wlacz dzwonek przed ruszeniem
                    self.waitMsec(100)
                    self.throttle1.setF4(False) # Wylacz dzwonek przed ruszeniem
                    self.waitMsec(4000)
                    self.throttle1.setF2(True) # Wlacz trabnij przed ruszeniem
                    self.waitMsec(1000)
                    self.throttle1.setF2(False) # Wylacz trabnij przed ruszeniem
                    self.waitMsec(100)
                    Kollib.drive_vehicle(self, self.throttle1, speed_global, True)
                    self.waitMsec(100)

                    self.waitSensorActive(SensorsList1[1])
                    #print("Czujnik zajety: ", SensorsList1[1])
                    self.waitMsec(100)

                    self.waitSensorActive(SensorsList1[2])
                    #print("Czujnik zajety: ", SensorsList1[2])
                    self.waitMsec(100)
                    print("LOK3 Zatrzymanie na stacji 2 - LOK3 TRASA DO LOTNISKA")
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[2], 3000)
                    Kollib.stop_at_station(self, self.throttle1, SensorsList1[2], 6000)
                    print("LOK3 Start ze stacji 2 - LOK3 TRASA DO LOTNISKA")
                    self.throttle1.setF4(True) # Wlacz dzwonek przed ruszeniem
                    self.waitMsec(100)
                    self.throttle1.setF4(False) # Wylacz dzwonek przed ruszeniem
                    self.waitMsec(4000)
                    self.throttle1.setF2(True) # Wlacz trabnij przed ruszeniem
                    self.waitMsec(1000)
                    self.throttle1.setF2(False) # Wylacz trabnij przed ruszeniem
                    self.waitMsec(100)
                    Kollib.drive_vehicle(self, self.throttle1, speed_global, True)
                    self.waitMsec(500)

                    self.waitSensorActive(SensorsList1[4])
                    #print("Czujnik zajety: ", SensorsList1[4])
                    self.waitMsec(100)
                    print("LOK3 Zatrzymanie na stacji 3 - LOK3 TRASA DO LOTNISKA")
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[4], 1000)
                    Kollib.stop_at_station(self, self.throttle1, SensorsList1[4], 6000)
                    print("LOK3 Start ze stacji 3 - LOK3 TRASA DO LOTNISKA")
                    self.throttle1.setF4(True) # Wlacz dzwonek przed ruszeniem
                    self.waitMsec(100)
                    self.throttle1.setF4(False) # Wylacz dzwonek przed ruszeniem
                    self.waitMsec(4000)
                    self.throttle1.setF2(True) # Wlacz trabnij przed ruszeniem
                    self.waitMsec(1000)
                    self.throttle1.setF2(False) # Wylacz trabnij przed ruszeniem
                    self.waitMsec(100)
                    Kollib.drive_vehicle(self, self.throttle1, speed_global, True)
                    self.waitMsec(100)

                    self.waitSensorActive(SensorsList1[7])
                    #print("Czujnik zajety: ", SensorsList1[7])
                    print("LOK3 Zatrzymanie na stacji 4 - LOK3 TRASA DO LOTNISKA")
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[7], 2500)
                    Kollib.stop_at_station(self, self.throttle1, SensorsList1[7], 6000)
                    print("LOK3 Start ze stacji 4 - LOK3 TRASA DO LOTNISKA")
                    self.throttle1.setF4(True) # Wlacz dzwonek przed ruszeniem
                    self.waitMsec(100)
                    self.throttle1.setF4(False) # Wylacz dzwonek przed ruszeniem
                    self.waitMsec(4000)
                    self.throttle1.setF2(True) # Wlacz trabnij przed ruszeniem
                    self.waitMsec(1000)
                    self.throttle1.setF2(False) # Wylacz trabnij przed ruszeniem
                    self.waitMsec(100)
                    Kollib.drive_vehicle(self, self.throttle1, speed_global, True)
                    Kollib.speed_change(self, self.throttle1, 0.5) #zmiana predkosci
                    self.waitMsec(100)

                    self.waitSensorActive(SensorsList1[8])
                    #print("Czujnik zajety: ", SensorsList1[8])
                    self.waitMsec(100)

                    self.waitSensorActive(SensorsList1[10])
                    #print("Czujnik zajety: ", SensorsList1[10])
                    Kollib.speed_change(self, self.throttle1, 0.5) #zmiana predkosci
                    self.waitMsec(100)

                    self.waitSensorActive(SensorsList1[9])
                    #print("Czujnik zajety: ", SensorsList1[9])
                    print("LOK3 Zatrzymanie na stacji 5 - LOK3 TRASA DO LOTNISKA")
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[9], 1500)
                    Kollib.stop_at_station(self, self.throttle1, SensorsList1[9], 6000)
                    print("LOK3 Stacja KONCOWA - stacja 5 - LOK3 TRASA DO LOTNISKA")
                    self.throttle1.setF0(False) # Zgaś światła
                    self.waitMsec(100)
                    self.throttle1.setF1(False) #wylacz dzwiek silnika
                    self.waitMsec(8000)
                    print("LOK3 KONIEC PETLI DO LOTNISKA, ROZPOCZYNAM NOWA LOK_3")
                    return 0

            """Jedzie do tylu - wozek napedowy z przodu"""
            def backward_train():
                #print("STATE: ", SensorsList1[0].state)
                #print("Inside handle(backward_train)")
                self.throttle1.setSpeedSetting(0)  # Upewnia sie że kolejka jest zatrzymana
                self.waitMsec(500)
                if SensorsList1[9].state == ACTIVE:
                    #print("STATE1: ", SensorsList1[9].state)
                    #print("Czujnik zajety: ", SensorsList1[9])
                    self.waitMsec(100)
                    print("LOK3 Start ze stacji 5 - LOK3 TRASA DO POMNIKA")
                    self.throttle1.setF1(True)  # wlacz dzwiek silnika
                    self.waitMsec(8000)
                    self.throttle1.setF0(True)  # Zapal światła
                    self.waitMsec(100)
                    self.throttle1.setF4(True) # Wlacz dzwonek przed ruszeniem
                    self.waitMsec(100)
                    self.throttle1.setF4(False) # Wylacz dzwonek przed ruszeniem
                    self.waitMsec(4000)
                    self.throttle1.setF2(True) # Wlacz trabnij przed ruszeniem
                    self.waitMsec(1000)
                    self.throttle1.setF2(False) # Wylacz trabnij przed ruszeniem
                    self.waitMsec(100)
                    Kollib.drive_vehicle(self, self.throttle1, speed_global, False)
                    self.waitMsec(4000)

                    self.waitSensorActive(SensorsList1[10])
                    #print("Czujnik zajety: ", SensorsList1[10])
                    self.waitMsec(100)

                    self.waitSensorActive(SensorsList1[8])
                    #print("Czujnik zajety: ", SensorsList1[8])
                    Kollib.speed_change(self, self.throttle1, 0.5) #zmiana predkosci
                    self.waitMsec(100)

                    self.waitSensorActive(SensorsList1[7])
                    #print("Czujnik zajety: ", SensorsList1[7])
                    print("LOK3 Zatrzymanie na stacji 4 - LOK3 TRASA DO POMNIKA")
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[7], 4500)
                    Kollib.stop_at_station(self, self.throttle1, SensorsList1[7], 6000)
                    print("LOK3 Start ze stacji 4 - LOK3 TRASA DO POMNIKA")
                    self.throttle1.setF4(True)  # Wlacz dzwonek przed ruszeniem
                    self.waitMsec(100)
                    self.throttle1.setF4(False)  # Wylacz dzwonek przed ruszeniem
                    self.waitMsec(4000)
                    self.throttle1.setF2(True)  # Wlacz trabnij przed ruszeniem
                    self.waitMsec(1000)
                    self.throttle1.setF2(False)  # Wylacz trabnij przed ruszeniem
                    self.waitMsec(100)
                    Kollib.drive_vehicle(self, self.throttle1, speed_global, False)

                    self.waitSensorActive(SensorsList1[4])
                    #print("Czujnik zajety: ", SensorsList1[4])
                    self.waitMsec(100)
                    Kollib.speed_change(self, self.throttle1, 0.5) #zmiana predkosci
                    self.waitMsec(100)

                    self.waitSensorActive(SensorsList1[3])
                    #print("Czujnik zajety: ", SensorsList1[3])
                    self.waitMsec(100)
                    print("LOK3 Zatrzymanie na stacji 3 - LOK3 TRASA DO POMNIKA")
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[3], 1500)
                    Kollib.stop_at_station(self, self.throttle1, SensorsList1[3], 6000)
                    print("LOK3 Start ze stacji 3 - LOK3 TRASA DO POMNIKA")
                    self.throttle1.setF4(True)  # Wlacz dzwonek przed ruszeniem
                    self.waitMsec(100)
                    self.throttle1.setF4(False)  # Wylacz dzwonek przed ruszeniem
                    self.waitMsec(4000)
                    self.throttle1.setF2(True)  # Wlacz trabnij przed ruszeniem
                    self.waitMsec(1000)
                    self.throttle1.setF2(False)  # Wylacz trabnij przed ruszeniem
                    self.waitMsec(100)
                    Kollib.drive_vehicle(self, self.throttle1, speed_global, False)
                    self.waitMsec(100)

                    self.waitSensorActive(SensorsList1[2])
                    #print("Czujnik zajety: ", SensorsList1[2])
                    Kollib.speed_change(self, self.throttle1, 0.5) #zmiana predosci
                    print("LOK3 Zatrzymanie na stacji 2 - LOK3 TRASA DO POMNIKA")
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[2], 3000)
                    Kollib.stop_at_station(self, self.throttle1, SensorsList1[2], 6000)
                    self.waitMsec(100)
                    self.throttle1.setF4(True)  # Wlacz dzwonek przed ruszeniem
                    self.waitMsec(100)
                    self.throttle1.setF4(False)  # Wylacz dzwonek przed ruszeniem
                    self.waitMsec(4000)
                    self.throttle1.setF2(True)  # Wlacz trabnij przed ruszeniem
                    self.waitMsec(1000)
                    self.throttle1.setF2(False)  # Wylacz trabnij przed ruszeniem
                    self.waitMsec(100)
                    Kollib.drive_vehicle(self, self.throttle1, speed_global, False)

                    self.waitSensorActive(SensorsList1[1])
                    #print("Czujnik zajety: ", SensorsList1[1])
                    Kollib.speed_change(self, self.throttle1, 0.5)
                    self.waitMsec(100)

                    self.waitSensorActive(SensorsList1[0])
                    print("LOK3 Czujnik zajety: ", SensorsList1[0])
                    print("LOK3 Zatrzymanie na stacji 1 - LOK3 TRASA DO POMNIKA")
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[0], 2000)
                    Kollib.stop_at_station(self, self.throttle1, SensorsList1[0], 6000)
                    print("LOK3 Stacja KONCOWA - stacja 1 - LOK3 TRASA DO POMNIKA")
                    self.throttle1.setF0(False)  # Zgaś światła
                    self.waitMsec(100)
                    self.throttle1.setF1(False)  # wylacz dzwiek silnika
                    self.waitMsec(10000)
                    print("LOK3 KONIEC PETLI DO POMNIKA, ROZPOCZYNAM NOWA LOK_3")
                    return 0

            """Uruchom odpowiednia funkcje zalezna od tego na ktorym torze krancowym sie znajduje"""
            if SensorsList1[0].state == ACTIVE:
                print("LOK3 Sprawdzam czy pauza..")
                check_stop()
                print("LOK3 Uruchamiam funkcje TRAM WISLA DO LOTNISKA")
                turnouts_initial_positions()
                forward_train()
            elif SensorsList1[9].state == ACTIVE:
                print("LOK3 Uruchamiam funkcje TRAM WISLA DO POMNIKA")
                turnouts_initial_positions()
                backward_train()


Lok3().start()

