from urllib import request
from flask import Flask,render_template, request, redirect, url_for, session, jsonify

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
    return loginlogic1.login(session, users, db, mycursor)

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        session.setdefault('nametaken', False)
        session.setdefault('passproperlength', True)
        session.setdefault('passSameWithConfirm', True)

        # Request from the html button with the name 'username'
        usernamereg = request.form['usernamereg']
        passwordreg = request.form['passwordreg']
        confirmpasswordreg = request.form['confirmpasswordreg']

        if not(usernamereg in users):
            if len(passwordreg) >= 6 and (passwordreg == confirmpasswordreg):
                session['nametaken'] = False
                cursor = db.cursor()
                query = "INSERT INTO mysql.registeredAccounts (user_name, user_password) VALUES (%s, %s)"
                cursor.execute(query, (usernamereg, passwordreg,))
                db.commit()
                cursor.close()

                # Redirect using the function name, NOT the app.route(/example)
                session['passproperlength'] = True
                session['passSameWithConfirm'] = True
                return redirect(url_for("successlogin", passproperlength=session.get('passproperlength')),)

            if len(passwordreg) < 6 or len(passwordreg) > 10:
                session['passproperlength'] = False
                print("Password not proper length")
                #RUNS FINE!
                return render_template('register.html', passproperlength=session.get('passproperlength'))
            elif (not(passwordreg == confirmpasswordreg)):
                session['passSameWithConfirm'] = False
                print("Password not same")
                return render_template('register.html', passSameWithConfirm=session.get('passSameWithConfirm'))

        else:
            return render_template('register.html')

        return render_template('register.html')

    else:
        # Retrieve session variables for rendering the template
        passproperlength = session.get('passproperlength')
        passSameWithConfirm = session.get('passSameWithConfirm')
        # passSameWithConfirm = session.get('passSameWithConfirm')
        return render_template('register.html',
                               passproperlength=passproperlength,
                               passSameWithConfirm=passSameWithConfirm)
                               # passSameWithConfirm=passSameWithConfirm)

    # else:
    #     passproperlength = request.args.get('passproperlength', True)
    #     passSameWithConfirm = request.args.get('passSameWithConfirm', True)
    #     #                                                     this is to convert python variable into html format variable
    #     return render_template('register.html',
    #                        passproperlength=passproperlength,
    #                        passSameWithConfirm=passSameWithConfirm
    #                        )

#DO NOT STORE SESSION VARIABLES AS SELF VARIABLES
#This is where the template will be stored in the url

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
