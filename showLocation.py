from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    # initialize map
    initial_latitude = 40.7128
    initial_longitude = -74.0060
    return render_template('showLocation.html', initial_latitude=initial_latitude, initial_longitude=initial_longitude)

if __name__ == '__main__':
    app.run(debug=True)
