from urllib import request
from flask import Flask,render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from loginLogic import loginLogic
from registerLogic import registerLogic

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
        # mycursor.execute('''CREATE TABLE IF NOT EXISTS average_reviews (
        #         ID INT AUTO_INCREMENT PRIMARY KEY,
        #         Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        #         username VARCHAR(255),
        #         total_ratings FLOAT,
        #         rating_count INT,
        #         average_rating FLOAT
        #         );
        #     ''')

        # Create temporary table
        mycursor.execute('''

                                
            INSERT INTO average_reviews (username, total_ratings, rating_count, average_rating)
            SELECT 
                user_name AS username,
                SUM(rating_given) AS total_ratings,
                COUNT(*) AS rating_count,
                SUM(rating_given) / COUNT(*) AS average_rating
            FROM 
                webDB.reviews
            GROUP BY 
                user_name
            ON DUPLICATE KEY UPDATE
                total_ratings = VALUES(total_ratings),
                rating_count = VALUES(rating_count),
                average_rating = VALUES(average_rating);

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
        usernameP = session.get('username')
        loggedIn = session.get('loggedIn')




        errorText = "placeholder"

        query = "SELECT average_rating FROM webDB.average_reviews WHERE username = %s "
        mycursor.execute(query, (usernameP,))
        ratingsArray = mycursor.fetchall()

        if ratingsArray:  # Check if ratingsArray is not empty
            ratings = round(float(ratingsArray[0][0]), 2)
        else:
            ratings = "N/A"

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

                return redirect(url_for("register"))

                # DO NOT DO THIS, THIS DIRECTLY TAMPERS THE CODE, USE HTML/JS
                # if loggedOut == "True":
                #     session['username'] = "You can't delete now! Youve already logged out..."

        return render_template('profile.html', usernameP=usernameP, loggedIn=loggedIn, errorText=errorText, ratings=ratings)

    else:
        return redirect(url_for("login"))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    print(session.get('loggedIn'))

    if session.get('loggedIn') == True:
        # Retrieve the username from the session or set it to None if the key is missing
        usernameP = session.get('username')
        loggedIn = session.get('loggedIn')

        passwordNotSame = False

        changepasssworderror = False
        errorText = "placeholder"



        # Retrieve the username from the session or set it to None if the key is missing
        query = "SELECT phone_number, nickname FROM webDB.registeredAccounts WHERE user_name = %s "
        mycursor.execute(query, (usernameP,))
        test1 = mycursor.fetchone()
        phoneNumber = test1[0]
        nickname = test1[1]




        query = "SELECT average_rating FROM webDB.average_reviews WHERE username = %s "
        mycursor.execute(query, (usernameP,))
        ratingsArray = mycursor.fetchall()

        if ratingsArray:  # Check if ratingsArray is not empty
            ratings = round(float(ratingsArray[0][0]), 2)
        else:
            ratings = "N/A"

        # Execute the SQL query with the username and password as parameters
        # This is where user enters his credentials in the HTML page, the parameter values then are run into the
        # query, if it finds a match it returns something back, if not then it returns null
        mycursor.execute(query, (usernameP,))
        # Fetch the result (assuming only one row is expected)

        if request.method == 'POST':
            # Retrieve the value of the 'logOut' form field

            loggedOut = request.form.get('logOut')
            deleteAccount = request.form.get('deleteAccount')
            changedPassword = request.form.get('changedPassword')
            changedNickname = request.form.get('changedNickname')
            changedPhoneNumber = request.form.get('changedPhoneNumber')


            passwordtext = request.form.get('confirmnewpassword')

            noLoginYet = "You haven't logged in!"
            accountDeleted = "Account successfully deleted..."

            if loggedOut == "True":
                # Remove the 'username' key from the session if the user logs out
                session['username'] = None
                session['loggedIn'] = False
                errorText = "Logged out."

                return redirect(url_for("login"))

            if deleteAccount == "True":  # works
                deleteQuery = "DELETE FROM webDB.registeredAccounts WHERE user_name = %s"
                mycursor.execute(deleteQuery, (session['username'],))
                db.commit()

                session['username'] = None
                session['loggedIn'] = False
                errorText = "Account deleted successfully."

                return redirect(url_for("register"))

                # DO NOT DO THIS, THIS DIRECTLY TAMPERS THE CODE, USE HTML/JS
                # if loggedOut == "True":
                #     session['username'] = "You can't delete now! Youve already logged out..."

            if changedPassword == "True":

                oldpassword = request.form['oldpassword']
                newpassword = request.form['newpassword']
                confirmnewpassword = request.form['confirmnewpassword']

                getpassword = "SELECT user_password from webDb.registeredAccounts WHERE user_name = %s "
                mycursor.execute(getpassword, (session['username'],))
                db.commit()

                userdata = mycursor.fetchone()


                if(newpassword == confirmnewpassword) and check_password_hash(userdata[0], oldpassword) :
                    alter_query = "UPDATE webDB.registeredAccounts SET user_password = %s WHERE user_name = %s"

                    hashedNewPassword = generate_password_hash(newpassword)
                    mycursor.execute(alter_query, (hashedNewPassword, usernameP))
                    db.commit()
                    print("Password changed successfully")

                elif newpassword != confirmnewpassword:
                    print("Passwords do not match")
                    passwordNotSame = True

            if changedNickname == "True":
                newNickname = request.form['newNickname']

                setNickname = "UPDATE webDb.registeredAccounts SET nickname = %s WHERE user_name = %s"

                mycursor.execute(setNickname, (newNickname, session['username']))
                db.commit()

            if changedPhoneNumber == "True":
                newPhoneNumber = request.form['newPhoneNumber']

                setNickname = "UPDATE webDb.registeredAccounts SET phone_number = %s WHERE user_name = %s"

                mycursor.execute(setNickname, (newPhoneNumber, session['username']))
                db.commit()


        return render_template('settings.html', usernameP=usernameP, loggedIn=loggedIn, errorText=errorText,
                               ratings=ratings, changepasssworderror=changepasssworderror, nickname=nickname, phoneNumber=phoneNumber, passwordNotSame=passwordNotSame)

    else:
        return redirect(url_for("settings"))
#
# @app.route('/testfile')
# def testfile():
#     if session.get('loggedIn') == True:
#         # Retrieve the username from the session or set it to None if the key is missing
#         usernameP = session.get('username')
#         loggedIn = session.get('loggedIn')
#         errorText = "placeholder"
#
#         query = "SELECT accumulative_reviews FROM webDB.reviews WHERE user_name = %s "
#         mycursor.execute(query, (usernameP,))
#         ratingsArray = mycursor.fetchall()
#
#         if ratingsArray:  # Check if ratingsArray is not empty
#             ratings = round(float(ratingsArray[0][0]), 2)
#         else:
#             ratings = "N/A"
#
#         # Execute the SQL query with the username and password as parameters
#         # This is where user enters his credentials in the HTML page, the parameter values then are run into the
#         # query, if it finds a match it returns something back, if not then it returns null
#         mycursor.execute(query, (usernameP,))
#         # Fetch the result (assuming only one row is expected)
#
#         if request.method == 'POST':
#             # Retrieve the value of the 'logOut' form field
#
#             loggedOut = request.form.get('logOut')
#             deleteAccount = request.form.get('deleteAccount')
#
#             noLoginYet = "You haven't logged in!"
#             accountDeleted = "Account successfully deleted..."
#
#             if loggedOut == "True":
#                 # Remove the 'username' key from the session if the user logs out
#                 session['username'] = None
#                 session['loggedIn'] = False
#                 errorText = "Logged out."
#
#                 return redirect(url_for("login"))
#
#             if deleteAccount == "True":  # works
#                 deleteQuery = "DELETE FROM webDB.registeredAccounts WHERE user_name = %s"
#                 mycursor.execute(deleteQuery, (session['username'],))
#                 db.commit()
#
#                 session['username'] = None
#                 session['loggedIn'] = False
#                 errorText = "Account deleted successfully."
#
#                 # DO NOT DO THIS, THIS DIRECTLY TAMPERS THE CODE, USE HTML/JS
#                 # if loggedOut == "True":
#                 #     session['username'] = "You can't delete now! Youve already logged out..."
#
#         return render_template('profile.html', usernameP=usernameP, loggedIn=loggedIn, errorText=errorText,
#                                ratings=ratings)
#
#     else:
#         return redirect(url_for("login"))

@app.route('/testfile')
def testfile():
    return render_template('testfile.html')


app.run(debug=True)
