import serial
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

print("\033[32mPOLAR ROBOTICS DATA ACQUISITION v1.0")

# Input for csv filename
print("\033[32mEnter name of file you want data outputted to: \033[97m")
csvName = input()
csvName += ".csv"

# Clear all existing data in opened file
f = open(csvName, "w+")
f.close()

## Write Headers

# buffer = ''
# while True:
#     rx_data = b''
#     rx_data = ser.readline()
#     buffer += rx_data.decode("utf-9")[:-1]
#     try:
#         rx_data = json.loads(buffer)
#         print(rx_data)
#         buffer = ''
#     except json.JSONDecodeError:
#         time.sleep(0)

rx_data = ser.readline()

with open(csvName, newline='',mode='a') as csvFile:
    writer = csv.writer(csvFile, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)
    writer.writerow(['Time',csv_format(rx_data, 0)])

while 1:
    # Collect Data from ESP32
    rx_data = ser.readline()

    # Write to CSV
    with open(csvName, newline='',mode='a') as csvFile:
        writer = csv.writer(csvFile, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)
        now = datetime.datetime.now()
        writer.writerow([now.time(), csv_format(rx_data,1)])
    linesWritten += 1