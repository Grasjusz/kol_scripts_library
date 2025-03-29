import jarray
import jmri
import sys

# Dodajemy ścieżkę do katalogu z plikiem Kollib.py, który zawiera autorskie funkcje pomocnicze.
sys.path.append(r'C:\Users\LOK_7\JMRI\My_JMRI_Railroad.jmri\MyScrypt')
import Kollib  # Import biblioteki użytkownika z dodatkowymi funkcjami

# Sekwencyjne przypisywanie adresów sensorów
FirstSensorAdress = x  # Początkowy adres pierwszego sensora (x)
NumberOfSensors = n  # Liczba sensorów do przypisania
SensorsList = []  # Lista, która będzie przechowywać sensory

# Dodajemy sensory do listy, ale sprawdzamy, czy dany sensor istnieje
for i in range(FirstSensorAdress, FirstSensorAdress + NumberOfSensors):
    sensor = sensors.getSensor("LS" + str(i))  # Pobieramy sensor o nazwie np. LS1, LS2...
    if sensor is not None:  # Jeśli sensor istnieje
        SensorsList.append(sensor)  # Dodajemy go do listy
    else:  # Jeśli sensor nie istnieje
        print(f"Sensor LS{i} nie został znaleziony.")  # Wypisujemy ostrzeżenie
print(SensorsList)  # Drukowanie listy sensorów do sprawdzenia

# Sekwencyjne przypisywanie adresów zwrotnic (turnouts)
# Zmienna `y` to pierwszy adres zwrotnicy w sekwencji
FirstTurnoutAdress = y
# Liczba zwrotnic do przypisania
NumberOfTurnouts = m
# Lista przechowująca obiekty zwrotnic
TurnoutsList = []
# Pętla iteruje przez kolejne wartości adresów zwrotnic i tworzy ich listę
for i in range(FirstTurnoutAdress, FirstTurnoutAdress + NumberOfTurnouts):
    TurnoutsList.append(turnouts.getTurnout("LT" + str(i)))  # Tworzenie adresu zwrotnicy np. LT1, LT2...
print(TurnoutsList)  # Drukowanie listy zwrotnic do sprawdzenia

'''
Jeśli czujniki (sensory) nie są ułożone w sekwencji, możesz dodać je ręcznie:
    Sensor1 = sensors.getSensor("LS1")
lub dopisywać je pojedynczo do listy:
    SensorsList.append(sensors.getSensor("LS" + str(1)))

Jeśli w projekcie istnieją inne grupy urządzeń (np. sygnały świetlne), można dopisać
analogiczne algorytmy jak dla sensorów czy zwrotnic.

UWAGA: Jeśli sensor zwróci wartość `None` (nie znajduje się w liście sensorów programu PanelPro),
spowoduje to wyłączenie wątku, który odwołuje się do tego czujnika. Dlatego należy sprawdzić listę
czujników przed użyciem w kodzie.
'''


# Definicja klasy dziedziczącej po AbstractAutomaton, odpowiedzialnej za automatyczne działanie systemu
class kolejka_test(jmri.jmrit.automat.AbstractAutomaton):

    def init(self):
        """
        Funkcja init() wywoływana jest jednorazowo na początku działania klasy.
        Służy do inicjalizacji zmiennych i konfiguracji systemu.
        """
        print
        "Inside init(self)"  # Informacja o rozpoczęciu procesu inicjalizacji

        # Pobranie sterowania dla lokomotywy o określonym adresie
        # Pierwszy argument to adres lokomotywy na dekoderze DCC
        # Drugi argument określa, czy adres lokomotywy jest "długi" (True) czy "krótki" (False)
        self.Lokomtywa_1 = self.getThrottle(7, False)  # Lokomotywa o adresie 7 (krótki adres)
        self.Lokomtywa_2 = self.getThrottle(3, False)  # Lokomotywa o adresie 3

        """
        Tutaj można dodać dodatkowe zmienne lub kroki inicjalizacji np. ustawienia stanów początkowych.
        """
        return

    def handle(self):
        """
        Funkcja handle() działa w pętli i jest wywoływana cyklicznie.
        Dopóki zwraca wartość 1 (True), pętla nie kończy działania.
        """
        print
        "Inside handle(self)"  # Informacja o rozpoczęciu obsługi pętli

        print
        "Start of Loop"  # Początek pętli działania

        # Przykład obsługi lokomotywy w celu zatrzymania jej ruchu
        print
        "Tramwaj_1"
        self.Lokomtywa_1.setSpeedSetting(0)  # Ustawienie prędkości lokomotywy na 0 (zatrzymanie)

        print
        "End of Loop"  # Koniec cyklu pętli
        # Funkcja zwraca 1, dzięki czemu pętla automatyki będzie kontynuowana
        return 1


# Uruchomienie automatu
kolejka_test().start()
