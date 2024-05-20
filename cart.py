from flask import Flask, request, render_template,redirect, url_for
import mysql.connector

#NOTE: STOP RUNNING PYTHON WHENEVER YOU WANNA ALTER SQL TABLES
db = mysql.connector.connect(
    host="localhost",
    user='root',
    passwd='Chan@125',
    database='customer'
)

cursor = db.cursor()

app = Flask(__name__)
app.secret_key = "oisdsaoidiosad"


@app.route('/', methods=['GET']) 
def menu():
    with open("remarks.txt", "r") as file:
        remarks = file.read()
    return render_template('menu.html', remarks=remarks)

@app.route('/home', methods=['GET']) 
def home():
    return render_template('home.html')

@app.route('/deen', methods=['GET']) 
def deen():
    return render_template('deen.html')

@app.route('/htc', methods=['GET']) 
def htc():
    return render_template('htc.html')

@app.route('/bakery', methods=['GET']) 
def bakery():
    return render_template('dlight_bakery.html')

@app.route('/add_to_cart', methods=['POST', 'GET']) 
def add_to_cart():
    if request.method == 'POST':
        

        remarks = request.form['remarks']
        testvalue = "x"
        print(remarks)
        sql = "INSERT INTO customer.user_remarks (remarks, username) VALUES (%s, %s)"
    
        cursor.execute(sql, (remarks, testvalue))
        db.commit()
        
        # with open("remarks.txt", "a") as file:
        #     file.write(remarks + "\n")
        # print(remarks)

        # return render_template('menu.html', remarks=remarks)
    return render_template("menu.html", remarks=remarks, testvalue=testvalue)

@app.route('/')  # Assuming you want to display remarks on the root route
def display_remarks():
  # Connect to database (省略 - omitted for brevity)
  cursor = db.cursor()
  cursor.execute("SELECT remarks FROM user_remarks")
  remarks_data = cursor.fetchall()  # Fetch all remarks as a list of tuples
  cursor.close()  # Close the cursor
  return render_template('menu.html', remarks=remarks_data)


app.run(debug=True)