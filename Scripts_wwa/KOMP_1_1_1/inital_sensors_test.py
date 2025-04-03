import jarray
import jmri
import sys, os
#Pobiera relatywną ścieżkę do skryptu (czyli przeszukuje katalog główny w ktorym jest uruchamiany skrypt)
sys.path.append(os.path.join(sys.path[0]))
import Kollib #Biblioteka autorskich funkcji

#Sekwencyjne przypisywanie adresów sensorą
FirstSensorAdress = 34 #Wpisz numer pierwszego czujnika danej sekcji
NumberOfSensors = 16 #wpisz ilość czujników (-1 pierwszy wpisany wyżej)
SensorsList = []
for i in range(FirstSensorAdress, FirstSensorAdress + NumberOfSensors):
    SensorsList.append(sensors.getSensor("LS"+str(i-1)))
print(SensorsList)