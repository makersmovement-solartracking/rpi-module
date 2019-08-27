import os
import logging, logging.config


if os.getenv("EXEC_MODE", "LOCAL") == "PROD":
    import RPi.GPIO as GPIO
    __LOCAL_MODE__ = False
    OUT = GPIO.OUT
    LOW = GPIO.LOW
    HIGH = GPIO.HIGH
    BCM = GPIO.BCM
else:
    __LOCAL_MODE__ = True
    # Variables declaration
    OUT = "output"
    LOW = "low"
    HIGH = "high"
    BCM = "bcm"

logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def cleanup(signum, frame):
    """ Cleans the GPIO pins. """
    if __LOCAL_MODE__:
        logger.info("Cleaned the pins")
    else:
        GPIO.cleanup()

def setup(pin_number, pin_type):
    """ Setups the GPIO pin. """
    if __LOCAL_MODE__:
        logger.info("Set pin {} to {}".format(pin_number, pin_type))
    else:
        GPIO.setup(pin_number, pin_type)


def setwarnings(condition):
    """ Sets the GPIO warnings false or true. """
    if __LOCAL_MODE__:
        logger.info("Set warnings to {}".format(condition))
    else:
        GPIO.setwarnings(condition)


def output(pin_number, pin_voltage):
    """ GPIO pin output. """
    if __LOCAL_MODE__:
        logger.info("Set pin {} to {}".format(pin_number, pin_voltage))
    else:
        GPIO.output(pin_number, pin_voltage)


def PWM(pin_number, frequency):
    """ GPIO pin frequency. """
    if __LOCAL_MODE__:
        logger.info("Set pin {} to frequency {}".format(pin_number, frequency))
        return MockPWM()
    else:
        return GPIO.PWM(pin_number, frequency)


def setmode(operation):
    """ Sets the operation of the Raspberry Pi pins. """
    if __LOCAL_MODE__:
        logger.info("Set board operation mode to {}".format(operation))
    else:
        GPIO.setmode(operation)


class MockPWM():
    """ Mock object of the PWM. """

    def __init__(self):
        pass

    def start(self, level):
        """ Simulates the PWM start. """
        logger.info("PWM Starts")

    def ChangeDutyCycle(self, level):
        """ Change the power of the pin output. """
        logger.info("Changed to {}".format(level))
