from urllib import request
from flask import Flask,render_template, request, redirect, url_for, session, jsonify

from loginLogic import loginLogic
from registerLogic import registerLogic

import json
import mysql.connector

#NOTE: STOP RUNNING PYTHON WHENEVER YOU WANNA ALTER SQL TABLES
db = mysql.connector.connect(
    host="localhost",
    user='root',
    passwd='0000',
    database='webDB'
)

mycursor = db.cursor(buffered=True)

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
    registerlogic = registerLogic()
    return registerlogic.register(session, users, db, mycursor)

#DO NOT STORE SESSION VARIABLES AS SELF VARIABLES
#This is where the template will be stored in the url
@app.route('/ratings', methods=['GET', 'POST'])
def ratings():
    if request.method == 'POST':
        ratings = request.form.get('rating')
        review = request.form.get('writeReview')
        usernameR = request.form.get('runnerName')


        insert_query = "INSERT INTO webDB.reviews (user_name, review_text, rating_given) VALUES (%s, %s, %s)"
        mycursor.execute(insert_query, (usernameR, review, ratings,))
        db.commit()  # Commit the transaction to save changes to the database

        # Create temporary table
        mycursor.execute('''
               CREATE TEMPORARY TABLE IF NOT EXISTS temp_accumulative AS
               SELECT user_name, AVG(rating_given) AS total_rating
               FROM reviews
               GROUP BY user_name
           ''')

        # Update main table with values from temporary table
        mycursor.execute('''
               UPDATE reviews rev
               JOIN temp_accumulative temp ON rev.user_name = temp.user_name
               SET rev.accumulative_reviews = temp.total_rating
           ''')

        # Commit changes and close connection
        db.commit()

        return redirect(url_for("ratingsent"))

    #Draw the website template from the folder!
    return render_template('ratings.html')

@app.route('/ratingsent', methods=['GET', 'POST'])
def ratingsent():
    return render_template('ratingsent.html')

def index():
    #Draw the website template from the folder!
    return render_template('frontpage.html')

@app.route('/accountcreatedsuccess')
def accountcreatedsuccess():

    return render_template('accountcreatedsuccess.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():

    print(session.get('loggedIn'))

    if session.get('loggedIn') == True:
        # Retrieve the username from the session or set it to None if the key is missing
        usernameP = session.get('username')
        loggedIn = session.get('loggedIn')
        errorText = "placeholder"

        query = "SELECT accumulative_reviews FROM webDB.reviews WHERE user_name = %s "
        mycursor.execute(query, (usernameP,))
        ratingArray = mycursor.fetchall()
        ratings = ratingArray[0]

        # Execute the SQL query with the username and password as parameters
        # This is where user enters his credentials in the HTML page, the parameter values then are run into the
        # query, if it finds a match it returns something back, if not then it returns null
        mycursor.execute(query, (usernameP,))
        # Fetch the result (assuming only one row is expected)

        if request.method == 'POST':
            # Retrieve the value of the 'logOut' form field

            loggedOut = request.form.get('logOut')
            deleteAccount = request.form.get('deleteAccount')

            noLoginYet = "You haven't logged in!"
            accountDeleted = "Account successfully deleted..."

            if loggedOut == "True":
                # Remove the 'username' key from the session if the user logs out
                session['username'] = None
                session['loggedIn'] = False
                errorText = "Logged out."

                return redirect(url_for("login"))


            if deleteAccount == "True": #works
                deleteQuery = "DELETE FROM webDB.registeredAccounts WHERE user_name = %s"
                mycursor.execute(deleteQuery, (session['username'],))
                db.commit()

                session['username'] = None
                session['loggedIn'] = False
                errorText = "Account deleted successfully."

                # DO NOT DO THIS, THIS DIRECTLY TAMPERS THE CODE, USE HTML/JS
                # if loggedOut == "True":
                #     session['username'] = "You can't delete now! Youve already logged out..."

        return render_template('profile.html', usernameP=usernameP, loggedIn=loggedIn, errorText=errorText, ratings=ratings)

    else:
        return redirect(url_for("login"))


app.run(debug=True)
