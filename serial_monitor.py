import serial
import os
import csv
import datetime

# Function to parse headers / values out of raw data and format it correctly
# rx_data = the data read from serial in bytes
# constant = used for remove_every_other
def csv_format(rx_data, constant):
    write_data = rx_data.decode("utf-8")[:-1]
    split_terms = write_data.split(",")
    every_other_term = split_terms[constant::2]
    final_data = ",".join(str(x) for x in every_other_term)
    return final_data


ser = serial.Serial(
        '/dev/ttyUSB0', 
        baudrate = 115200, 
        parity   = serial.PARITY_NONE, 
        stopbits = serial.STOPBITS_ONE, 
        bytesize = serial.EIGHTBITS, 
        timeout  = 1
    )

linesWritten = 0
csvName = ""

print("\n\033[32mPOLAR ROBOTICS DATA ACQUISITION v1.1")
print("\033[97mSerial Monitor to CSV")
print("Takes data from a serial monitor input and converts to CSV format.")
print("Documentation is located in PR-Docs repo.\n")

while 1:
    # Input for csv filename
    print("\033[32mEnter name of CSV file (without .csv): \033[97m", end = "")
    csvName = input()
    csvName += ".csv"

    # Check if a file with that name already exists
    if os.path.exists(csvName):
        print("\033[31mWarning: File {} already exists!\033[97m".format(csvName))
    else: 
        break

## Write Headers
# Duplicate is not typo, the first one eliminates readline starting in the middle of text
rx_data = ser.readline()
rx_data = ser.readline()

with open(csvName, newline='',mode='a') as csvFile:
    writer = csv.writer(csvFile, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)
    writer.writerow(['Time',csv_format(rx_data, 0)])

while 1:
    # Collect Data from ESP32
    rx_data = ser.readline()

    # Write data to terminal
    write_data = rx_data.decode("utf-8")[:-1]
    now = datetime.datetime.now()
    print(str(now.time()) + write_data)

    # Write to CSV
    with open(csvName, newline='',mode='a') as csvFile:
        writer = csv.writer(csvFile, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)
        now = datetime.datetime.now()
        writer.writerow([now.time(), csv_format(rx_data,1)])
    linesWritten += 1