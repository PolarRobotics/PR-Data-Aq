import serial
import csv
import datetime
import select, sys

ser = serial.Serial(
        '/dev/ttyUSB1', 
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

# Write Headers
arrayHeaders = []

while 1:
    if(ser.in_waiting == 0):
        rx_data = ser.readline()
        break
write_data = rx_data.decode("utf-8")[:-1]
splitTerms = write_data.split(" ,")

print(splitTerms)

for i in splitTerms:
    arrayHeaders += splitTerms[i % 2 + 1]
    

with open(csvName, newline='',mode='a') as csvFile:
    writer = csv.writer(csvFile, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)
    stringHeaders = ",".join(str(x) for x in arrayHeaders)
    writer.writerow(['Time',stringHeaders])

while 1:
    # Break When Enter is Pressed
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = input()
        print("\033[31mDATA ACQUISITION HALTED. EXITING...")
        break

    # Collect Data from ESP32
    rx_data = ser.readline()
    write_data = rx_data.decode("utf-8")[:-1]
    print(write_data)

    # Write to CSV
    with open(csvName, newline='',mode='a') as csvFile:
        now = datetime.datetime.now()
        writer = csv.writer(csvFile, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE)
        writer.writerow([now.time(), write_data])
    linesWritten += 1