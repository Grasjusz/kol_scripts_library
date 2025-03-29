import jarray
import jmri
import sys, os
import threading
# Dodaj ścieżke do katalogu, w którym znajduje sie biblioteka Kollib.py
sys.path.append(os.path.join(sys.path[0]))
import Kollib #Biblioteka autorskich funkcji

#Sekwencyjne przypisywanie adresów sensorą - trasa tramwaj
FirstSensorAdress = 16
NumberOfSensors = 6
SensorsList1 = []
for i in range(FirstSensorAdress, FirstSensorAdress + NumberOfSensors):
    SensorsList1.append(sensors.getSensor("LS"+str(i+1)))
print("Sensor List 1:", SensorsList1)

#Sekwencyjne przypisywanie adresów sensorą - trasa br80 towarowa
FirstSensorAdress = 22
NumberOfSensors = 9
SensorsList2 = []
for i in range(FirstSensorAdress, FirstSensorAdress + NumberOfSensors):
    SensorsList2.append(sensors.getSensor("LS"+str(i+1)))
print("Sensor List 2:", SensorsList2)

#Reczne przypisywanie adresów sensorą
Sensor32 = sensors.getSensor("LS32") #Mijanka/zatoczka na tramwaju
print("Sensor mijanka/wahadlo:", Sensor32)

FirstTurnoutAdress = 100
NumberOfTurnouts = 4
TurnoutsList_BCD = []
for i in range(FirstTurnoutAdress, FirstTurnoutAdress + NumberOfTurnouts):
    TurnoutsList_BCD.append(turnouts.getTurnout("LT"+str(i)))
print(TurnoutsList_BCD)



'''
Jeśli czujniki nie są ułożone w sekwencji, możesz dodać je jako Sensor1 = sensors.getSensor("LS1") lub
SensorsList.append(sensors.getSensor("LS" + str(1))), jeśli chcesz umieścić je w liście.

Jeśli to możliwe, dopisz taki sam algorytm dla innych elementów.

Jeśli dany sensor nie znajduje sie na liście sensorów w panelu "PanelPro" 
(jego wartość to None), skutkuje to wyłaczeniem watku w którym znajduje sie fukcja
odnoszaca sie do tego czujnika.
'''


