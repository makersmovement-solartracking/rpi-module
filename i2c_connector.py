from smbus2 import SMBus


class I2C:
    """ Represents the I2C connection and all its
    functions necessary to create the communication
    between the Arduino and the Raspberry Pi. """

    def __init__(self, address, number_of_ldrs=2):
        self.connector = SMBus(1)
        self.SLAVE_ADDRESS = address
        self.number_of_ldrs = number_of_ldrs

    def get_arduino_data(self):
        """ Fetchs the Arduino data transfered through I2C. """
        return self.connector.read_i2c_block_data(self.SLAVE_ADDRESS, 1,
                                                  (self.number_of_ldrs * 2))

    def get_ldr_values(self):
        """ Gets the ldr values and validates it. """
        brute_data = self.get_arduino_data()
        ldr_values = convert_byte_to_integer(brute_data)
        if not is_valid_ldr_list(ldr_values):
            raise InvalidLDRListException
        if not is_valid_ldr_data(ldr_values):
            raise InvalidLDRListValuesException
        return ldr_values


def convert_byte_to_integer(data):
    """ Converts the byte data to an integer. """
    ldr_data = []
    for i in range(int(len(data)/2)):
        # Creates a list with the ldrs value as integers
        ldr_data.append(aggregate_bytes(data[i*2], data[i*2 + 1]))
    return ldr_data


def aggregate_bytes(most_representative, least_representative):
    """ Aggregates n bytes into a single word. """
    return (most_representative << 8 | least_representative) & 0xffffffff


def is_valid_ldr_list(ldr_list):
    """ Checks the length of the ldr list,
    verifying if it has an valid length. """
    if not ldr_list or len(ldr_list) % 2 != 0:
        return False
    else:
        return True


def is_valid_ldr_data(ldr_list):
    """ Validates the values sent to the Raspberry Pi from the Arduino. """
    if 65535 in ldr_list:
        return False
    else:
        return True


class InvalidLDRListException(Exception):
    """ Exception for an invalid LDR list. """

    def __init__(self):
        self.msg = "Invalid LDR List.\nThe transfered list is either odd or empty."

    def __str__(self):
        return repr(self.msg)


class InvalidLDRListValuesException(Exception):
    """ Exception for an invalid ldr list. """

    def __init__(self):
        self.msg = "Invalid LDR Value.\nThe LDR values will not be used."

    def __str__(self):
        return repr(self.msg)
