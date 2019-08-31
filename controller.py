""" Controls the linear actuator movements. """

import logging, logging.config
from enum import Enum
import gpio_connector as GPIO

logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class L298N:
    """ Raspberry Pi module that controls the linear actuator
    movements. """

    def __init__(self, output_pins, energy_channel):

        # Pins
        self.output_pins = output_pins
        self.energy_channel = energy_channel

        # Initialize GPIO pins
        GPIO.setmode(GPIO.BCM)
        self.setup_output_pins()
        GPIO.setup(self.energy_channel, GPIO.OUT)
        self.initialize_output_pins()
        self.actuator = GPIO.PWM(self.energy_channel, 1000)
        self.actuator.start(25)

        # Set warnings off
        GPIO.setwarnings(False)

        # Set default to medium
        self.change_power(50)

        # Map of inputs to commands
        self.movemap = {
            'low': self.change_power(25),
            'medium': self.change_power(50),
            'high': self.change_power(75)}

        self.movements = {"stop": Movements.stop,
                          "right": Movements.right,
                          "left": Movements.left
                          }

    def move(self, direction, output_pins):
        """ Moves to a given direction. """
        try:
            return self.movements[direction](output_pins)
        except KeyError as error:
            logger.warning("{}\n{}".format(error, "Invalid Movement"))

    def change_power(self, level):
        """ Changes the actuator power. """
        self.actuator.ChangeDutyCycle(level)
        return logger.info("changed power to {}".format(level))

    def setup_output_pins(self):
        """ Setups the pins to out. """
        for pins in self.output_pins:
            GPIO.setup(pins, GPIO.OUT)

    def initialize_output_pins(self):
        """ initializes the output pins to low """
        for pins in self.output_pins:
            GPIO.output(pins[0], GPIO.LOW)
            GPIO.output(pins[1], GPIO.LOW)


class Movements(Enum):
    """ Movements that can be done by the GPIO. """

    @classmethod
    def stop(cls, output_pins):
        """ Stops the actuator. """
        for pin_pairs in output_pins:
            GPIO.output(pin_pairs[0], GPIO.LOW)
            GPIO.output(pin_pairs[1], GPIO.LOW)
        return logger.info("Stopped the movements")

    @classmethod
    def left(cls, output_pins):
        """ Moves forward, turning the panels to the left"""
        for pin_pairs in output_pins:
            GPIO.output(pin_pairs[0], GPIO.HIGH)
            GPIO.output(pin_pairs[1], GPIO.LOW)
        return logger.info("Turning the panels to the left")

    @classmethod
    def right(cls, output_pins):
        """ Moves backward, turning the panels to the right """
        for pin_pairs in output_pins:
            GPIO.output(pin_pairs[0], GPIO.LOW)
            GPIO.output(pin_pairs[1], GPIO.HIGH)
        return logger.info("Turning the panels to the right")
