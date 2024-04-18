from urllib import request
from flask import Flask,render_template, request, redirect, url_for, session
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

#Do not use self variables, flask does not like it..
#This is where the template will be stored in the url
@app.route('/html')
def index():
    #Draw the website template from the folder!
    return render_template('html.html')


#Post means send or create, an attempt will be made to the server, if conditions are right it will return you back with a status
@app.route('/login', methods=['GET', 'POST'])
def login():
    #DO NOT INITIALIZE THIS VARIABLE IN THE FUNCTION, IT WILL KEEPING ON LOOPING THE SAME VARIABLE
    #EVERYTIME A USER DOES A POST REQUEST
    #firstAttempt = True
    session.setdefault('loginAttempts', -1)
    # session.setdefault('firstAttempt', False)
    # session.setdefault('secondAttempt', False)
    # session.setdefault('thirdAttempt', False)
    # session.setdefault('fourthAttempt', False)
    # session.setdefault('fifthAttempt', False)

    #The trues and falses are the default variables that they will start with

    if request.method == 'POST':
        #Request from the html button with the name 'username'
        username = request.form['username']
        password = request.form['password']


        if username in users and users[username] == password:
            return redirect(url_for('welcome', login_failed=False))

        else:
            session['firstAttempt'] = True
            session['loginAttempts'] += 1

            cursor = db.cursor()
            query = "INSERT INTO clicks (click_id, username) VALUES (%s, %s)"
            cursor.execute(query, (42069, username,))

            # query1 = "INSERT INTO clicks (url) VALUES (%s)"
            # cursor.execute(query1, (username,))

            db.commit()
            cursor.close()

            return redirect(url_for('login', login_failed=True))

    else:
        # Check if login failed from query parameter
        login_failed = request.args.get('login_failed', False)
        #                                                     this is to convert python variable into html format variable
        return render_template('login.html',
                               login_failed=login_failed,
                               firstAttempt=session.get('firstAttempt'),
                               # attempts=session.get('loginAttempts'),
                               # firstAttempt=session.get('loginAttempts', 0),
                               # secondAttempt=session.get('loginAttempts', 1),
                               # thirdAttempt=session.get('loginAttempts', 2),
                               # fourthAttempt=session.get('loginAttempts', 3)
                               )


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

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
