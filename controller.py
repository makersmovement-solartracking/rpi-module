""" Controls the linear actuator movements. """

from enum import Enum
import gpio_connector as GPIO


GPIO_INPUT_ONE = 24
GPIO_INPUT_TWO = 23
CHANNEL = 25


class L298N:
    """ Raspberry Pi module that controls the linear actuator
    movements. """

    def __init__(self, output_pins):

        # Initialize GPIO pins
        GPIO.setmode(GPIO.BCM)
        self.setup_output_pins(output_pins)
        GPIO.setup(CHANNEL, GPIO.OUT)
        self.initialize_output_pins(output_pins)
        self.actuator = GPIO.PWM(CHANNEL, 1000)
        self.actuator.start(25)

        # Set warnings off
        GPIO.setwarnings(False)

        # Set default to low
        self.change_power(25)

        # Map of inputs to commands
        self.movemap = {
            'low': self.change_power(25),
            'medium': self.change_power(50),
            'high': self.change_power(75)}

        self.movements = {"stop": Movements.stop,
                          "right": Movements.right,
                          "left": Movements.left,
                          }

    def move(self, direction):
        """ Moves to a given direction. """
        try:
            return self.movements[direction]()
        except KeyError as e:
            print(str(e))
            print("Invalid movement")

    def change_power(self, level):
        """ Changes the actuator power. """
        self.actuator.ChangeDutyCycle(level)
        return "changed to {}".format(level)

    def setup_output_pins(self, output_pins):
        """ Setups the pins to out. """
        for pins in output_pins: 
            GPIO.setup(pins, GPIO.OUT)

    def initialize_output_pins(self, output_pins):
        """ initializes the output pins to low """
        for pins in output_pins:
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
        return "stopped"

    @classmethod
    def left(cls, output_pins):
        """ Moves forward, turning the panels to the left"""
        for pin_pairs in output_pins:
            GPIO.output(pin_pairs[0], GPIO.HIGH)
            GPIO.output(pin_pairs[1], GPIO.LOW)
        return "turned the panels to the left"

    @classmethod
    def right(cls, output_pins):
        """ Moves backward, turning the panels to the right """
        for pin_pairs in output_pins:
            GPIO.output(pin_pairs[0], GPIO.LOW)
            GPIO.output(pin_pairs[1], GPIO.HIGH)
        return "moved to left"
