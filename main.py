from urllib import request
from flask import Flask,render_template, request, redirect, url_for, session

from loginLogic import loginLogic

import json
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user='root',
    passwd='0000',
    database='mysql'
)

mycursor = db.cursor()

app = Flask(__name__)
app.secret_key = 'theSecretKeyToTheEvilPiratesTreasureHarHarHar'


# Dummy data for testing purposes
users = {'john': 'password',
         'jane': 'password123',
         'bomboman': 'fentanyllover123'
         }


@app.route('/successlogin')
def successlogin():
    return render_template('successlogin.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    loginlogic1 = loginLogic()
    return loginlogic1.login(session, users, db)

@app.route('/register', methods=['GET', 'POST'])
def register():
    session.setdefault('nametaken', False)

    if request.method == 'POST':
        # Request from the html button with the name 'username'
        usernamereg = request.form['usernamereg']
        passwordreg = request.form['passwordreg']

        #dumps is the stringify but for python
        stringpassword = json.dumps(passwordreg)

        if not(usernamereg in users):
            if stringpassword.length() >= 6:
                session['nametaken'] = False
                # Redirect using the function name, NOT the app.route(/example)
                cursor = db.cursor()
                query = "INSERT INTO registeredAccounts (user_name, user_password) VALUES (%s, %s)"
                cursor.execute(query, (stringpassword, usernamereg,))
                db.commit()
                cursor.close()
                return redirect(url_for("successlogin"))
        else:
            session['nametaken'] = True
            return render_template('register.html', nametakenHTML=session.get('nametaken'))

    return render_template('register.html')

#DO NOT STORE SESSION VARIABLES AS SELF
#This is where the template will be stored in the url
@app.route('/frontpage')
def index():
    #Draw the website template from the folder!
    return render_template('frontpage.html')

@app.route('/createaccount')
def createAccount():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    else:
        return render_template('createaccount.html')

@app.route('/html2')
def page2():
    return render_template('html2.html')

app.run(debug=True)
