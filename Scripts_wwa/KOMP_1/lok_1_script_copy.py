import jarray
import jmri
import sys, os

# Dodaj ścieżke do katalogu, w którym znajduje sie biblioteka Kollib.py
sys.path.append(os.path.join(sys.path[0])) #szuka biblioteczki w tym samym folderze w ktorym jest uruchamiany skrypt
import Kollib #Biblioteka autorskich funkcji

#Sekwencyjne przypisywanie adresów sensorą - trasa tramwaj
FirstSensorAdress = 0
NumberOfSensors = 7
SensorsList1 = []
for i in range(FirstSensorAdress, FirstSensorAdress + NumberOfSensors):
    SensorsList1.append(sensors.getSensor("LS"+str(i+1)))
print("Sensor List 1:", SensorsList1)

#Wywolaj czujniki jako nieaktywne by je wzbudzić
def activate_sensors(sensors_list):
    for sensor in sensors_list:
        sensor.setState(INACTIVE)

activate_sensors(SensorsList1)

'''
Jeśli czujniki nie są ułożone w sekwencji, możesz dodać je jako Sensor1 = sensors.getSensor("LS1") lub
SensorsList.append(sensors.getSensor("LS" + str(1))), jeśli chcesz umieścić je w liście.

Jeśli to możliwe, dopisz taki sam algorytm dla innych elementów.

Jeśli dany sensor nie znajduje sie na liście sensorów w panelu "PanelPro" 
(jego wartość to None), skutkuje to wyłaczeniem watku w którym znajduje sie fukcja
odnoszaca sie do tego czujnika.
'''


