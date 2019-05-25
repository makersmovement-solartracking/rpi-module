""" Controls the linear actuator movements. """

from enum import Enum
import gpio_connector as GPIO


GPIO_INPUT_ONE = 24
GPIO_INPUT_TWO = 23
CHANNEL = 25


class L298N:
    """ Raspberry Pi module that controls the linear actuator
    movements. """

    def __init__(self):

        # Initialize GPIO pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GPIO_INPUT_ONE, GPIO.OUT)
        GPIO.setup(GPIO_INPUT_TWO, GPIO.OUT)
        GPIO.setup(CHANNEL, GPIO.OUT)
        GPIO.output(GPIO_INPUT_ONE, GPIO.LOW)
        GPIO.output(GPIO_INPUT_TWO, GPIO.LOW)
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


class Movements(Enum):
    """ Movements that can be done by the GPIO. """

    @classmethod
    def stop(cls):
        """ Stops the actuator. """
        GPIO.output(GPIO_INPUT_ONE, GPIO.LOW)
        GPIO.output(GPIO_INPUT_TWO, GPIO.LOW)
        return "stopped"

    @classmethod
    def right(cls):
        """ Moves forward. """
        GPIO.output(GPIO_INPUT_ONE, GPIO.HIGH)
        GPIO.output(GPIO_INPUT_TWO, GPIO.LOW)
        return "moved to right"

    @classmethod
    def left(cls):
        """ Moves backward. """
        GPIO.output(GPIO_INPUT_ONE, GPIO.LOW)
        GPIO.output(GPIO_INPUT_TWO, GPIO.HIGH)
        return "moved to left"
