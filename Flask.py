from flask import Flask, render_template
import SerialMonitor

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

# @app.route('/run')
# def run():
#    SerialMonitor.__main__
#    print("test")
#    return render_template('run.html')

if __name__ == '__main__':
   app.run()
