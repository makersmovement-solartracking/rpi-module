from controller import L298N

motor = L298N()
movements = ["low", "forward", "backward", "stop",
             "this will produce an error"]

for move in movements:
    print(motor.move(move))
