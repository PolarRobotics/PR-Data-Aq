import os
from flask import Flask, render_template, request, session, send_from_directory
from werkzeug.exceptions import abort
import static.py.SerialMonitor as SerialMonitor

app = Flask(__name__)
app.secret_key = 'rhysisfine69'
app.debug = True

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
        'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/serial_monitor')
def serial_monitor():
    return render_template('serialmonitor.html')

@app.route('/start_serial_monitor', methods=['GET', 'POST'])
def start_serial_monitor():
    print(request.form)
    action = request.form.get('action')
    if action == 'start':
        csv_filename = request.form['csv_filename']
        SerialMonitor.main(csv_filename, session)
        session['stop_program'] = False
        return "Started serial monitor"
    elif action == 'stop':
        session['stop_loop'] = True
        return "Stopped serial monitor"
    return "No action"

if __name__ == '__main__':
   app.run()
