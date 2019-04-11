import os
if os.getenv("EXEC_MODE", "LOCAL") == "PROD":
    import RPi.GPIO as GPIO
    __LOCAL_MODE__ = False
else:
    __LOCAL_MODE__ = True


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


def pwm(pin_number, frequency):
    if __LOCAL_MODE__:
        print("Set pin {} to frequency {}".format(pin_number, frequency))
    else:
        GPIO.PWM(pin_number, frequency)
