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
        if validates_ldr_data(ldr_values):
            return ldr_values
        return False


def convert_byte_to_integer(data):
    """ Converts the byte data to an integer. """
    ldr_data = []
    for i in int(len(data))/2:
        # Creates a list with the ldrs value as integers
        ldr_data.append(aggregate_bytes(data[i*2], data[i*2 + 1]))
    return ldr_data


def aggregate_bytes(most_representative, least_representative):
    """ Aggregates n bytes into a single word. """
    return (most_representative << 8 | least_representative) & 0xffffffff


def check_ldr_list_length(ldr_list):
    """ Checks the length of the ldr list, verifying if it's
    odd, even or empty. """
    if not ldr_list:
        raise EmptyLDRListException
    if len(ldr_list) % 2 != 0:
        raise OddLDRListException
    return True


def validates_ldr_data(ldr_list):
    """ Validates the values sent to the Raspberry pi
    from the Arduino. """
    if check_ldr_list_length(ldr_list):
        if 65535 in ldr_list:
            # Checks if the ldr_list has a invalid value (65535)
            return False
        else:
            return True
    return False

class OddLDRListException(Exception):
    """ Exception for an odd LDR list. """
    def __init__(self):
        self.message = "LDR list is odd."
        super().__init__(self.message)


class EmptyLDRListException(Exception):
    """ Exception for an empty ldr list. """
    def __init__(self):
        self.message = "LDR list is empty"
        super().__init__(self.message)
  
