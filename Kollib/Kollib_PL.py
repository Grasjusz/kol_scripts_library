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
    self.waitMsec(100)