class lok2(jmri.jmrit.automat.AbstractAutomaton):

    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration.
        print("Inside init(self)")

        # get loco address. For long address change "False" to "True"
        self.throttle1 = self.getThrottle(3, False) #Tramwaj
        self.throttle2 = self.getThrottle(6, False) #BR80, towarowy
        return

    def handle(self):
        # handle() is called repeatedly until it returns false.
        """Sprawdź czy zwrotnice sa w odpowiednim polozeniu i ustaw na pozycje startowe
        #2 dla CLOSED, #4 dla THROWN """
        for turnout in TurnoutsList_BCD:
            if turnout.getKnownState() == 2:
                Kollib.zwrotnica_test(self, turnout)

        while True:
            """Jedzie do tylu - wozek napedowy z tylu"""
            def backward_tram():
                print("STATE: ", SensorsList1[0].state)
                # state17 = SensorsList1[0].getState() #sprawdź status sensora #2 for ACTIVE, #4 for INACTIVE
                # print("The state is:", state17)
                print("Inside handle(backward_tram)")
                self.throttle1.setSpeedSetting(0)  # Upewnia sie że kolejka jest zatrzymana
                self.waitMsec(500)
                if SensorsList1[0].state == ACTIVE:
                    print("Czujnik zajety: ", SensorsList1[0])
                    self.waitMsec(100)
                    self.throttle1.setF3(True)#Unieś pantografy
                    self.waitMsec(1000)
                    self.throttle1.setF17(True)# Oświetlenie stacji docelowej pociagu
                    self.waitMsec(100)
                    self.throttle1.setF0(True)# Wlaczenie swiatel pociagu
                    self.waitMsec(100)
                    self.throttle1.setF18(True)# Zamykanie drzwi
                    self.waitMsec(4000)
                    self.throttle1.setF18(False)# Zamykanie drzwi
                    self.waitMsec(2000)
                    Kollib.drive_vehicle(self, self.throttle1, 0.4, False)
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList1[1])
                    print("Czujnik zajety: ", SensorsList1[1])
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList1[2])
                    print("Czujnik zajety: ", SensorsList1[2])
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[2], 1)#stop gora stacja
                    self.waitMsec(100)
                    print("Pociag towarowy powraca - warszawa wilenska")
                    backward_train()  # uruchom pociag towarowy do powrotu
                    print("Pociag towarowy powrocil - warszawa wilenska")
                    self.throttle1.setF18(True)# Zamykanie drzwi
                    self.waitMsec(4000)
                    self.throttle1.setF18(False)# Zamykanie drzwi
                    self.waitMsec(2000)
                    Kollib.drive_vehicle(self, self.throttle1, 0.4, False)
                    self.waitSensorActive(SensorsList1[3])
                    print("Czujnik zajety: ", SensorsList1[3])
                    Kollib.drive_vehicle(self, self.throttle1, 0.05, False)
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList1[4])
                    print("Czujnik zajety: ", SensorsList1[4])
                    self.waitMsec(100)
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[4], 400)
                    self.waitMsec(100)
                    self.throttle1.setF0(False)# Wylaczenie swiatel pociagu
                    self.waitMsec(100)
                    self.throttle1.setF3(False)# Opuść pantografy
                    self.waitMsec(1000)
                    return 0

            """Jedzie do przodu - wozek napedowy z przodu"""
            def forward_tram():
                print("STATE: ", SensorsList1[0].state)
                print("Inside handle(forward_tram)")
                self.throttle1.setSpeedSetting(0)  # Upewnia sie że kolejka jest zatrzymana
                self.waitMsec(500)
                if SensorsList1[4].state == ACTIVE:
                    print("STATE1: ", SensorsList1[4].state)
                    print("Czujnik zajety: ", SensorsList1[4])
                    self.waitMsec(100)
                    self.throttle1.setF3(True)# Unieś pantografy
                    self.waitMsec(1000)
                    self.throttle1.setF17(True)# Oświetlenie stacji docelowej pociagu
                    self.waitMsec(100)
                    self.throttle1.setF0(True)# Wlaczenie swiatel pociagu
                    self.waitMsec(100)
                    self.throttle1.setF18(True)# Zamykanie drzwi
                    self.waitMsec(4000)
                    self.throttle1.setF18(False)# Zamykanie drzwi
                    self.waitMsec(2000)
                    Kollib.drive_vehicle(self, self.throttle1, 0.4, True)
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList1[3])
                    print("Czujnik zajety: ", SensorsList1[3])
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList1[2])
                    print("Czujnik zajety: ", SensorsList1[2])
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[2], 1000)#stop gora stacja
                    self.waitMsec(2000)
                    print("Pociag towarowy wyrusza - warszawa bunkry")
                    forward_train()#uruchom pociag towarowy do powrotu
                    print("Pociag towarowy dojechal - warszawa bunkry")
                    self.throttle1.setF18(True)# Zamykanie drzwi
                    self.waitMsec(4000)
                    self.throttle1.setF18(False)# Zamykanie drzwi
                    self.waitMsec(2000)
                    Kollib.drive_vehicle(self, self.throttle1, 0.4, True)
                    self.waitSensorActive(SensorsList1[1])
                    print("Czujnik zajety: ", SensorsList1[1])
                    Kollib.drive_vehicle(self, self.throttle1, 0.1, True)
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList1[0])
                    print("Czujnik zajety: ", SensorsList1[0])
                    self.waitMsec(100)
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[0], 2000)
                    self.waitMsec(20000)
                    Kollib.drive_vehicle(self, self.throttle1, 0.05, True)
                    self.waitMsec(100)
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[0], 100)
                    self.waitMsec(100)
                    self.throttle1.setF0(False)# Wylaczenie swiatel pociagu
                    self.waitMsec(100)
                    self.throttle1.setF3(False)#Opuść pantografy
                    self.waitMsec(1000)
                    return 0



            """Jedzie do przodu - wozek napedowy z przodu"""
            def forward_train():
                print("STATE: ", SensorsList2[4].state)
                print("Inside handle(forward_tram)")
                self.throttle2.setSpeedSetting(0)  # Upewnia sie że kolejka jest zatrzymana
                self.waitMsec(500)
                if SensorsList2[4].state == ACTIVE:
                    print("STATE1: ", SensorsList2[4].state)
                    print("Czujnik zajety: ", SensorsList2[4])
                    self.waitMsec(100)
                    self.throttle2.setF0(True)# Zapal światła
                    self.waitMsec(100)
                    Kollib.drive_vehicle(self, self.throttle2, 0.6, True)
                    self.waitMsec(100)
                    self.throttle2.setF1(True)# wlacz dzwiek silnika
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList2[5])
                    print("Czujnik zajety: ", SensorsList2[5])
                    self.waitMsec(100)
                    self.throttle2.setF2(True)# wlacz klakson w tunelu
                    self.waitMsec(3000)
                    self.throttle2.setF2(False)# wylacz klakson w tunelu
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList2[6])
                    print("Czujnik zajety: ", SensorsList2[6])
                    self.waitMsec(100)
                    Kollib.drive_vehicle(self, self.throttle2, 0.4, True)
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList2[7])
                    print("Czujnik zajety: ", SensorsList2[7])
                    Kollib.drive_vehicle(self, self.throttle2, 0.2, True)
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList2[8])
                    print("Czujnik zajety: ", SensorsList2[8])
                    self.waitMsec(100)
                    self.waitMsec(100)
                    Kollib.delay_stop(self, self.throttle2, SensorsList2[8], 1000)
                    self.throttle2.setF0(False)# Zgaś światła
                    self.waitMsec(100)
                    self.throttle2.setF1(False)# wylacz dzwiek silnika
                    self.waitMsec(3000)
                    return 0

            def backward_train():
                print("STATE: ", SensorsList2[8].state)
                print("Inside handle(backward_train)")
                self.throttle2.setSpeedSetting(0)  # Upewnia sie że kolejka jest zatrzymana
                self.waitMsec(500)
                if SensorsList2[8].state == ACTIVE:
                    print("STATE1: ", SensorsList2[8].state)
                    print("Czujnik zajety: ", SensorsList2[4])
                    self.waitMsec(100)
                    self.throttle2.setF3(True)# wlacz stukanie narzedzi
                    self.waitMsec(5000)
                    self.throttle2.setF3(False)# wylacz stukanie narzedzi
                    self.waitMsec(100)
                    self.throttle2.setF1(True)# wlacz dzwiek silnika
                    self.waitMsec(100)
                    self.throttle2.setF0(True)# Zapal światła
                    self.waitMsec(100)
                    Kollib.drive_vehicle(self, self.throttle2, 0.5, False)
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList2[7])
                    print("Czujnik zajety: ", SensorsList2[7])
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList2[6])
                    print("Czujnik zajety: ", SensorsList2[6])
                    self.waitMsec(8000)
                    self.throttle2.setF2(True)# wlacz klakson w tunelu
                    self.waitMsec(3000)
                    self.throttle2.setF2(False)# wylacz klakson w tunelu
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList2[5])
                    print("Czujnik zajety: ", SensorsList2[5])
                    Kollib.drive_vehicle(self, self.throttle2, 0.4, False)
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList2[4])
                    print("Czujnik zajety: ", SensorsList2[4])
                    self.waitMsec(100)
                    Kollib.delay_stop(self, self.throttle2, SensorsList2[4], 500)
                    self.throttle2.setF0(False)# Zgaś światła
                    self.waitMsec(100)
                    self.throttle2.setF1(False)# wylacz dzwiek silnika
                    self.waitMsec(3000)
                    return 0


            """Uruchom odpowiednia funkcje zalezna od tego na ktorym torze krancowym sie znajduje"""
            if SensorsList1[0].state == ACTIVE and SensorsList2[8].state == ACTIVE:
                print("Uruchamian funkcje backward_tram")
                backward_tram()
            elif SensorsList1[4].state == ACTIVE and SensorsList2[4].state == ACTIVE:
                print("Uruchamian funkcje forward_tram")
                forward_tram()


lok2().start()

