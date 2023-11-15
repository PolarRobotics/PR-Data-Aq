# SerialMonitor.py - Corbin Hibler - 2023-10-30
# Python script to convert serial communications from Polar Robotics ESP32
# into a CSV file with headers
import serial
import csv
import datetime
from flask import session

def csv_format(rx_data, constant):
    """
    Function to parse headers / values out of raw data and format it correctly.

    Parameters:
    rx_data (bytes): The data read from serial in bytes
    constant (int): Which every other term you want removed

    Returns:
    str: The combined string with commas that will be written in the CSV file
    """
    write_data = rx_data.decode("utf-8")[:-1]
    split_terms = write_data.split(",")
    every_other_term = split_terms[constant::2]
    final_data = ",".join(str(x) for x in every_other_term)
    return final_data
csv_filename = "Test"

def main(csv_filename):
    # Serial Setup
    # Change port variable to directory of USB/GPIO port to ESP32:
        # 'dev/ttyUSB0' for USB Port 0 on Linux/Mac Devices
        # 'dev/ttyUSB1' for USB Port 1 on Linux/Mac Devices
        # 'dev/ttyAMA0' for GPIO Port on Raspberry Pi
    port = '/dev/ttyUSB0'
    ser = serial.Serial(
            port, 
            baudrate = 115200, 
            parity   = serial.PARITY_NONE, 
            stopbits = serial.STOPBITS_ONE, 
            bytesize = serial.EIGHTBITS, 
            timeout  = 1
        )

    # Input for csv filename
    csvName = ""
    csvName = csv_filename
    csvName += ".csv"

    # Clear all existing data in opened file
    f = open(csvName, "w+")
    f.close()

    # Write Headers
    # Duplicate is not typo, the first one eliminates readline starting in the middle of text
    rx_data = ser.readline()
    rx_data = ser.readline()

    with open(csvName, newline='',mode='a') as csvFile:
        writer = csv.writer(csvFile, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)
        writer.writerow(['Time',csv_format(rx_data, 0)])

    # Data Recording
    while 1:
        if session.get('stop_loop'):
            break
        # Collect Data from ESP32
        rx_data = ser.readline()

        # Write to CSV
        with open(csvName, newline='',mode='a') as csvFile:
            writer = csv.writer(csvFile, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)
            now = datetime.datetime.now()
            writer.writerow([now.time(), csv_format(rx_data,1)])

if __name__ == "__main__":
    main()