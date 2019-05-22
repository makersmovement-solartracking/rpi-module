from controller import L298N
from i2c_connector import I2C


class SolarTracker:
    """ Controls the solar panels movement, using the I2C connection
    to obtain the LDR values data, and the L298N to move the actuator. """

    def __init__(self, address, acceptable_deviation, ldr_count=2):
        self.acceptable_deviation = acceptable_deviation
        self.controller = L298N()
        self.i2c = I2C(address, ldr_count)
        self.strategies = {"empty": self._no_movement,
                           "greedy": self._greedy_movement,}

    def _no_movement(self):
        return "stop"

    def _greedy_movement(self, ldr_values):
        if ldr_values[0] > ldr_values[1] + self.acceptable_deviation:
            return "left"
        if ldr_values[1] > ldr_values[0] + self.acceptable_deviation:
            return "right"
        return "stop"

    def run(self, strategy="empty"):
        """ Runs the tracking. """
        if strategy not in self.strategies.keys(): # Verifies if the strategy is valid
            raise Exception("Invalid strategy!")
        while True:
            ldr_values = self.i2c.get_ldr_values()
            if ldr_values:
                # Gets the selected strategy from the strategies dict
                # and pass the ldr_values as an argument
                movement = self.strategies[strategy](ldr_values)
                self.controller.move(movement)
            else:
                # If the ldr_values is invalid, stop the movements and continues the flow
                self.controller.move("stop")

if __name__ == "__main__":
    ARDUINO_ADDRESS = 0X08
    ACCEPTABLE_DEVIATION = 50
    SOLAR_TRACKER = SolarTracker(ARDUINO_ADDRESS, ACCEPTABLE_DEVIATION)
    SOLAR_TRACKER.run()
