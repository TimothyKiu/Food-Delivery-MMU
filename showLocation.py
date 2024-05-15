from flask import Flask, jsonify, render_template
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': "localhost",
    'user': 'root',
    'passwd': '0000',
    'database': 'location_database'
}

@app.route('/')
def showLocation():
    return render_template('showLocation.html')

@app.route('/get_location')
def get_location():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("SELECT latitude, longitude FROM location ORDER BY id DESC LIMIT 1")  # Fetch latest coordinates
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        latitude, longitude = result
        return jsonify({'latitude': latitude, 'longitude': longitude})
    else:
        return jsonify({'error': 'No data found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
