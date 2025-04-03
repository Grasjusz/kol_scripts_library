import jarray
import jmri
import sys
# Dodaj ścieżkę do katalogu, w którym znajduje się biblioteka Kollib.py
sys.path.append(r'C:\Users\dawid\JMRI\Komp_3_Warszawa.jmri\Skrypty')
from Scripts_wwa.KOMP_1 import Kollib

#Sekwencyjne przypisywanie adresów sensorą 
FirstSensorAdress = 73
NumberOfSensors = 16
SensorsList_MAK = []
for i in range(FirstSensorAdress, FirstSensorAdress + NumberOfSensors):
    SensorsList_MAK.append(sensors.getSensor("LS"+str(i)))
print(SensorsList_MAK)

FirstSensorAdress = 97
NumberOfSensors = 16
SensorsList_OBR = []
for i in range(FirstSensorAdress, FirstSensorAdress + NumberOfSensors):
    SensorsList_OBR.append(sensors.getSensor("LS"+str(i)))
print(SensorsList_OBR)



class obrotnica_wwa(jmri.jmrit.automat.AbstractAutomaton):     
    def init(self):
        self.throttle = self.getThrottle(6, False)
        self.koniec_bcd = sensors.getSensor("koniec_bcd")
        print "wyjscie z init obrotnica"
        return
    def handle(self):
        self.waitMsec(10)
        self.throttle.setIsForward(True) # 
        self.throttle.setSpeedSetting(0)
        self.throttle.setF0(True)
        self.waitMsec(100)
        print (SensorsList_OBR[10])
        print "przed biblioteka"
        Kollib.flag_obrot_rampa(SensorsList_MAK[1], SensorsList_OBR[13], SensorsList_OBR[14], SensorsList_OBR[15], TurnoutsList_BCD[7])
        self.waitMsec(500)
        execfile(jmri.util.FileUtil.getExternalFilename("scripts:reset_bcd.py"))
        self.waitMsec(100)
        execfile(jmri.util.FileUtil.getExternalFilename("scripts:obrot_kombinacja_12.py"))
        self.waitMsec(100)
        self.waitSensorActive([self.koniec_bcd])
        self.waitMsec(1000)
        self.waitSensorActive([self.zez_na_ruch])
        Kollib.drive_vehicle(self, 0.2, True)
        self.waitMsec(1000)
        Kollib.delay_stop(self, SensorsList_OBR[15], 1000)
        
       
        print "wykonany program z biblioteki"
        return 0

obrotnica_wwa().start()
