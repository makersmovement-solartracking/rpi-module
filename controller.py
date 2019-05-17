import gpio_connector as GPIO


# LINEAR ACTUATOR OBJECT

class L298N:

    # Params

    input1 = 24
    input2 = 23
    en = 25
    p = None

    def __init__(self):

        # Initialize GPIO pins

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.input1, GPIO.OUT)
        GPIO.setup(self.input2, GPIO.OUT)
        GPIO.setup(self.en, GPIO.OUT)
        GPIO.output(self.input1, GPIO.LOW)
        GPIO.output(self.input2, GPIO.LOW)
        self.p = GPIO.PWM(self.en, 1000)
        self.p.start()

        # Set default to low
        self.change_power(25)

        # Map of inputs to commands
        self.movemap = {
            'low': self.change_power(25),
            'medium': self.change_power(50),
            'high': self.change_power(75)
            }

    def move_multi(self, directions):

        # In case you wanted to execute multiple directions
        # for example, move_multi(["forward", "stop", "backward"])

        for direction in directions:
            return self.move(direction)

    def move(self, direction):
        try:
            return self.movemap[direction]
        except KeyError as e:
            print(str(e))
            raise KeyError("Please enter a valid instruction {}".format(
                self.movemap.keys())
            )

    def change_power(self, level):
        self.p.ChangeDutyCycle(level)
        return "changed to {}".format(level)


class Movements(enum.Enum):
    """ Movements that can be done by the GPIO. """
 
    def stop(self):
        GPIO.output(self.input1, GPIO.LOW)
        GPIO.output(self.input2, GPIO.LOW)
        return "stopped"

    def forward(self):
        GPIO.output(self.input1, GPIO.HIGH)
        GPIO.output(self.input2, GPIO.LOW)
        return "forwarded"

    def backward(self):
        GPIO.output(self.input1, GPIO.LOW)
        GPIO.output(self.input2, GPIO.HIGH)
        return "backwarded"


