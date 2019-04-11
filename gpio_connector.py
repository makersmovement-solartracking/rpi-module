import os
if os.getenv("EXEC_MODE", "LOCAL") == "PROD":
    import RPi.GPIO as GPIO
    __LOCAL_MODE__ = False
    OUT = GPIO.OUT
    LOW = GPIO.LOW
    HIGH = GPIO.HIGH
    BCM = GPIO.BMC
else:
    __LOCAL_MODE__ = True
    # Variables declaration
    OUT = "output"
    LOW = "low"
    HIGH = "high"
    BCM = "bcm"


def setup(pin_number, pin_type):
    if __LOCAL_MODE__:
        print("Set pin {} to {}".format(pin_number, pin_type))
    else:
        GPIO.setup(pin_number, pin_type)


def output(pin_number, pin_voltage):
    if __LOCAL_MODE__:
        print("Set pin {} to {}".format(pin_number, pin_voltage))
    else:
        GPIO.output(pin_number, pin_voltage)


def PWM(pin_number, frequency):
    if __LOCAL_MODE__:
        print("Set pin {} to frequency {}".format(pin_number, frequency))
        return MockPWM
    else:
        GPIO.PWM(pin_number, frequency)


def setmode(operation):
    if __LOCAL_MODE__:
        print("Set board operation mode to {}".format(operation))
    else:
        GPIO.setmode(operation)


class MockPWM():

    def __init__(self):
        pass

    def start():
        print("PWM start")

    def ChangeDutyCycle(level):
        print("Changed to {}".format(level))