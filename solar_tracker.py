from controller import L298N
from i2c_connector import I2C
from time import sleep


class SolarTracker:
    """ Controls the solar panels movement, using the I2C connection
    to obtain the LDR values data, and the L298N to move the actuator. """

    def __init__(self, address, acceptable_deviation, ldr_count=2):
        self.acceptable_deviation = acceptable_deviation
        self.controller = L298N()
        self.i2c = I2C(address, ldr_count)
        self.night_mode = False
        self.strategies = {"empty": self._no_movement,
                           "greedy": self._greedy_movement}

    def _no_movement(self, *args):
        """ The actuator must stop. """
        return "stop"

    def _greedy_movement(self, ldr_values):
        if ldr_values[0] > ldr_values[1] + self.acceptable_deviation:
            return "left"
        if ldr_values[1] > ldr_values[0] + self.acceptable_deviation:
            return "right"
        return "stop"

    def night_time_mode(self, ldr_list):
        """ Verifies if the light is low enough to end the day and enter
        the night mode. """
        if ldr_list[0] < 100 and ldr_list[1] < 100 and not self.night_mode:
            self.controller.move("stop")
            if self.night_mode is False:
                print("Entering night mode...")
                self.night_mode = True
            sleep(300)
            return None
        elif self.night_mode:
            print("Exiting night mode!")
            self.night_mode = False

    def run(self, strategy="empty"):
        """ Runs the tracking. """
        if strategy not in self.strategies.keys():
            # Verifies if the strategy is valid
            raise Exception("Invalid strategy!")
        while True:
            try:
                ldr_values = self.i2c.get_ldr_values()
            except (IOError, OSError):
                continue
            if ldr_values:
                # Gets the selected strategy from the strategies dict
                # and pass the ldr_values as an argument
                movement = self.strategies[strategy](ldr_values)
                self.controller.move(movement)
                self.night_time_mode(ldr_values)
            else:
                # invalid ldr_values
                self.controller.move("stop")


if __name__ == "__main__":
    ARDUINO_ADDRESS = 0X08
    ACCEPTABLE_DEVIATION = 100
    SOLAR_TRACKER = SolarTracker(ARDUINO_ADDRESS, ACCEPTABLE_DEVIATION)
    SOLAR_TRACKER.run() # Argument must be the strategy used in the tracking
