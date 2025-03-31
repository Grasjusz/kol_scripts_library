'''
Autorska biblioteka z funkcjami do sterowania pojazdami i elementami infrastruktury kolejowej (np. zwrotnicami).
'''

'''
UWAGA: Zmienna "station" odnosi się do czujników stacji, ponieważ użycie nazwy "sensor" powoduje konflikt z biblioteką JMRI.
Każda funkcja jest odpowiedzialna za jedną operację (np. zatrzymanie pojazdu, zmiana prędkości, ustawienie kierunku).
'''


def stop_at_station(self, vehicle, station, delay):
    """
    Zatrzymuje pojazd na wskazanej stacji i wstrzymuje jego ruch na określony czas.

    - Funkcja oczekuje na aktywację podanego czujnika (stacji).
    - Po aktywacji zatrzymuje pojazd (prędkość = 0).
    - Następnie wykonuje opóźnienie zgodnie z wartością parametru "delay".

    :param vehicle: Obiekt pojazdu, który ma zostać zatrzymany.
    :param station: Czujnik związany z daną stacją, który należy monitorować.
    :param delay: Czas (w milisekundach), przez który pojazd pozostaje zatrzymany na stacji.
    :return: None
    """
    # Oczekiwanie na aktywację czujnika stacji
    print "stop_at_station:Wait for Sensor", station, vehicle
    self.waitSensorActive([station])

    # Zatrzymanie pojazdu
    print "stop_at_station:Stop on Station", station, vehicle
    vehicle.setSpeedSetting(0)
    self.waitMsec(100)
    vehicle.setSpeedSetting(0)
    self.waitMsec(100)
    # Opóźnienie dla dodatkowego odczekania na stacji
    print "stop_at_station:Delay"
    self.waitMsec(delay)
    self.waitMsec(500)


def drive_vehicle(self, vehicle, speed, is_forward):
    """
    Ustawia kierunek jazdy pojazdu oraz jego prędkość.

    - Funkcja służy do rozpoczęcia ruchu pojazdu z określoną prędkością.
    - Określany jest kierunek (do przodu lub wstecz) za pomocą flagi "is_forward".
    - Prędkość jest ustawiana na wartość z parametru "speed".

    :param vehicle: Obiekt pojazdu, który chcemy sterować.
    :param speed: Docelowa prędkość pojazdu.
    :param is_forward: Flaga określająca kierunek jazdy (True = do przodu, False = wstecz).
    :return: None
    """
    # Ustawienie kierunku jazdy pojazdu
    print "drive_vehicle:Set Loco Direction", vehicle, is_forward
    vehicle.setIsForward(is_forward)
    self.waitMsec(500)
    print "drive_vehicle:Set Speed", vehicle, speed
    # Ustawienie prędkości
    vehicle.setSpeedSetting(speed)
    self.waitMsec(100)


def delay_stop(self, vehicle, station, delay):
    """
    Powoduje zatrzymanie pojazdu po określonym czasie od aktywacji czujnika stacji.

    - Monitoruje aktywację czujnika stacji.
    - Po aktywacji powoduje krótki postój (delay), po czym zatrzymuje pojazd.

    :param vehicle: Obiekt pojazdu, który ma zostać zatrzymany.
    :param station: Czujnik stacji, który należy monitorować.
    :param delay: Długość oczekiwania (w milisekundach) po aktywacji czujnika przed zatrzymaniem pojazdu.
    :return: None
    """
    # Czekanie na aktywację czujnika stacji
    print "delay_stop:Wait for Sensor", station, vehicle
    self.waitSensorActive([station])

    # Opóźnienie przed zatrzymaniem
    print "delay_stop:Delay"
    self.waitMsec(delay)
    print "delay_stop:Stop"
    # Zatrzymanie pojazdu
    vehicle.setSpeedSetting(0)
    self.waitMsec(100)
    vehicle.setSpeedSetting(0)


def speed_change(self, vehicle, speed_multiplier):
    """
    Zmienia prędkość pojazdu mnożąc jego aktualną prędkość przez podany mnożnik.

    - Funkcja przydatna w sytuacjach, gdy trzeba zmodyfikować prędkość na podstawie czynnika zewnętrznego.

    :param vehicle: Obiekt pojazdu, którego prędkość ma być zmieniona.
    :param speed_multiplier: Mnożnik prędkości (np. 0.5 dla zmniejszenia o połowę lub 2 dla podwojenia prędkości).
    :return: None
    """
    # Odczytanie aktualnej prędkości
    current_speed = vehicle.getSpeedSetting()

    # Zmiana prędkości na podstawie mnożnika
    vehicle.setSpeedSetting(current_speed * speed_multiplier)
    self.waitMsec(1000)


def sc_station(self, vehicle, station, speed_multiplier):
    """
    Modyfikuje prędkość pojazdu po wykryciu aktywacji czujnika stacji.

    - Funkcja monitoruje czujnik stacji.
    - Jeśli czujnik zostanie aktywowany, zmienia prędkość pojazdu zgodnie z podanym mnożnikiem.
    - Ważne w przypadku dynamicznych zmian prędkości w odpowiedzi na zdarzenia.

    :param vehicle: Obiekt pojazdu, który ma reagować na aktywację stacji.
    :param station: Czujnik monitorowany przez funkcję.
    :param speed_multiplier: Mnożnik zmieniający prędkość pojazdu (np. 2 dla dwukrotnego przyspieszenia, 0.5 dla spowolnienia).
    :return: None
    """
    # Oczekiwanie na aktywację czujnika stacji
    self.waitSensorActive([station])

    # Zmiana prędkości z uwzględnieniem mnożnika
    current_speed = vehicle.getSpeedSetting()
    vehicle.setSpeedSetting(current_speed * speed_multiplier)
    self.waitMsec(1000)


