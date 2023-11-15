# Flask.py - Corbin Hibler - 2023-11-10
# Python webserver backend for Data Acquisition project, using Flask app and library.

# Import necessary libraries (Python modules)
import os
from flask import Flask, render_template, request, session, send_from_directory
from werkzeug.exceptions import abort
import static.py.serial_monitor as serial_monitor

# Initialize Flask app with secret key and debug mode
app = Flask(__name__)
app.secret_key = 'rhysisfine69'
app.debug = True

# Define route for the home/index page
@app.route('/')
def index():
    return render_template('index.html')

# Define route for the favicon
@app.route('/favicon.ico')
def favicon():
    # Send the favicon file with the correct MIME type
    return send_from_directory(os.path.join(app.root_path, 'static'),
        'favicon.ico',mimetype='image/vnd.microsoft.icon')

# Define route for the serial monitor page
@app.route('/serial_monitor')
def serial_monitor():
    return render_template('serial-monitor.html')

# Define route for starting the serial monitor, accepting both GET and POST requests
@app.route('/start_serial_monitor', methods=['GET', 'POST'])
def start_serial_monitor():
    # Print the form data for debugging (comment out if needed)
    print(request.form)

    # Get the action from the form data
    action = request.form.get('action')

    #Start Serial Monitor
    if action == 'start':
        # Get the CSV filename from the form data
        csv_filename = request.form['csv_filename']
        # Call the main function of the SerialMonitor module
        serial_monitor.main(csv_filename)
        session['stop_loop'] = False
        return "Started serial monitor"
    
    # Stop Serial Monitor
    elif action == 'stop':
        session['stop_loop'] = True
        return "Stopped serial monitor"
    
    # If no action was provided (Error case!)
    return "No action"

# If this script is run directly (not imported)
if __name__ == '__main__':
    app.run()