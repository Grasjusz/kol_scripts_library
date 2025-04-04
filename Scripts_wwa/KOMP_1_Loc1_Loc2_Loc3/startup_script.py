import jarray
import jmri
import os


class Start(jmri.jmrit.automat.AbstractAutomaton):

    def init(self):
        print("Uruchamiam makiete.. Czekaj..")
        self.LS1 = sensors.getSensor("LS1")  # Pozycja startowa tramwaj burza
        self.LS17 = sensors.getSensor("LS17")  # Pozycja startowa pociag dlugi wawa wilenska
        self.LS31 = sensors.getSensor("LS31")  # Pozycja startowa pociag towarowy bunkier
        self.LS33 = sensors.getSensor("LS33")  # Pozycja startowa 0 tramwaj wisla
        self.LS42 = sensors.getSensor("LS42")  # Pozycja startowa 1 tramwaj wisla

        # Initializuje wirtualne czujniki "switche on/off"
        self.tram_storm_init = sensors.getSensor("IS1")
        self.tram_visla_bridge_init = sensors.getSensor("IS2")
        self.tram_visla_init = sensors.getSensor("IS3")
        self.br80_init = sensors.getSensor("IS4")
        self.v20_init = sensors.getSensor("IS5")
        self.train_long_init = sensors.getSensor("IS6")

        #Initializuje lokomotywy
        self.tram_storm = self.getThrottle(10, False)  # tramwaj burza adr 10
        self.tram_visla = self.getThrottle(11, False)  # tramwaj wisla adr 11
        self.tram_visla_bridge = self.getThrottle(12, False)  # tramwaj most1 wisla adr 12
        self.tram_visla_bridge_2 = self.getThrottle(13, False)  # tramwaj most2 wisla adr 13
        self.train_long = self.getThrottle(3, False)  # pociag osobowy adr 3
        self.br80 = self.getThrottle(5, False)  # BR80 adr 5
        self.V20 = self.getThrottle(6, False)  # V20020 adr 6
        return

    def handle(self):
        # Definiowanie poszczególnych elementów ścieżki do pliku - w celu dostosowania pod wlasne potrzeby
        user_folder = "C:\\Users\\LOK_1"
        jmri_folder = "JMRI"
        file_name_LOK_1 = "lok_1_end_day_initial_position.py"  # nazwa pliku do otwarcia
        file_name_LOK_2 = "lok_2_end_day_initial_position.py"  # nazwa pliku do otwarcia
        file_name_LOK_3 = "lok_3_end_day_initial_position.py"  # nazwa pliku do otwarcia

        # Tworzenie pełnej ścieżki za pomocą os.path.join
        file_path_LOK_1_emergency = os.path.join(user_folder, jmri_folder, "LOK_1.jmri", "scripting", file_name_LOK_1)
        file_path_LOK_2_emergency = os.path.join(user_folder, jmri_folder, "LOK_1.jmri", "scripting", file_name_LOK_2)
        file_path_LOK_3_emergency = os.path.join(user_folder, jmri_folder, "LOK_1.jmri", "scripting", file_name_LOK_3)

        #Resetuje zasilanie jesli wlaczone, jesli nie, uruchamia i daje czas na realizacje czujnikow
        print("Uruchamiam zasilanie...")
        powermanager.setPower(jmri.PowerManager.OFF)
        self.waitMsec(3000)
        powermanager.setPower(jmri.PowerManager.IDLE)
        self.waitMsec(3000)
        powermanager.setPower(jmri.PowerManager.ON)
        self.waitMsec(10000)

        # Zatrzymuje pociagi jesli jakis sie zawiesil
        print("Zatrzymanie pociagow przed uruchomieniem")
        self.waitMsec(100)
        self.V20.setSpeedSetting(0) #v20 wilenska
        self.waitMsec(100)

        self.train_long.setSpeedSetting(0) #pociag osobowy wilenska
        self.waitMsec(100)

        self.tram_visla.setSpeedSetting(0) #tramwaj wisla
        self.waitMsec(100)

        self.tram_storm.setSpeedSetting(0) #tramwaj burza
        self.waitMsec(100)

        #Wylaczone kolejki ktore maja byc - bez tego zawiesza skrypt przygotwane pod trasy mostowe
        """
        self.tram_visla_bridge.setSpeedSetting(0)
        self.waitMsec(100)

        self.tram_visla_bridge_2.setSpeedSetting(0)
        self.waitMsec(100)
        
        self.br80.setSpeedSetting(0)
        self.waitMsec(100)
        """

        print("Wykonuje sprawdzenie czujnikow")

        # Tramwaj burza:
        self.waitMsec(3000)
        if self.LS1.state == ACTIVE:
            print("czujnik LS1 TRAMWAJ BURZA aktywny")
            self.tram_storm_init.setState(ACTIVE)
            print("Uruchom skrypt loco_1_script normalnie")

        elif self.LS1.state != ACTIVE:
            self.waitMsec(1000)
            print("Brak lokomotywy uruchamiam program awaryjny")
            exec(open(file_path_LOK_1_emergency).read(), globals())
            self.tram_storm_init.setState(ACTIVE)
        else:
            print("Nieoczekiwany blad LOK1 TRAMWAJ BURZA przetrzyj tory, ustaw pociag, zresetuj program")

        # Tramwaj wisla:
        self.waitMsec(3000)
        if self.LS33.state == ACTIVE or self.LS42.state == ACTIVE:
            print("czujnik LS33 lub LS42 TRAMWAJ WISLA aktywny")
            self.tram_visla_init.setState(ACTIVE)
            print("Uruchom skrypt loco_3_script normalnie")

        elif self.LS33.state != ACTIVE or self.LS42.state != ACTIVE:
            self.waitMsec(1000)
            print("BRAK TRAMWAJU na stacji krancowej, uruchamiam program awaryjny")
            exec(open(file_path_LOK_3_emergency).read(), globals())
            self.tram_visla_init.setState(ACTIVE)
        else:
            print("Nieoczekiwany blad LOK3 TRAMWAJ WISLA przetrzyj tory, ustaw pociag, zresetuj program")

        # Pociag osobowy i towarowy wawa wilenska:
        self.waitMsec(3000)
        if self.LS17.state == ACTIVE and self.LS31.state == ACTIVE:
            print("czujnik LS17 i LS31 BUNKRY aktywny")
            self.train_long_init.setState(ACTIVE)
            self.self.v20_init.setState(ACTIVE)
            print("Uruchom skrypt loco_2_script normalnie")

        elif self.LS17.state != ACTIVE and self.LS31.state != ACTIVE:
            self.waitMsec(1000)
            print("BRAK OBU LOKOMOTYW na stacjach, uruchamiam program awaryjny")
            exec(open(file_path_LOK_2_emergency).read(), globals())
            self.train_long_init.setState(ACTIVE)
            self.v20_init.setState(ACTIVE)

        elif self.LS17.state == ACTIVE and self.LS31.state != ACTIVE:
            self.waitMsec(1000)
            print("POCIAG TOWAROWY nie na stacji, uruchamiam program awaryjny")
            exec(open(file_path_LOK_2_emergency).read(), globals())
            self.train_long_init.setState(ACTIVE)
            self.v20_init.setState(ACTIVE)

        elif self.LS17.state != ACTIVE and self.LS31.state == ACTIVE:
            self.waitMsec(1000)
            print("POCIAG OSOBOWY nie na stacji, uruchamiam program awaryjny")
            exec(open(file_path_LOK_2_emergency).read(), globals())
            self.train_long_init.setState(ACTIVE)
            self.v20_init.setState(ACTIVE)

        else:
            print("Nieoczekiwany blad LOK2 WAWA WILENSKA, przestaw pociagi, zresetuj program..")
        return 0


Start().start()
