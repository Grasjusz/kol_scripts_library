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

#Sekwencyjne przypisywanie adresów sensorą - trasa pociag osobowy
FirstSensorAdress = 16
NumberOfSensors = 6
SensorsList1 = []
for i in range(FirstSensorAdress, FirstSensorAdress + NumberOfSensors):
    SensorsList1.append(sensors.getSensor("LS"+str(i+1)))
#print("Sensor List 1:", SensorsList1)

#Wywolaj czujniki jako nieaktywne by je wzbudzić
activate_sensors(SensorsList1)

#Sekwencyjne przypisywanie adresów sensorą - trasa V20 towarowa
FirstSensorAdress = 22
NumberOfSensors = 9
SensorsList2 = []
for i in range(FirstSensorAdress, FirstSensorAdress + NumberOfSensors):
    SensorsList2.append(sensors.getSensor("LS"+str(i+1)))
#print("Sensor List 2:", SensorsList2)

#Wywolaj czujniki jako nieaktywne by je wzbudzić
activate_sensors(SensorsList2)

#Reczne przypisywanie adresów sensorą - zatoczka
Sensor32 = sensors.getSensor("LS32") #Mijanka/zatoczka na tramwaju
#print("Sensor mijanka/wahadlo:", Sensor32)

#Wywolaj czujniki jako nieaktywne by je wzbudzić
Sensor32.setState(INACTIVE)

#Sekwencyjne przypisywanie adresów zwrotnic
FirstTurnoutAdress = 100
NumberOfTurnouts = 4
TurnoutsList_BCD = []
for i in range(FirstTurnoutAdress, FirstTurnoutAdress + NumberOfTurnouts):
    TurnoutsList_BCD.append(turnouts.getTurnout("LT"+str(i)))
#print(TurnoutsList_BCD)

'''
Jeśli czujniki nie są ułożone w sekwencji, możesz dodać je jako Sensor1 = sensors.getSensor("LS1") lub
SensorsList.append(sensors.getSensor("LS" + str(1))), jeśli chcesz umieścić je w liście.

Jeśli to możliwe, dopisz taki sam algorytm dla innych elementów.

Jeśli dany sensor nie znajduje sie na liście sensorów w panelu "PanelPro" 
(jego wartość to None), skutkuje to wyłaczeniem watku w którym znajduje sie fukcja
odnoszaca sie do tego czujnika.
'''


