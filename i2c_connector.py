from smbus2 import SMBus

class I2C:
    """ Represents the I2C connection and all its
    functions necessary to create the communication
    between the Arduino and the Raspberry Pi. """

    def __init__(self, address):
        self.connector = SMBus(1)
        self.SLAVE_ADDRESS = address


    def get_arduino_data(self):
        """ Fetchs the Arduino data transfered through I2C. """
        data  = self.connector.read_i2c_block_data(self.SLAVE_ADDRESS, 1, 2)
        return data

    def convert_byte_to_integer(self, data):
        """ Converts the byte data to an integer. """
        ldr_data = (data[0] << 8)|data[1]
        return ldr_data
