from smbus2 import SMBus

class I2C:
    """ Represents the I2C connection and all its
    functions necessary to create the communication
    between the Arduino and the Raspberry Pi. """

    def __init__(self, address, number_of_ldrs):
        self.connector = SMBus(1)
        self.SLAVE_ADDRESS = address
        self.number_of_ldrs = number_of_ldrs

    def get_arduino_data(self):
        """ Fetchs the Arduino data transfered through I2C. """
        data = self.connector.read_i2c_block_data(self.SLAVE_ADDRESS, 1, (self.number_of_ldrs * 2))
        return data

    def convert_byte_to_integer(self, data):
        """ Converts the byte data to an integer. """
        ldr_data = []
        for i in range(0, self.number_of_ldrs, 2):
            # Creates a list with the ldrs value as integers
            ldr_data.append((data[i] << 8 | data[i+1]))

        return ldr_data
