import sqlite3
import os
from flask import Flask, render_template, request, session, send_from_directory
from werkzeug.exceptions import abort
import static.py.SerialMonitor as SerialMonitor

# Access database and sets row_factory sqlite.Row so we have name-based access to columns
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Open a database connection and execute a SQL query to get the program page
def get_program(program_id):
    conn = get_db_connection()
    program = conn.execute('SELECT * FROM programs WHERE id = ?',
                        (program_id,)).fetchone()
    conn.close()
    if program is None:
        abort(404)
    return program

app = Flask(__name__)
app.secret_key = 'rhysisfine69'
app.debug = True

@app.route('/')
def index():
   conn = get_db_connection()
   programs = conn.execute('SELECT * FROM programs').fetchall()
   conn.close()
   return render_template('index.html', programs=programs)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
        'favicon.ico',mimetype='image/vnd.microsoft.icon')

@app.route('/<int:program_id>')
def program(program_id):
    program = get_program(program_id)
    return render_template('program.html', program=program)

@app.route('/serial_monitor', methods=['GET', 'POST'])
def start_serial_monitor():
    print(request.form)
    if request.form['action'] == 'start':
        csv_filename = request.form['csv_filename']
        SerialMonitor.main(csv_filename, session)
        session['stop_program'] = False
        return "Started serial monitor"
    elif request.form['action'] == 'stop':
        session['stop_loop'] = True
        return "Stopped serial monitor"
    return "No action"

if __name__ == '__main__':
   app.run()
