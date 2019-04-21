import smbus
import time

bus = smbus.SMBus(1)
address = 0x04


def unmap(value, in_min, in_max, out_min, out_max):
    """Unmaps the number received through the I2C connection"""
    return (value * ((in_max - in_min) + out_min) + in_min ) / (out_max - out_min)


while True:
    data = bus.read_byte(address)
    print(data)
    print(unmap(data, 0, 1023, 0, 255))
    time.sleep(1)

