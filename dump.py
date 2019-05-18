from controller import L298N
from time import sleep
import i2c_connector as i2c
import datetime as dt
from csv import writer

i2c_slave = i2c.I2C(0x8, 4)
i = 0

while True:
    try:
        brute_data = i2c_slave.get_arduino_data()   
    except ( IOError, OSError) as e:
        continue
    ldr_values = i2c.convert_byte_to_integer(brute_data)
    date = dt.datetime.now()
    time_now = "{}:{}:{}".format(date.hour, date.minute, date.second)
    msg = "{}, {}, {}, {}, {}".format(time_now, ldr_values[0], ldr_values[1], ldr_values[2], ldr_values[3])
    values = [time_now,  ldr_values[0], ldr_values[1], ldr_values[2], ldr_values[3]]
    with open("out.csv", "a") as file:
        writer = writer()
        writer.writerow(values)
    sleep(1)
