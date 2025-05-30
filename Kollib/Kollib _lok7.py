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
    :param vehicle: The vehicle object to be stopped.
    :param station: The station sensor to interact with.
    :param delay: The time in milliseconds the vehicle should remain stopped.
    :return: None
    """
    print "stop_at_station:White for sensor", station
    self.waitSensorActive([station])
    print "stop_at_station:Stop on Station", station
    vehicle.setSpeedSetting(0)  # Stop the vehicle
    self.waitMsec(500)
    vehicle.setSpeedSetting(0)
    print "stop_at_station:Delay =", delay, "ms"
    self.waitMsec(delay)
    self.waitMsec(1000)


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
    print "drive_vehicle:Set", vehicle, "Forward", is_forward
    vehicle.setIsForward(is_forward)
    self.waitMsec(1000)
    vehicle.setIsForward(is_forward)
    self.waitMsec(500)
    print "drive_vehicle:", vehicle, "Set Speed", speed
    vehicle.setSpeedSetting(speed)
    self.waitMsec(1000)
    vehicle.setSpeedSetting(speed)
    self.waitMsec(1000)


def delay_stop(self, vehicle, station, delay):
    """
    Causes the vehicle to wait a given delay before stopping.
    :param vehicle: The controlled vehicle object providing methods for sensor interaction and throttle control.
    :param station: The sensor station at which the vehicle should wait.
    :param delay: Time in milliseconds for which the vehicle should pause after activating the sensor.
    :return: None
    """
    print "delay_stop:White for sensor", station
    self.waitSensorActive([station])
    print "delay_stop:White to stop. Delay =", delay, "ms"
    self.waitMsec(delay)
    print "delay_stop:Stop", station
    vehicle.setSpeedSetting(0)
    self.waitMsec(100)
    vehicle.setSpeedSetting(0)
    self.waitMsec(1000)


def speed_change(self, vehicle, speed_multiplier):
    print "speed_change:Changing speed", vehicle
    curent_speed = vehicle.getSpeedSetting()
    speed_delta = curent_speed * speed_multiplier
    self.waitMsec(500)
    print "speed_change:", vehicle, "New speed", speed_delta
    vehicle.setSpeedSetting(speed_delta)
    self.waitMsec(100)
    vehicle.setSpeedSetting(speed_delta)
    self.waitMsec(1000)


def sc_station(self, vehicle, station, speed_multiplier):  # sc->speed change
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
    self.waitSensorActive([station])
    print "sc_station:", vehicle, "Waite for sensor", station
    curent_speed = vehicle.throttle.getSpeedSetting()
    self.waitMsec(500)
    print "sc_station:", vehicle, "New speed", speed_delta
    vehicle.setSpeedSetting(curent_speed * speed_multiplier)
    self.waitMsec(100)
    vehicle.setSpeedSetting(curent_speed * speed_multiplier)
    self.waitMsec(1000)


def turnout_revers(self, zwrotnica):
    """
    Reverses the state of a turnout (zwrotnica) between 'closed' and 'thrown'.
    :param self: Reference to the current instance of the class.
    :param zwrotnica: The turnout object whose state will be checked and switched.
                      It must implement the methods `getKnownState()` and `setState(state: int)`.
                      Known states:
                          - 2: Closed
                          - 4: Thrown
    """
    # Print a test message for debugging purposes
    print "turnout_revers:", zwrotnica
    # Check if the switch (zwrotnica) state is "closed" (2)
    if zwrotnica.getKnownState() == 2:  # 2 means closed
        # Change the state to "thrown" (4)
        zwrotnica.setState(4)
        # Print the new state to verify the change
        print(zwrotnica.getKnownState())
    # Check if the switch (zwrotnica) state is "thrown" (4)
    if zwrotnica.getKnownState() == 4:  # 4 means thrown
        # Change the state back to "closed" (2)
        zwrotnica.setState(2)
        # Print the new state to verify the change
        print(zwrotnica.getKnownState())