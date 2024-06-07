from flask import Flask, render_template, request, jsonify
import mysql.connector

# NOTE: STOP RUNNING PYTHON WHENEVER YOU WANNA ALTER SQL TABLES
db = mysql.connector.connect(
    host="localhost",
    user='root',
    passwd='0000',
    database='webdb'
)

cursor = db.cursor(dictionary=True)

app = Flask(__name__)


@app.route('/')
def index():
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    if orders:
        return render_template('index-keyon.html', orders=orders)
    else:
        return render_template('no_comfirm_order.html')


@app.route('/process_order', methods=['POST'])
def process_order():
    try:
        order_id = int(request.form['order_id'])
    except ValueError:
        return "Invalid order ID."

    cursor.execute("SELECT * FROM orders WHERE ID = %s", (order_id,))
    order = cursor.fetchone()
    if order:
        return render_template('comfirm_order.html', order=order)
    else:
        return "Order not found."


@app.route('/comfirm_order', methods=['POST'])
def confirm_order():
    decision = request.form['decision']
    try:
        order_id = int(request.form['order_id'])
    except ValueError:
        return "Invalid order ID."

    if decision == 'accept':
        cursor.execute("SELECT * FROM orders WHERE ID = %s", (order_id,))
        order = cursor.fetchone()
        if order:
            return render_template('order_accepted.html', order=order)
        else:
            return "Order not found."
    elif decision == 'decline':
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
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
    order_id = data.get('order_id')

    if not all([latitude, longitude, order_id]):
        return "Invalid data received", 400

    sql = """
    INSERT INTO location (order_id, latitude, longitude)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE
        latitude = VALUES(latitude),
        longitude = VALUES(longitude),
        last_updated = CURRENT_TIMESTAMP
    """
    val = (order_id, latitude, longitude)
    cursor.execute(sql, val)
    db.commit()

    print(f"Rider location: Latitude {latitude}, Longitude {longitude}")
    return f"Rider location: Latitude {latitude}, Longitude {longitude}"


if __name__ == '__main__':
    app.run(debug=True)
