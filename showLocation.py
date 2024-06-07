from flask import Flask, jsonify, render_template
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': "localhost",
    'user': 'root',
    'passwd': '0000',
    'database': 'webdb'
}

def get_locations():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT latitude, longitude FROM location WHERE order_id = 1")
    locations = cursor.fetchall()
    conn.close()
    return locations

@app.route('/')
def index():
    return render_template('showLocation.html')

@app.route('/locations')
def locations():
    locations = get_locations()
    return jsonify(locations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
