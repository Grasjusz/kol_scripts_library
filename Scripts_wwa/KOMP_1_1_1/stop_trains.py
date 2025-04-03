import jarray
import jmri

class Stop(jmri.jmrit.automat.AbstractAutomaton):

    def init(self):
        self.tram_storm_init = sensors.getSensor("IS1")
        self.tram_visla_bridge_init = sensors.getSensor("IS2")
        self.tram_visla_init = sensors.getSensor("IS3")
        self.br80_init = sensors.getSensor("IS4")
        self.v20 = sensors.getSensor("IS5")
        self.train_long_init = sensors.getSensor("IS6")

        self.tram_storm = self.getThrottle(6, False) #tramwaj burza adr 10
        self.tram_visla = self.getThrottle(6, False)  #tramwaj wisla adr 11
        self.tram_visla_bridge = self.getThrottle(6, False)  #tramwaj wisla adr 12
        self.tram_visla_bridge_2 = self.getThrottle(6, False)  #tramwaj wisla adr 13
        self.train_long = self.getThrottle(6, False)  #pociag osobowy adr 3
        self.br80 = self.getThrottle(6, False)  #BR80 adr 5
        self.V20 = self.getThrottle(6, False)  #V20020 adr 6
        return

    def handle(self):

        self.tram_storm_init.setState(INACTIVE)
        self.tram_visla_bridge_init.setState(INACTIVE)
        self.tram_visla_init.setState(INACTIVE)
        self.br80_init.setState(INACTIVE)
        self.v20.setState(INACTIVE)
        self.train_long_init.setState(INACTIVE)
        return 0


Stop().start()
