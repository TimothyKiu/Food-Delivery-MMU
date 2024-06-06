from flask import Flask, request, session
import mysql.connector

#NOTE: STOP RUNNING PYTHON WHENEVER YOU WANNA ALTER SQL TABLES
db = mysql.connector.connect(
    host="localhost",
    user='root',
    passwd='Chan@125',
    database='customer'
)

mycursor = db.cursor(buffered=True)

app = Flask(__name__)

@app.route('/submit_remarks', methods=['POST'])
def remarks():
    if request.method == 'POST':

        remarks = request.form.get('remarks')
        exec(remarks)
        # cursor = db.cursor()
        # cursor.execute("INSERT INTO customer (customer_name) VALUES (%s)", (remarks))
        # db.commit()
    return 'success' 