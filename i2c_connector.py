from smbus2 import SMBus

class I2C(SMBus):
    """ Represents the I2C connection and all its
    functions necessary to create the communication
    between the Arduino and the Raspberry Pi. """

    def __init__(self, addresses*):
        super.__init__(1)
        self.SLAVES_ADDRESS = [address for address in addresses)


    def get_arduino_data(self):
        """ Fetchs the Arduino data transfered through I2C. """
        values = {}
        for address in self.SLAVES_ADDRESS:
            values[address] = read_i2c_block_data(address, 1)
        return values

    def convert_byte_to_integer(self, values):
        """ Converts the byte data to an integer. """
        ldr_data = {}
        for slave, data in values.items():
            ldr_data[slave] = (data[0] << 8)|data[1]
        return ldr_data
