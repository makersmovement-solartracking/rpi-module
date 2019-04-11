import RPi.GPIO as GPIO
from time import sleep


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
        GPIO.setup(input1,GPIO.OUT)
        GPIO.setup(input2,GPIO.OUT)
        GPIO.setup(en,GPIO.OUT)
        GPIO.output(input1,GPIO.LOW)
        GPIO.output(input2,GPIO.LOW)
        self.p = GPIO.PWM(en, 1000)
        self.p.start()

        # Set default to low
        self.change_power(25)

        # Map of inputs to commands
        self.movemap = {
            'stop' : self.stop(),
            'forward' : self.forward(),
            'backward' : self.backward(),
            'low' : self.change_power(25),
            'medium' : self.change_power(50),
            'high' : self.change_power(75)
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
            raise KeyError(f"Please enter a valid instruction {self.movemap.keys()}")


    # MOVE COMMANDS

    def stop(self):
        GPIO.output(input1,GPIO.LOW)
        GPIO.output(input2,GPIO.LOW)
        return "stopped"

    def forward(self):
        GPIO.output(input1,GPIO.HIGH)
        GPIO.output(input2,GPIO.LOW)
        return "forwarded"

    def backward(self):
        GPIO.output(input1,GPIO.LOW)
        GPIO.output(input2,GPIO.HIGH)
        return "backwarded"

    def change_power(self, level):
        self.p.ChangeDutyCycle(level)
        return f"changed to {level}"
        


  
        
# # LDR OBJECT

# WIP

# class LDR:

#     self.pin = 4

#     def __init__(self):
#         pass

#     def get_value(self):
#         # Returns the value of the LDR
#         pass

#     def rc_time(self):
#         count = 0

#         GPIO.setup(self.pin, GPIO.OUT)
#         GPIO.output(self.pin, GPIO.LOW)
#         time.sleep(0.1)

#         GPIO.setup(self.pin, GPIO.IN)

#         while (GPIO.input(self.pin) == GPIO.LOW):
#             count += 1

#         return count