def revers_turnouts(self, zwrotnica):
    """
    Zmienia stan wskazanej zwrotnicy na stan przeciwny.

    - Funkcja obsługuje przełączanie zwrotnic w dwie strony:
        1) Jeśli zwrotnica w stanie "2", przełącza na stan "4".
        2) Jeśli zwrotnica w stanie "4", przełącza na stan "2".
    - Używana w przypadkach, kiedy chcemy zmienić kierunek ruchu pociągu.

    :param zwrotnica: Obiekt sterujący zwrotnicą.
    :return: None
    """
    # Sprawdzenie bieżącego stanu zwrotnicy i przełączenie na stan przeciwny
    if zwrotnica.getKnownState() == 2:
        zwrotnica.setState(4)
        self.waitMsec(100)
    elif zwrotnica.getKnownState() == 4:
        zwrotnica.setState(2)
        self.waitMsec(100)'''
Autorska biblioteka z kolejkowymi funkcjami
'''

'''
Zmienna station tyczy sie kazdego czujnika poniewarz
zmiena o nazwie sensor powoduje konflikt z bibliotekom JMRI
'''

def stop_at_station(self, vehicle, station, delay):
    """
    Stops the vehicle at the specified station and waits for the given delay.

    :param self:
    :param vehicle: The vehicle object to be stopped.
    :param station: The station sensor to interact with.
    :param delay: The time in milliseconds the vehicle should remain stopped.
    :return: None
    """
    print(vehicle)
    self.waitSensorActive([station])
    print "stop_at_station:Stop on Station"
    vehicle.setSpeedSetting(0)# Stop the vehicle
    self.waitMsec(100)
    vehicle.setSpeedSetting(0)
    print "stop_at_station:Delay"
    self.waitMsec(delay)
    self.waitMsec(500)



def drive_vehicle(self, vehicle, speed, is_forward):
    """
    Drives a vehicle by setting its forward direction and speed.

    :param vehicle: The vehicle instance to be controlled.
    :param speed: The speed setting to apply to the vehicle after direction
        synchronization.
    :param is_forward: A flag indicating whether the vehicle should move
        forward (True) or not (False).
    :return: None
    """
    # set loco to forward
    print(vehicle)
    print "drive_vehicle:Set Loco Direction"
    print(is_forward)
    vehicle.setIsForward(is_forward)
    self.waitMsec(500)
    print "drive_vehicle:Set Speed"
    vehicle.setSpeedSetting(speed)
    self.waitMsec(100)
    vehicle.setSpeedSetting(speed)
    self.waitMsec(500)


def delay_stop(self, vehicle,station,delay):
    """
    Causes the vehicle to wait a given delay before stopping.

    :param self:
    :param vehicle: The controlled vehicle object providing methods for sensor interaction and throttle control.
    :param station: The sensor station at which the vehicle should wait.
    :param delay: Time in milliseconds for which the vehicle should pause after activating the sensor.
    :return: None
    """
    print(vehicle)
    print "delay_stop:White for sensor"
    self.waitSensorActive([station])
    print "delay_stop:White to stop"
    self.waitMsec(delay)
    print "delay_stop:Stop"
    vehicle.setSpeedSetting(0)
    self.waitMsec(100)
    vehicle.setSpeedSetting(0)
    self.waitMsec(1000)


def speed_change(self, vehicle, speed_multiplier):
    print(vehicle)
    print "speed_change:Changing speed"
    curent_speed=vehicle.getSpeedSetting()
    self.waitMsec(500)
    vehicle.setSpeedSetting(curent_speed * speed_multiplier)
    self.waitMsec(1000)

def sc_station(self, vehicle,station,speed_multiplier):#sc->speed change
    """
    Modifies the speed of the vehicle when a specific station sensor is activated. This function first waits for
    the designated sensor at the station to become active. After confirming the sensor activation, the function
    retrieves the current speed setting of the vehicle, applies the provided multiplier to the speed setting, and
    updates the vehicle's throttle to reflect the new speed. It ensures a delay both after the sensor is sensed
    and after the new speed is set.

    :param vehicle: The vehicle object that interacts with the station and its throttle is updated accordingly.
    :param station: The identifier of the station whose sensor is being monitored for activation.
    :param speed_multiplier: A multiplier value to adjust the speed of the vehicle upon station sensor activation.
    :return: None
    """
    print(vehicle)
    self.waitSensorActive([station])
    print "sc_station:White for sensor"
    curent_speed=vehicle.getSpeedSetting()
    self.waitMsec(500)
    print "sc_station:Changing speed"
    vehicle.setSpeedSetting(curent_speed * speed_multiplier)
    self.waitMsec(1000)

def revers_turnouts(self, zwrotnica):
    print "Zmiana położenia zwrotnicy"
    if zwrotnica.getKnownState() == 2 :
        zwrotnica.setState(4)
        self.waitMsec(100)
        zwrotnica.setState(4)
        print(zwrotnica.getKnownState())
    if zwrotnica.getKnownState() == 4:
        zwrotnica.setState(2)
        self.waitMsec(100)
        zwrotnica.setState(2)
        print(zwrotnica.getKnownState())


