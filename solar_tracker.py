import signal
import logging, logging.config
import controller
from i2c_connector import I2C, InvalidLDRListException, InvalidLDRListValuesException
from time import sleep

logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class SolarTracker:
    """
    Solar tracking, centralizing the solar panel arrays to it.

    ...

    Attributes
    ----------
    address: int
        Address of the I2C slave.
    acceptable_deviation: int
        Default deviation between the ldrs.
    output_pins: list
        List with tuples representing the pairs of output pins.
        Always (Left, Right).
    energy_channel: int
        Raspberry Pi pin which will provide the energy.
    ldr_count: int
        Number of ldr.
        Default=2.

    Methods
    -------
    _no_movement()
        Empty strategy which will not move the panels

    _greedy_movement(ldr_values)
        Returns the direction that has the highest amount of light

    night_time_mode(ldr_values)
        Verifies if the light is low enough to activate night mode

    run(strategy)
        Executes the process, processing the data and moving the array
    """

    def __init__(self, address, acceptable_deviation,
                 output_pins, energy_channel, ldr_count=2):
        # Attributes used to move the solar panel
        self.acceptable_deviation = acceptable_deviation
        self.output_pins = output_pins
        self.energy_channel = energy_channel

        # Objects used to get data and activate the actuator
        self.controller = controller.L298N(self.output_pins, self.energy_channel)
        self.i2c = I2C(address, ldr_count)

        # Strategies that can be used in the solar tracking
        self.strategies = {"empty": self._no_movement,
                           "greedy": self._greedy_movement}

        # If the docker container stops running, clear the pins
        signal.signal(signal.SIGINT, controller.GPIO.cleanup)
        signal.signal(signal.SIGTERM, controller.GPIO.cleanup)

        # Attribut used to set the night mode on or off
        self.night_mode = False

    def _no_movement(self, ldr_values):
        """
        Strategy with no movement

        Parameters
        ----------

        ldr_values: list
            Contains the LDR values sent by the Arduino

        Returns
        -------
        string
            Stop

        """
        return "stop"

    def _greedy_movement(self, ldr_values):
        """
        Strategy that fetchs the direction with highest amount of light

        Parameters
        ----------

        ldr_values: list
            Contains the LDR values sent by the Arduino

        Returns
        -------
        string
            left if the left LDR has a value higher than the right one.
            right if the right LDR has a value higher than the left one.
            stop if both LDRs are within the acceptable deviation.

        """
        if ldr_values[0] > ldr_values[1] + self.acceptable_deviation:
            return "left"
        if ldr_values[1] > ldr_values[0] + self.acceptable_deviation:
            return "right"
        return "stop"

    def night_time_mode(self, ldr_values):
        """
        Mode which will make the software pause when there isn't enought light

        ...

        Compares both LDR values to 100, if both are lower than the value, stops
        the linear actuators and enters into the night mode, which will make new
        requests every 5 minutes in order to verify if there is enough light to
        come back to work.

        Parameters
        ----------
        ldr_values: list
            Contains the LDR values sent by the Arduino

        Returns
        -------
            None

        -------

        """

        if ldr_values[0] < 10 and ldr_values[1] < 10:
            self.controller.move("stop", self.output_pins)
            if self.night_mode is False:
                logger.info("Entering night mode...")
                self.night_mode = True
            sleep(300)
        elif self.night_mode:
            logger.info("Exiting night mode!")
            self.night_mode = False

    def run(self, strategy="empty"):
        """
        Executes the solar tracking, activating the linear actuators to move the
        solar panel array

        ...

        Every 0.5 seconds, requests a new list of data from the Arduino,
        process and validates it. If the LDR values are valid, verifies to
        which direction the solar panel array should move and, if necessary,
        moves it to that direction.
        If the LDR values are not valid, stops any movement in order to keep
        the precision of the software.

        Parameters
        ----------
        strategy: string
            Which strategy will be used to process the LDR data.
            Default=empty

        Exceptions
        ----------
        unvalid strategy:
            Strategy not available in the software
        IOError, OSError:
            Errors hardware related, can be ignored and the software will
        run normally

        """
        if strategy not in self.strategies.keys():
            # Verifies if the strategy is valid
            raise Exception("Invalid strategy!")
        while True:
            try:
                sleep(0.5)
                ldr_values = self.i2c.get_ldr_values()

            except (IOError, OSError) as e:
                logger.exception(str(e))
                continue

            except (InvalidLDRListException, InvalidLDRListValuesException) as e:
                self.controller.move("stop", self.output_pins)
                logger.exception(str(e))
                continue

            # Verifies if it's night or if there isn't a good amount of light
            self.night_time_mode(ldr_values)
            # Gets the selected strategy from the strategies dict
            # and pass the ldr_values as an argument
            movement = self.strategies[strategy](ldr_values)
            self.controller.move(movement, self.output_pins)

if __name__ == "__main__":
    ARDUINO_ADDRESS = 0X08  # Address of the Arduino
    ACCEPTABLE_DEVIATION = 50  # Normal deviation between the LDRs
    # Output pins which will be connected to each actuator
    # they must be tuples. (Left, Right)
    OUTPUT_PINS = [(23, 24)]
    ENERGY_CHANNEL = 25
    solar_tracker = SolarTracker(ARDUINO_ADDRESS, ACCEPTABLE_DEVIATION,
                                 OUTPUT_PINS, ENERGY_CHANNEL)
    solar_tracker.run("greedy")  # Argument must be the strategy used in the tracking
