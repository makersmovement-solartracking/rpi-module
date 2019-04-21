import smbus2
import time

bus = smbus2.SMBus(1)
address = 0x08

def convert_byte_to_integer(byte_list):
    """ Convert the separated bytes into an integer"""
    return (byte_list[0] << 8)|byte_list[1]

while True:
    data = bus.read_i2c_block_data(address, 2, 2)
    value = convert_byte_to_integer(data)
    print(value)
    time.sleep(1)

