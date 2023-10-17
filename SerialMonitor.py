import serial
import csv
import datetime
import os, select, sys

ser = serial.Serial(
        '/dev/ttyUSB0', 
        baudrate = 115200, 
        parity   = serial.PARITY_NONE, 
        stopbits = serial.STOPBITS_ONE, 
        bytesize = serial.EIGHTBITS, 
        timeout  = 1
    )

i = 0

csvName = ""

while 1:
    # Output Stuff and Break
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[32mPOLAR ROBOTICS DATA ACQUISITION v1.0")
    if(csvName == ""):
        # Input for csv filename
        print("\033[32mEnter name of file you want data outputted to: ")
        csvName = input()
        csvName += ".csv"

        # Clear all existing data in opened file
        f = open(csvName, "w+")
        f.close()
    print("Data acquisition in progress...\nNumber of lines entered = \033[93m", i, "\n\033[41m\033[97mPress ENTER to stop script...\033[0m")
    
    # Break When Enter is Pressed
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = input()
        print("\033[31mDATA ACQUISITION HALTED. EXITING THE MAINFRAME...")
        break
    i += 1

    # Collect Data from ESP32
    rx_data = ser.readline()
    
    # Write to CSV
    # If you want a new name for the CSV file, change 'SerialMonitor.csv' to what you want.
    with open(csvName, newline='',mode='a') as csvFile:
        now = datetime.datetime.now()
        writer = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write_data = rx_data.decode("utf-8")[:-2]
        writer.writerow([now.time(), write_data])
        csvFile.close()