class Lok2(jmri.jmrit.automat.AbstractAutomaton):

    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration.
        print("LOK2 Program wawa wilenska uruchomiony...  Czekam na sensor IS5 i IS6 ze skryptu startup..")
        self.waitMsec(6000)
        """Sensor wirtualny uruchamiajacy makiete - czekam na odpowiedz z startup_script.py"""
        self.startup_sensor_1 = sensors.getSensor("IS5")  # Pozycja startowa pociag pasazerski
        self.startup_sensor_2 = sensors.getSensor("IS6")  # Pozycja startowa pociag towarowy
        self.waitSensorActive([self.startup_sensor_1])
        self.waitSensorActive([self.startup_sensor_2])


        # get loco address. For long address change "False" to "True"
        self.throttle1 = self.getThrottle(3, False) #Pociag osobowy
        self.throttle2 = self.getThrottle(6, False) #V20, towarowy

    def handle(self):
        # handle() is called repeatedly until it returns false.
        print("LOK2 Program LOK2_HANDLE uruchomiony")

        while True:

            def check_stop():
                """Sensor wirtualny zatrzymujacy lub uruchamiajacy z powrotem makiete"""
                self.startup_sensor_1 = sensors.getSensor("IS5")  # Pozycja startowa pociag osobowy
                self.startup_sensor_2 = sensors.getSensor("IS6")  # Pozycja startowa pociag towarowy

                suspend_1 = self.waitSensorActive([self.startup_sensor_1])
                suspend_2 = self.waitSensorActive([self.startup_sensor_2])

                if suspend_1 == ACTIVE and suspend_2 == ACTIVE:
                    pass #kontynuuj program
                elif suspend_1 != ACTIVE and suspend_2 != ACTIVE:
                    print("LOK2 Pociagi zatrzymane LOK_2_wilenska")
                    Kollib.drive_vehicle(self, self.throttle1, 0, True) #zatrzymaj pociag osobowy i czekaj na zmiane sygnalu
                    Kollib.drive_vehicle(self, self.throttle2, 0, True) #zatrzymaj pociag towarowy i czekaj na zmiane sygnalu
                    print("LOK2 Pauza wlaczona..")
                return

            def turnouts_initial_positions():
                """Sprawdz czy zwrotnice sa w odpowiednim polozeniu i ustaw na pozycje startowe"""
                """#2 dla CLOSED, #4 dla THROW"""
                if TurnoutsList_BCD[0].getKnownState() == 2:
                    TurnoutsList_BCD[0].setState(4)
                    self.waitMsec(1000)
                    print("LOK2 Przestawiam zwrotnice na THROWN:", TurnoutsList_BCD[0], TurnoutsList_BCD[0].getKnownState())

                elif TurnoutsList_BCD[1].getKnownState() == 2:
                    TurnoutsList_BCD[1].setState(4)
                    self.waitMsec(1000)
                    print("LOK2 Przestawiam zwrotnice na THROWN:", TurnoutsList_BCD[1], TurnoutsList_BCD[1].getKnownState())

                elif TurnoutsList_BCD[2].getKnownState() == 2:
                    TurnoutsList_BCD[2].setState(4)
                    self.waitMsec(1000)
                    print("LOK2 Przestawiam zwrotnice na THROWN:", TurnoutsList_BCD[2], TurnoutsList_BCD[2].getKnownState())

                elif TurnoutsList_BCD[3].getKnownState() == 2:
                    TurnoutsList_BCD[3].setState(4)
                    self.waitMsec(1000)
                    print("LOK2 Przestawiam zwrotnice na THROWN:", TurnoutsList_BCD[3], TurnoutsList_BCD[3].getKnownState())

                TurnoutsList_BCD[0].setState(4)
                self.waitMsec(1000)
                print("LOK2 Przestawiam zwrotnice na THROWN:", TurnoutsList_BCD[0], TurnoutsList_BCD[0].getKnownState())
                TurnoutsList_BCD[1].setState(4)
                self.waitMsec(1000)
                print("LOK2 Przestawiam zwrotnice na THROWN:",TurnoutsList_BCD[1], TurnoutsList_BCD[1].getKnownState())
                TurnoutsList_BCD[2].setState(4)
                self.waitMsec(1000)
                print("LOK2 Przestawiam zwrotnice na THROWN:",TurnoutsList_BCD[2], TurnoutsList_BCD[2].getKnownState())
                TurnoutsList_BCD[3].setState(4)
                self.waitMsec(1000)
                print("LOK2 Przestawiam zwrotnice na THROWN:",TurnoutsList_BCD[3], TurnoutsList_BCD[3].getKnownState())
                return 0

            """Jedzie do tylu - wozek napedowy z przodu"""
            def backward_tram():
                #print("STATE: ", SensorsList1[0].state)
                print("LOK2 POCIAG OSOBOWY TRASA DO BUNKROW)")
                self.throttle1.setSpeedSetting(0)  # Upewnia sie że kolejka jest zatrzymana
                self.waitMsec(500)
                if SensorsList1[0].state == ACTIVE:
                    #print("Czujnik zajety: ", SensorsList1[0])
                    self.waitMsec(100)
                    self.throttle1.setF3(True)#Unieś pantografy
                    self.waitMsec(1000)
                    self.throttle1.setF6(True) # wlacz dzwiek silnika
                    self.waitMsec(3000)
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
                    #print("Czujnik zajety: ", SensorsList1[1])
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList1[2])
                    #print("Czujnik zajety: ", SensorsList1[2])
                    print("LOK2 Zatrzymanie na stacji 2 - BUNKRY TRASA DO BUNKROW")
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[2], 1)#stop gora stacja
                    self.waitMsec(100)
                    print("LOK2 Pociag towarowy powraca - warszawa wilenska")
                    backward_train()  # uruchom pociag towarowy do powrotu
                    print("LOK2 Pociag towarowy powrocil - warszawa wilenska")
                    self.throttle1.setF18(True)# Zamykanie drzwi
                    self.waitMsec(4000)
                    self.throttle1.setF18(False)# Zamykanie drzwi
                    self.waitMsec(2000)
                    print("LOK2 Start na stacji 2 - TRASA DO BUNKROW")
                    Kollib.drive_vehicle(self, self.throttle1, 0.4, False)
                    self.waitSensorActive(SensorsList1[3])
                    #print("Czujnik zajety: ", SensorsList1[3])
                    self.waitMsec(100)
                    Kollib.speed_change(self, self.throttle1, 0.4)
                    self.waitMsec(20000)
                    Kollib.speed_change(self, self.throttle1, 0.1)
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList1[4])
                    #print("Czujnik zajety: ", SensorsList1[4])
                    print("LOK2 Zatrzymanie na stacji 3 - TRASA DO BUNKROW")
                    self.waitMsec(100)
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[4], 100)
                    self.waitMsec(100)
                    self.throttle1.setF0(False)# Wylaczenie swiatel pociagu
                    self.waitMsec(100)
                    self.throttle1.setF3(False)# Opuść pantografy
                    self.waitMsec(1000)
                    self.throttle1.setF6(False) # wylacz dzwiek silnika
                    self.waitMsec(3000)
                    print("LOK2 KONIEC PETLI, ROZPOCZYNAM NOWA LOK_2_WAWA_WILENSKA")
                    return 0

            """Jedzie do przodu - wozek napedowy z przodu"""
            def forward_tram():
                #print("STATE: ", SensorsList1[0].state)
                print("LOK2 POCIAG OSOBOWY TRASA DO WAWA WILENSKA")
                self.throttle1.setSpeedSetting(0)  # Upewnia sie że kolejka jest zatrzymana
                self.waitMsec(500)
                if SensorsList1[4].state == ACTIVE:
                    #print("STATE1: ", SensorsList1[4].state)
                    #print("Czujnik zajety: ", SensorsList1[4])
                    self.waitMsec(100)
                    self.throttle1.setF3(True)# Unieś pantografy
                    self.waitMsec(1000)
                    self.throttle1.setF6(True) # wlacz dzwiek silnika
                    self.waitMsec(3000)
                    self.throttle1.setF17(True)# Oświetlenie stacji docelowej pociagu
                    self.waitMsec(100)
                    self.throttle1.setF0(True)# Wlaczenie swiatel pociagu
                    self.waitMsec(100)
                    self.throttle1.setF18(True)# Zamykanie drzwi
                    self.waitMsec(4000)
                    self.throttle1.setF18(False)# Zamykanie drzwi
                    self.waitMsec(2000)
                    print("LOK2 Start na stacji 3 - TRASA WAWA WILENSKA")
                    Kollib.drive_vehicle(self, self.throttle1, 0.4, True)
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList1[3])
                    #print("Czujnik zajety: ", SensorsList1[3])
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList1[2])
                    #print("Czujnik zajety: ", SensorsList1[2])
                    print("LOK2 Zatrzymanie na stacji 2 - TRASA WAWA WILENSKA")
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[2], 1000)#stop gora stacja
                    self.waitMsec(2000)
                    print("LOK2 Pociag towarowy wyrusza - trasa do warszawa bunkry")
                    forward_train()#uruchom pociag towarowy do powrotu
                    print("LOK2 Pociag towarowy dojechal - trasa do warszawa bunkry")
                    self.throttle1.setF18(True)# Zamykanie drzwi
                    self.waitMsec(4000)
                    self.throttle1.setF18(False)# Zamykanie drzwi
                    self.waitMsec(2000)
                    print("LOK2 Start na stacji 2 - TRASA WAWA WILENSKA")
                    Kollib.drive_vehicle(self, self.throttle1, 0.4, True)
                    self.waitSensorActive(SensorsList1[1])
                    #print("Czujnik zajety: ", SensorsList1[1])
                    Kollib.speed_change(self, self.throttle1, 0.3)
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList1[0])
                    #print("Czujnik zajety: ", SensorsList1[0])
                    print("LOK2 Zatrzymanie na stacji 1 - TRASA WAWA WILENSKA")
                    self.waitMsec(100)
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[0], 2000)
                    self.waitMsec(10000)
                    Kollib.drive_vehicle(self, self.throttle1, 0.1, True) #rusz do przodu aby wzbudzic czujnik
                    self.waitMsec(1500)
                    Kollib.delay_stop(self, self.throttle1, SensorsList1[0], 100)
                    self.waitMsec(100)
                    self.throttle1.setF0(False)# Wylaczenie swiatel pociagu
                    self.waitMsec(100)
                    self.throttle1.setF3(False)#Opuść pantografy
                    self.waitMsec(1000)
                    self.throttle1.setF6(False) # wylacz dzwiek silnika
                    self.waitMsec(3000)
                    print("LOK2 KONIEC PETLI, ROZPOCZYNAM NOWA LOK_2_WAWA_WILENSKA")
                    return 0

            """Jedzie do przodu - wozek napedowy z przodu"""
            def forward_train():
                #print("STATE: ", SensorsList2[4].state)
                print("LOK2 POCIAG TOWAROWY - TRASA DO BUNKRY")
                self.throttle2.setSpeedSetting(0)  # Upewnia sie że kolejka jest zatrzymana
                self.waitMsec(500)
                if SensorsList2[4].state == ACTIVE:
                    #print("STATE1: ", SensorsList2[4].state)
                    #print("Czujnik zajety: ", SensorsList2[4])
                    self.waitMsec(100)
                    self.throttle2.setF0(True)# Zapal światła
                    print("LOK2 Start na stacji 1 - TRASA DO BUNKRY")
                    self.throttle2.setF1(True) # wlacz dzwiek silnika
                    self.waitMsec(10000)
                    Kollib.drive_vehicle(self, self.throttle2, 0.5, True) #ustawienie predkosci
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList2[5])
                    #print("Czujnik zajety: ", SensorsList2[5])
                    self.waitMsec(100)
                    self.throttle2.setF2(True)# wlacz klakson w tunelu
                    self.waitMsec(4500)
                    self.throttle2.setF2(False)# wylacz klakson w tunelu
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList2[6])
                    #print("Czujnik zajety: ", SensorsList2[6])
                    self.waitMsec(100)
                    Kollib.speed_change(self, self.throttle2, 0.8) # zmiana iloczynu predkosci
                    self.waitMsec(2000)
                    Kollib.speed_change(self, self.throttle2, 0.7) # zmiana iloczynu predkosci
                    self.waitMsec(1500)
                    self.waitSensorActive(SensorsList2[7])
                    #print("Czujnik zajety: ", SensorsList2[7])
                    Kollib.speed_change(self, self.throttle2, 0.5)# zmiana iloczynu predkosci
                    self.waitMsec(3000)
                    Kollib.speed_change(self, self.throttle2, 0.3)# zmiana iloczynu predkosci
                    self.waitMsec(1500)
                    Kollib.speed_change(self, self.throttle2, 0.1)# zmiana iloczynu predkosci
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList2[8])
                    #print("Czujnik zajety: ", SensorsList2[8])
                    print("LOK2 Zatrzymanie na stacji 3 - TRASA DO BUNKRY")
                    self.waitMsec(100)
                    Kollib.delay_stop(self, self.throttle2, SensorsList2[8], 500)
                    self.throttle2.setF0(False)# Zgaś światła
                    self.waitMsec(100)
                    self.throttle2.setF1(False)# wylacz dzwiek silnika
                    self.waitMsec(3000)
                    return 0

            def backward_train():
                #print("STATE: ", SensorsList2[8].state)
                print("LOK2 POCIAG TOWAROWY - TRASA DO WAWA WILENSKA")
                self.throttle2.setSpeedSetting(0)  # Upewnia sie że kolejka jest zatrzymana
                self.waitMsec(500)
                if SensorsList2[8].state == ACTIVE:
                    #print("STATE1: ", SensorsList2[8].state)
                    #print("Czujnik zajety: ", SensorsList2[4])
                    self.waitMsec(100)
                    self.throttle2.setF3(True)# wlacz stukanie narzedzi
                    self.waitMsec(5000)
                    self.throttle2.setF3(False)# wylacz stukanie narzedzi
                    self.waitMsec(100)
                    self.throttle2.setF0(True)# Zapal światła
                    print("LOK2 Start na stacji 3 - TRASA WAWA WILENSKA")
                    self.waitMsec(100)
                    self.throttle2.setF1(True) # wlacz dzwiek silnika
                    self.waitMsec(10000)
                    Kollib.drive_vehicle(self, self.throttle2, 0.5, False)
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList2[7])
                    #print("Czujnik zajety: ", SensorsList2[7])
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList2[6])
                    #print("Czujnik zajety: ", SensorsList2[6])
                    self.waitMsec(4000)
                    self.throttle2.setF2(True)# wlacz klakson w tunelu
                    self.waitMsec(6000)
                    self.throttle2.setF2(False)# wylacz klakson w tunelu
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList2[5])
                    #print("Czujnik zajety:", SensorsList2[5])
                    self.waitMsec(100)
                    Kollib.drive_vehicle(self, self.throttle2, 0.4, False)
                    self.waitMsec(2000)
                    Kollib.drive_vehicle(self, self.throttle2, 0.3, False)
                    self.waitMsec(100)
                    self.waitSensorActive(SensorsList2[4])
                    #print("Czujnik zajety:", SensorsList2[4])
                    print("LOK2 Zatrzymanie na stacji 1 - TRASA WAWA WILENSKA")
                    self.waitMsec(100)
                    Kollib.drive_vehicle(self, self.throttle2, 0.1, False)
                    self.waitMsec(4000)
                    Kollib.delay_stop(self, self.throttle2, SensorsList2[4], 500)
                    self.throttle2.setF0(False) #Zgaś światła
                    self.waitMsec(100)
                    self.throttle2.setF1(False) #wylacz dzwiek silnika
                    self.waitMsec(3000)
                    return 0

            """Uruchom odpowiednia funkcje zalezna od tego na ktorym torze krancowym sie znajduje"""
            if SensorsList1[0].state == ACTIVE and SensorsList2[8].state == ACTIVE:
                print("LOK2 Sprawdz czy pauza..")
                check_stop()
                print("LOK2 Uruchamiam funkcje resetujaca zwrotnice")
                turnouts_initial_positions()
                print("LOK2 Uruchamiam funkcje backward_tram")
                backward_tram()
            elif SensorsList1[4].state == ACTIVE and SensorsList2[4].state == ACTIVE:
                print("LOK2 Uruchamiam funkcje resetująca zwrotnice")
                turnouts_initial_positions()
                print("LOK2 Uruchamiam funkcje forward_tram")
                forward_tram()


Lok2().start()

