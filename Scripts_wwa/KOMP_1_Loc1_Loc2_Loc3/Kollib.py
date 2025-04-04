'''
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
    self.waitSensorActive([station])
    #print "stop_at_station:Stop on Station"
    vehicle.setSpeedSetting(0)# Stop the vehicle
    #print "stop_at_station:Delay"
    self.waitMsec(delay)



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
    #print "drive_vehicle:Set Loco Forward"
    vehicle.setIsForward(is_forward)
    # wait 1 second for layout to catch up, then set speed
    self.waitMsec(1000)
    #print "drive_vehicle:Set Speed1"
    vehicle.setSpeedSetting(speed)

def delay_stop(self, vehicle,station,delay):
    """
    Causes the vehicle to wait a given delay before stopping.

    :param self:
    :param vehicle: The controlled vehicle object providing methods for sensor interaction and throttle control.
    :param station: The sensor station at which the vehicle should wait.
    :param delay: Time in milliseconds for which the vehicle should pause after activating the sensor.
    :return: None
    """

    #print "delay_stop:White for sensor"
    self.waitSensorActive([station])
    #print "delay_stop:White to stop"
    self.waitMsec(delay)
    #print "delay_stop:Stop"
    vehicle.setSpeedSetting(0)
    self.waitMsec(1000)


def speed_change(self, vehicle, speed_multiplier):
    #print "speed_change:Changing speed"
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
    vehicle.waitSensorActive([station])
    #print "sc_station:White for sensor"
    curent_speed=vehicle.getSpeedSetting()
    self.waitMsec(500)
    #print "sc_station:Changing speed"
    vehicle.setSpeedSetting(curent_speed * speed_multiplier)
    self.waitMsec(1000)

def zwrotnica_test(self, zwrotnica):
    #print "zwrotnica test:"
    if zwrotnica.getKnownState() == 2 : #2 closed
        zwrotnica.setState(4)
        print(zwrotnica.getKnownState())
    if zwrotnica.getKnownState() == 4: #4 thrown
        zwrotnica.setState(2)
        print(zwrotnica.getKnownState())


