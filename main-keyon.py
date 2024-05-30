from flask import Flask, render_template, request, jsonify
import mysql.connector

# NOTE: STOP RUNNING PYTHON WHENEVER YOU WANNA ALTER SQL TABLES
db = mysql.connector.connect(
    host="localhost",
    user='root',
    passwd='0000',
    database='location_database'
)

cursor = db.cursor()

app = Flask(__name__)

orders = [
    {"id": 1, "item": "roti kosong"},
    {"id": 2, "item": "maggi goreng"},
    {"id": 3, "item": "teh tarik"}
]

@app.route('/')
def index():
    if orders:
        return render_template('index-keyon.html', orders=orders)
    else:
        return render_template('no_comfirm_order.html')

@app.route('/process_order', methods=['POST'])
def process_order():
    order_id = int(request.form['order_id'])
    order = next((order for order in orders if order['id'] == order_id), None)
    if order:
        return render_template('comfirm_order.html', order=order)
    else:
        return "Order not found."

@app.route('/comfirm_order', methods=['POST'])
def confirm_order():
    decision = request.form['decision']
    order_id = int(request.form['order_id'])
    if decision == 'accept':
        order = next((order for order in orders if order['id'] == order_id), None)
        if order:
            return render_template('order_accepted.html', order=order)
        else:
            return "Order not found."
    elif decision == 'decline':
        if orders:
            return render_template('index-keyon.html', orders=orders)
        else:
            return render_template('no_comfirm_order.html')
    else:
        return "Invalid decision"

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
