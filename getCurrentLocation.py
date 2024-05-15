from flask import Flask, render_template, request
import mysql.connector

#NOTE: STOP RUNNING PYTHON WHENEVER YOU WANNA ALTER SQL TABLES
db = mysql.connector.connect(
    host="localhost",
    user='root',
    passwd='0000',
    database='location_database'
)

cursor = db.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('getCurrentLocationHTML.html')

@app.route('/current_location', methods=['POST'])
def current_location():
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']
    # Process location data as needed

    sql = "INSERT INTO location (latitude, longitude) VALUES (%s, %s)"
    val = (latitude, longitude)
    cursor.execute(sql, val)
    db.commit()

    print("rider location: Latitude {}, Longitude {}".format(latitude, longitude))
    return "rider location: Latitude {}, Longitude {}".format(latitude, longitude)


if __name__ == '__main__':
    app.run(debug=True)
