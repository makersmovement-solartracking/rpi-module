""" Gets the value of n LDRs and append it to a csv file. """

from time import sleep
from csv import writer
from datetime import datetime
from i2c_connector import I2C, EmptyLDRListException, OddLDRListException, UnvalidLDRListValuesException
import sys


ADDRESS = 0X8
LDR_COUNT = 4
i2c_slave = I2C(ADDRESS, LDR_COUNT)


def write_to_csv_file(data, filename="out.csv"):
    """ Appends the data to a CSV file. """
    with open(filename, 'wb') as csv_file:
        csv_writer = writer(csv_file)
        csv_writer.writerow(data)


def get_ldr_values_by_time_string(data):
    """ Creates the message used to print the data
    to the terminal. """
    time = datetime.now()
    ldr_message = "{}:{}:{}".format(time.hour, time.minute, time.second)
    for value in data:
        ldr_message += ", {}".format(value)
    return ldr_message


while True:
    try:
        sleep(1)
        ldr_values = i2c_slave.get_ldr_values()

    except (IOError, OSError):
        continue

    except (OddLDRListException, EmptyLDRListException, UnvalidLDRListValuesException) as e:
        print(str(e))
        continue

    ldr_values_by_time = get_ldr_values_by_time_string(ldr_values)
    print(ldr_values_by_time)

    if len(sys.argv) > 1 and str(sys.argv[1]) is '-c':
        ldr_values_by_time.replace(' ', ',')
        write_to_csv_file(ldr_values_by_time)


