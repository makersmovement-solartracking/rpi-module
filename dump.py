""" Gets the value o n LDRs and append it to a csv file. """

from time import sleep
from csv import writer
from datetime import datetime
from i2c_connector import I2C


ADDRESS = 0X8
LDR_COUNT = 4
I2C_SLAVE = I2C(ADDRESS, LDR_COUNT)


def write_to_csv_file(data, filename="out.csv"):
    """ Appends the data to a CSV file. """
    with open(filename) as csv_file:
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


def get_csv_data_list(data):
    """ Creates the list that will be used by the CSV
    writer to append the data to the CSV file. """
    time = datetime.now()
    ldr_message = "{}:{}:{}".format(time.hour, time.minute, time.second)
    csv_data = [ldr_message]
    for value in data:
        csv_data.append(value)
    return csv_data


while True:
    try:
        LDR_VALUES = I2C_SLAVE.get_ldr_values()
    except (IOError, OSError):
        continue
    CSV_DATA = get_csv_data_list(LDR_VALUES)  # Creates the CSV list
    write_to_csv_file(CSV_DATA)  # Appends the data to the CSV file
    # Get the LDR values string
    LDR_VALUES_BY_TIME = get_ldr_values_by_time_string(LDR_VALUES)
    print(LDR_VALUES_BY_TIME)  # Prints the LDR values
    sleep(1)
