# Flask.py - Corbin Hibler - 2023-11-10
# Python webserver backend for Data Acquisition project, using Flask app and library.

# Import necessary libraries (Python modules)
import os
import signal
from flask import Flask, render_template, request, session, send_from_directory, jsonify
from werkzeug.exceptions import abort
from static.py import serial_monitor
from multiprocessing import Process

# Initialize Flask app with secret key and debug mode
app = Flask(__name__)
app.secret_key = 'rhysisfine69'
app.debug = True

# Define route for the home/index page
@app.route('/')
def index_page():
    return render_template('index.html')

# Define route for the favicon
@app.route('/favicon.ico')
def favicon():
    # Send the favicon file with the correct MIME type
    return send_from_directory(os.path.join(app.root_path, 'static'),
        'favicon.ico',mimetype='image/vnd.microsoft.icon')

# Define route for the serial monitor page
@app.route('/serial_monitor')
def serial_monitor_page():
    return render_template('serial-monitor.html')

# Global Variable to store process ID
pid = None

# Define route for starting the serial monitor
@app.route('/start_serial_monitor', methods=['POST'])
def start_serial_monitor():
    global pid
    print("STARTING...")
    # Print the form data for debugging (comment out if needed)
    print(request.form)
    # Get the CSV filename from the form data
    csv_filename = request.form['csv_filename']
    # Create a new process that runs the main function
    p = Process(target=serial_monitor.main, args=(csv_filename,))
    # Start the process
    p.start()
    # Store the process ID and CSV path
    pid = p.pid
    print(f"Started process with ID {pid}")
    csv_path = os.path.join(os.getcwd(), f"{csv_filename}.csv")
    session['csv_path'] = csv_path
    #return jsonify({'message': "Started serial monitor", 'csv_path': csv_path})
    return "Done"

@app.route('/stop_serial_monitor', methods=['POST'])
def stop_serial_monitor():
    global pid
    print("STOPPING...")
    if pid is not None:
        print(f"Stopping process with ID {pid}")
        try:
            # Send the SIGTERM signal to the process
            os.kill(pid, signal.SIGTERM)
        #    message = "Stopped serial monitor"
        except Exception as e:
            print(f"Failed to stop process: {e}")
        #    message = f"Failed to stop serial monitor: {e}"
    else:
        print("No process ID found.")
    #    message = "No process ID found"
    return jsonify({'csv_path': session.get('csv_path')})

@app.route('/download_csv', methods=['POST'])
def download_csv():
    # Get the CSV filename from the form data
    csv_filename = request.form['csv_filename']
    csv_path = os.path.join(os.getcwd(), f"{csv_filename}.csv")
    # Check if file exists
    if os.path.exists(csv_path):
        # Send file for download
        return send_from_directory(directory=os.getcwd(), path=f"{csv_filename}.csv", as_attachment=True)
    else:
        return "File not found."
# If this script is run directly (not imported)
if __name__ == '__main__':
    app.run()