from controller import L298N
from i2c_connector import I2C

class SolarTracker:

    def __init__(self, address, acceptable_deviation, ldr_count):
        self.ACCEPTABLE_DEVIATION = acceptable_deviation
        self.controller = L298N()
        self.i2c = I2C(address, ldr_count)
        self.strategies = {"empty": self._no_movement,
                           "greedy": self._greedy_movement,}

    def _no_movement(self, ldr_values):
        return "stop"

    def _greedy_movement(self, ldr_values):
        if ldr_values[0] > ldr_values[1] + ACCEPTABLE_DEVIATION:
            return "left"
        elif ldr_values[1] > ldr_values[0] + ACCEPTABLE_DEVIATION:
            return "right"
        else:
            return "stop"

    def run(self, strategy="empty"):
        """ Runs the tracking. """
        if strategy not in self.strategies.keys(): # Verifies if the strategy is valid
            raise Exception("Invalid strategy!")
        while True:
            ldr_values = self.i2c.get_ldr_values()
            movement = self.strategies[strategy](ldr_values)
            self.controller.move(movement)

solar_tracker = SolarTracker(0x08, 2)


solar_tracker.run()
solar_tracker.run("sakjdk")
