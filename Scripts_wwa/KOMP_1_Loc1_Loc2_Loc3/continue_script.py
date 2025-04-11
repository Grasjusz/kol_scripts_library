import jarray
import jmri

class Continue(jmri.jmrit.automat.AbstractAutomaton):

    def init(self):
        self.tram_storm_init = sensors.getSensor("IS1")
        self.tram_visla_bridge_init = sensors.getSensor("IS2")
        self.tram_visla_init = sensors.getSensor("IS3")
        self.br80_init = sensors.getSensor("IS4")
        self.v20 = sensors.getSensor("IS5")
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
        self.tram_storm_init.setState(ACTIVE)
        self.tram_visla_bridge_init.setState(ACTIVE)
        self.tram_visla_init.setState(ACTIVE)
        self.br80_init.setState(ACTIVE)
        self.v20.setState(ACTIVE)
        self.train_long_init.setState(ACTIVE)
        return 0


Continue().start()
