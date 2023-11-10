# Flask.py - Corbin Hibler - 2023-11-10
# Python webserver backend for Data Acquisition project, using Flask app and library.

# Import necessary libraries (Python modules)
import os
from flask import Flask, render_template, request, session, send_from_directory
from werkzeug.exceptions import abort
import static.py.SerialMonitor as SerialMonitor

# Initialize Flask app
app = Flask(__name__)
# Set secret key for session
app.secret_key = 'rhysisfine69'
# Enable debug mode
app.debug = True

# Define route for the home/index page
@app.route('/')
def index():
    # Render the index.html template
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
    # Render the serialmonitor.html template
    return render_template('serialmonitor.html')

# Define route for starting the serial monitor, accepting both GET and POST requests
@app.route('/start_serial_monitor', methods=['GET', 'POST'])
def start_serial_monitor():
    # Print the form data for debugging
    print(request.form)
    # Get the action from the form data
    action = request.form.get('action')
    # If the action is 'start'
    if action == 'start':
        # Get the CSV filename from the form data
        csv_filename = request.form['csv_filename']
        # Call the main function of the SerialMonitor module
        SerialMonitor.main(csv_filename, session)
        # Set the 'stop_program' session variable to False
        session['stop_program'] = False
        # Return a success message to console
        return "Started serial monitor"
    # If the action is 'stop'
    elif action == 'stop':
        # Set the 'stop_loop' session variable to True
        session['stop_loop'] = True
        # Return a success message to console
        return "Stopped serial monitor"
    # If no action was provided (Error case!)
    return "No action"

# If this script is run directly (not imported)
if __name__ == '__main__':
    # Run the Flask app
    app.run()