class Lok1(jmri.jmrit.automat.AbstractAutomaton):

    def init(self):
        # init() is called exactly once at the beginning to do
        # any necessary configuration.
        print("Inside init(self)")
        print("Program tramwaj burza uruchomiony...  Czekam na sensor IS1.. ze skryptu startup..")
        self.waitMsec(3000)
        """Sensor wirtualny uruchamiajacy makiete - czekam na odpowiedz z startup_script.py"""
        self.startup_sensor = sensors.getSensor("IS1")  # Pozycja startowa tramwaj burza
        self.waitSensorActive([self.startup_sensor])

        # get loco address. For long address change "False" to "True"
        self.throttle1 = self.getThrottle(10, False) #Tramwaj
        return

    def handle(self):
        # handle() is called repeatedly until it returns false.
        print("Inside handle(self)")

        speed_global = 0.4 # Ustawiamy jedną zmienna glowna prędkosc

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
                        self.waitMsec(10000)
                        pass
            pass

        if SensorsList1[0].state != ACTIVE:
            if SensorsList1[1].state != ACTIVE:
                print("Pociag nie na stacji startowej - uruchamiam funkcje jedz do stacji startowej")
                drive_to_start_station()
                print("Pociag na stacji startowej - przechodze do wlasciwego programu")
                pass

        elif SensorsList1[0].state == ACTIVE:
            if SensorsList1[1].state == ACTIVE:
                print("Podlacz zasilanie w 15 sekund lub zresetuj zasilanie makiety")
                print("Skrypt uruchomiony przed uruchomieniem zasilania - uruchamiam funkcje jedz do stacji startowej")
                self.waitMsec(15000)
                print("Czas minal! uruchamiam skrypt normalnie! - mozliwosc awarii!")
                drive_to_start_station()
                print("Pociag na stacji startowej - przechodze do wlasciwego programu")
                pass

        else:
            drive_to_start_station()

        while True:
            def check_stop():
                """Sensor wirtualny zatrzymujacy lub uruchamiajacy z powrotem makiete"""
                self.startup_sensor = sensors.getSensor("IS1")  # Pozycja startowa tramwaj burza
                suspend = self.waitSensorActive([self.startup_sensor])

                if suspend == ACTIVE:
                    pass
                elif suspend != ACTIVE:
                    print("Pociagi zatrzymane LOK_1_burza")
                    Kollib.drive_vehicle(self, self.throttle1, 0, True)
                return

            def driving_loop():
                """Jedzie do przodu - wozek napedowy z przodu"""
                print("STATE: ", SensorsList1[0].state)
                print("Uruchom pociag w normalnym stanie")
                self.throttle1.setSpeedSetting(0)  # Upewnia sie że kolejka jest zatrzymana
                self.waitMsec(1000)
                print("Czujnik zajety: ", SensorsList1[0])
                self.waitMsec(100)
                print("Zatrzymanie na stacji 1 PETLA OK")
                self.waitMsec(100)
                self.throttle1.setF1(False)  # wylacz dzwiek silnika
                self.waitMsec(6000)
                print("Start ze stacji 1 FORWARD")
                self.throttle1.setF1(True)  # wlacz dzwiek silnika
                self.waitMsec(6000)
                self.throttle1.setF0(True)  # Zapal światła
                self.waitMsec(100)
                self.throttle1.setF4(True)  # Wlacz dzwonek przed ruszeniem
                self.waitMsec(100)
                self.throttle1.setF4(False)  # Wylacz dzwonek przed ruszeniem
                self.waitMsec(4000)
                self.throttle1.setF2(True)  # Wlacz trabnij przed ruszeniem
                self.waitMsec(1000)
                self.throttle1.setF2(False)  # Wylacz trabnij przed ruszeniem
                self.waitMsec(100)
                Kollib.drive_vehicle(self, self.throttle1, speed_global, True)

                self.waitSensorActive(SensorsList1[1])
                print("Czujnik zajety: ", SensorsList1[1])
                self.waitMsec(100)
                print("Zatrzymanie na stacji 2 FORWARD")
                Kollib.delay_stop(self, self.throttle1, SensorsList1[1], 100)
                Kollib.stop_at_station(self, self.throttle1, SensorsList1[1], 6000)
                print("Start ze stacji 2 FORWARD")
                self.throttle1.setF4(True)  # Wlacz dzwonek przed ruszeniem
                self.waitMsec(100)
                self.throttle1.setF4(False)  # Wylacz dzwonek przed ruszeniem
                self.waitMsec(4000)
                self.throttle1.setF2(True)  # Wlacz trabnij przed ruszeniem
                self.waitMsec(1000)
                self.throttle1.setF2(False)  # Wylacz trabnij przed ruszeniem
                self.waitMsec(100)
                Kollib.drive_vehicle(self, self.throttle1, speed_global, True)

                self.waitSensorActive(SensorsList1[2])
                print("Czujnik zajety: ", SensorsList1[2])
                self.waitMsec(100)
                print("Zatrzymanie na stacji 3 FORWARD")
                Kollib.delay_stop(self, self.throttle1, SensorsList1[2], 100)
                Kollib.stop_at_station(self, self.throttle1, SensorsList1[2], 6000)
                print("Start ze stacji 3 FORWARD")
                self.throttle1.setF4(True)  # Wlacz dzwonek przed ruszeniem
                self.waitMsec(100)
                self.throttle1.setF4(False)  # Wylacz dzwonek przed ruszeniem
                self.waitMsec(4000)
                self.throttle1.setF2(True)  # Wlacz trabnij przed ruszeniem
                self.waitMsec(1000)
                self.throttle1.setF2(False)  # Wylacz trabnij przed ruszeniem
                self.waitMsec(100)
                Kollib.drive_vehicle(self, self.throttle1, speed_global, True)

                self.waitSensorActive(SensorsList1[3])
                print("Czujnik zajety: ", SensorsList1[3])
                self.waitMsec(100)
                print("Przejscie dla pieszych")
                self.throttle1.setF2(True)  # Wlacz trabnij przed przejsciem
                self.waitMsec(1000)
                self.throttle1.setF2(False)  # Wylacz trabnij przed przejsciem
                self.waitMsec(100)
                Kollib.speed_change(self, self.throttle1, 0.7)
                self.waitMsec(3000)
                Kollib.drive_vehicle(self, self.throttle1, speed_global, True)

                self.waitSensorActive(SensorsList1[4])
                print("Czujnik zajety: ", SensorsList1[4])
                self.waitMsec(100)
                print("Przejscie dla pieszych")
                self.throttle1.setF2(True)  # Wlacz trabnij przed przejsciem
                self.waitMsec(1000)
                self.throttle1.setF2(False)  # Wylacz trabnij przed przejsciem
                self.waitMsec(100)
                Kollib.speed_change(self, self.throttle1, 0.7)
                self.waitMsec(3000)
                Kollib.drive_vehicle(self, self.throttle1, speed_global, True)

                self.waitSensorActive(SensorsList1[5])
                print("Czujnik zajety: ", SensorsList1[5])
                self.waitMsec(100)
                print("Skrzyżowanie")
                Kollib.speed_change(self, self.throttle1, 0.7)
                self.throttle1.setF2(True)  # Wlacz trabnij przed przejsciem
                self.waitMsec(1000)
                self.throttle1.setF2(False)  # Wylacz trabnij przed przejsciem
                self.waitMsec(100)
                Kollib.drive_vehicle(self, self.throttle1, speed_global, True)

                self.waitSensorActive(SensorsList1[6])
                print("Czujnik zajety: ", SensorsList1[6])
                self.waitMsec(100)
                print("Zatrzymanie na stacji 4 FORWARD")
                Kollib.delay_stop(self, self.throttle1, SensorsList1[6], 100)
                Kollib.stop_at_station(self, self.throttle1, SensorsList1[6], 6000)
                print("Start ze stacji 4 FORWARD")
                self.throttle1.setF4(True)  # Wlacz dzwonek przed ruszeniem
                self.waitMsec(100)
                self.throttle1.setF4(False)  # Wylacz dzwonek przed ruszeniem
                self.waitMsec(4000)
                self.throttle1.setF2(True)  # Wlacz trabnij przed ruszeniem
                self.waitMsec(1000)
                self.throttle1.setF2(False)  # Wylacz trabnij przed ruszeniem
                self.waitMsec(100)
                Kollib.drive_vehicle(self, self.throttle1, speed_global, True)
                self.waitMsec(5000)
                Kollib.speed_change(self, self.throttle1, 0.7)

                self.waitSensorActive(SensorsList1[0])
                print("Czujnik zajety: ", SensorsList1[0])
                self.waitMsec(100)
                print("Zatrzymanie na stacji 1 - koniec petli")
                Kollib.delay_stop(self, self.throttle1, SensorsList1[0], 500)
                self.waitMsec(100)
                self.throttle1.setF1(False)  # wylacz dzwiek silnika
                self.waitMsec(6000)
                print("KONIEC PETLI, ROZPOCZYNAM NOWA LOK_1_BURZA")
                return

            check_stop()
            driving_loop()


Lok1().start()

