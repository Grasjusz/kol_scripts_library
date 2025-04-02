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
print("Sensor List 1:", SensorsList1)

FirstTurnoutAdress = 104
NumberOfTurnouts = 2
TurnoutsList_BCD = []
for i in range(FirstTurnoutAdress, FirstTurnoutAdress + NumberOfTurnouts):
    TurnoutsList_BCD.append(turnouts.getTurnout("LT"+str(i)))
print("Turnout List 1:", TurnoutsList_BCD)

'''
Jeśli czujniki nie są ułożone w sekwencji, możesz dodać je jako Sensor1 = sensors.getSensor("LS1") lub
SensorsList.append(sensors.getSensor("LS" + str(1))), jeśli chcesz umieścić je w liście.

Jeśli to możliwe, dopisz taki sam algorytm dla innych elementów.

Jeśli dany sensor nie znajduje sie na liście sensorów w panelu "PanelPro" 
(jego wartość to None), skutkuje to wyłaczeniem watku w którym znajduje sie fukcja
odnoszaca sie do tego czujnika.
'''


class lok3(jmri.jmrit.automat.AbstractAutomaton):
    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration.
        print("Inside init(self)")
        # get loco address. For long address change "False" to "True"
        self.throttle1 = self.getThrottle(6, False) #Tramwaj
        #self.throttle2 = self.getThrottle(6, False) #BR80, towarowy
        return

    def handle(self):

        speed_global = 0.4 # Ustawiamy jedną zmienna główną prędkosc

        # handle() is called repeatedly until it returns false.
        print("Inside handle(self)")
        """Sprawdź czy zwrotnice sa w odpowiednim polozeniu i ustaw na pozycje startowe"""
        # 2 dla CLOSED, #4 dla THROWN
        TurnoutsList_BCD[0].setState(4)
        self.waitMsec(1000)
        print("Przestawiam zwrotnice na THROWN:", TurnoutsList_BCD[0], TurnoutsList_BCD[0].getKnownState())
        TurnoutsList_BCD[1].setState(4)
        self.waitMsec(1000)
        print("Przestawiam zwrotnice na THROWN:", TurnoutsList_BCD[1],  TurnoutsList_BCD[0].getKnownState())
        while True:

            """Jedzie do przodu - wozek napedowy z przodu"""
            def forward_train():
                print("STATE: ", SensorsList1[0].state)
                print("Inside handle(forward_tram)")
                self.throttle1.setSpeedSetting(0)  # Upewnia sie że kolejka jest zatrzymana
                self.waitMsec(500)
                if SensorsList1[0].state == ACTIVE:
                    print("STATE1: ", SensorsList1[0].state)
                    print("Czujnik zajety: ", SensorsList1[0])
                    self.waitMsec(100)
                    print("Start ze stacji 1 FORWARD")
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
                    print("Czujnik zajety: ", SensorsList1[1])
                    self.waitMsec(100)

                    self.waitSensorActive(SensorsList1[2])
                    print("Czujnik zajety: ", SensorsList1[2])
                    self.waitMsec(100)
                    print("Zatrzymanie na stacji 2 FORWARD")
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[2], 5000)
                    Kollib.stop_at_station(self, self.throttle1, SensorsList1[2], 6000)
                    print("Start ze stacji 2 FORWARD")
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
                    print("Czujnik zajety: ", SensorsList1[4])
                    self.waitMsec(100)

                    print("Zatrzymanie na stacji 3 FORWARD")
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[4], 1000)
                    Kollib.stop_at_station(self, self.throttle1, SensorsList1[4], 6000)
                    print("Start ze stacji 3 FORWARD")
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
                    print("Czujnik zajety: ", SensorsList1[7])
                    print("Zatrzymanie na stacji 4 FORWARD")
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[7], 2500)
                    Kollib.stop_at_station(self, self.throttle1, SensorsList1[7], 6000)
                    print("Start ze stacji 4 FORWARD")
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
                    print("Czujnik zajety: ", SensorsList1[8])
                    self.waitMsec(100)

                    self.waitSensorActive(SensorsList1[10])
                    print("Czujnik zajety: ", SensorsList1[10])
                    Kollib.speed_change(self, self.throttle1, 0.5) #zmiana predkosci
                    self.waitMsec(100)

                    self.waitSensorActive(SensorsList1[9])
                    print("Czujnik zajety: ", SensorsList1[9])
                    print("Zatrzymanie na stacji 5 FORWARD")
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[9], 800)
                    Kollib.stop_at_station(self, self.throttle1, SensorsList1[9], 6000)
                    print("Stacja KONCOWA - stacja 5 BACKWARD")
                    self.throttle1.setF0(False) # Zgaś światła
                    self.waitMsec(100)
                    self.throttle1.setF1(False) #wylacz dzwiek silnika
                    self.waitMsec(8000)
                    print("Koniec funkcji forward_train")

                    return 0

            def backward_train():
                print("STATE: ", SensorsList1[0].state)
                print("Inside handle(backward_train)")
                self.throttle1.setSpeedSetting(0)  # Upewnia sie że kolejka jest zatrzymana
                self.waitMsec(500)
                if SensorsList1[9].state == ACTIVE:
                    print("STATE1: ", SensorsList1[9].state)
                    print("Czujnik zajety: ", SensorsList1[9])
                    self.waitMsec(100)
                    print("Start ze stacji 5 BACKWARD")
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
                    print("Czujnik zajety: ", SensorsList1[10])
                    self.waitMsec(100)

                    self.waitSensorActive(SensorsList1[8])
                    print("Czujnik zajety: ", SensorsList1[8])
                    Kollib.speed_change(self, self.throttle1, 0.5) #zmiana predkosci
                    self.waitMsec(100)

                    self.waitSensorActive(SensorsList1[7])
                    print("Czujnik zajety: ", SensorsList1[7])
                    print("Zatrzymanie na stacji 4 BACKWARD")
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[7], 4500)
                    Kollib.stop_at_station(self, self.throttle1, SensorsList1[7], 6000)
                    print("Start ze stacji 4 BACKWARD")
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
                    print("Czujnik zajety: ", SensorsList1[4])
                    self.waitMsec(100)
                    Kollib.speed_change(self, self.throttle1, 0.5) #zmiana predkosci
                    self.waitMsec(100)

                    self.waitSensorActive(SensorsList1[3])
                    print("Czujnik zajety: ", SensorsList1[3])
                    self.waitMsec(100)
                    print("Zatrzymanie na stacji 3 BACKWARD")
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[3], 1500)
                    Kollib.stop_at_station(self, self.throttle1, SensorsList1[3], 6000)
                    print("Start ze stacji 3 BACKWARD")
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
                    print("Czujnik zajety: ", SensorsList1[2])
                    Kollib.speed_change(self, self.throttle1, 0.5) #zmiana predosci
                    print("Zatrzymanie na stacji 2 BACKWARD")
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
                    print("Czujnik zajety: ", SensorsList1[1])
                    Kollib.speed_change(self, self.throttle1, 0.5)
                    self.waitMsec(100)

                    self.waitSensorActive(SensorsList1[0])
                    print("Czujnik zajety: ", SensorsList1[0])
                    print("Zatrzymanie na stacji 1 BACKWARD")
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[0], 2000)
                    Kollib.stop_at_station(self, self.throttle1, SensorsList1[0], 6000)
                    print("Stacja KONCOWA - stacja 1 BACKWARD")
                    self.throttle1.setF0(False)  # Zgaś światła
                    self.waitMsec(100)
                    self.throttle1.setF1(False)  # wylacz dzwiek silnika
                    self.waitMsec(10000)
                    return 0

            """Uruchom odpowiednia funkcje zalezna od tego na ktorym torze krancowym sie znajduje"""
            if SensorsList1[0].state == ACTIVE:
                print("Uruchamian funkcje forward_train")
                forward_train()
            elif SensorsList1[9].state == ACTIVE:
                print("Uruchamian funkcje backward_train")
                backward_train()


lok3().start()

