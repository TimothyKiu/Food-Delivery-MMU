from flask import Flask, render_template, request
import mysql.connector

# Example orders data (can be replaced with database queries)
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
        return "Order declined"
    else:
        return "Invalid decision"

if __name__ == '__main__':
    app.run(debug=True)
