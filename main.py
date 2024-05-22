from urllib import request
from flask import Flask,render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from loginLogic import loginLogic
from registerLogic import registerLogic
import os
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
mycursor.execute("SHOW GRANTS FOR 'root'@'localhost'")



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


@app.route('/otherratings', methods=['GET', 'POST'])
def otherratings():
    if session.get('loggedIn') == True:

        usernameP = "Search for reviews"

        reviewText = []
        timeStamps = []
        totalReviews = len(timeStamps)
        reviewStars = []
        reviewSize = len(reviewText)
        ratings = "N/A"

        nickname = "N/A"
        phone_number = "N/A"
        user_name = "N/A"

        if request.method == 'POST':

            username = request.form['username']
            usernameP = username

            getInfo = "SELECT nickname, phone_number, user_name FROM webDB.registeredAccounts WHERE user_name = %s"
            mycursor.execute(getInfo, (usernameP,))
            infoArray = mycursor.fetchall()

            if infoArray[0][0] == None:
                nickname = "Not set"
            else:
                nickname = infoArray[0][0]
            if infoArray[0][1] == None:
                phone_number = "Not set"
            else:
                phone_number = infoArray[0][1]
            user_name = infoArray[0][2]




            # Retrieve the value of the 'logOut' form field
            query = "SELECT average_rating FROM webDB.average_reviews WHERE username = %s "
            mycursor.execute(query, (username,))
            ratingsArray = mycursor.fetchall()

            if ratingsArray:  # Check if ratingsArray is not empty
                ratings = round(float(ratingsArray[0][0]), 2)
            else:
                ratings = "N/A"

            # Execute the SQL query with the username and password as parameters
            # This is where user enters his credentials in the HTML page, the parameter values then are run into the
            # query, if it finds a match it returns something back, if not then it returns null

            query2 = "SELECT review_text, rating_given, timestamp FROM webDB.reviews WHERE user_name = %s"
            mycursor.execute(query2, (username,))
            reviewsArray = mycursor.fetchall()
            if reviewsArray:  # Check if ratingsArray is not empty
                reviewsGiven = reviewsArray[0][0]
                ratingsGiven = reviewsArray[0][1]
                timestamp = reviewsArray[0][2]
            else:
                reviewText = "N/A"
                ratingsGiven = "N/A"
                timestamp = "N/A"

            # Store each review tab in an array

            for i in range(len(reviewsArray)):
                reviewText.append(reviewsArray[i][0])

            reviewSize = len(reviewText)

            reviewStars = []
            for i in range(len(reviewsArray)):
                reviewStars.append(reviewsArray[i][1])

            timeStamps = []
            for i in range(len(reviewsArray)):
                timeStamps.append(reviewsArray[i][2])

            for k in range(len(timeStamps)):
                print(reviewStars[k])
                print(reviewText[k])
                print(timeStamps[k])

            totalReviews = len(timeStamps)

            loggedOut = request.form.get('logOut')
            deleteAccount = request.form.get('deleteAccount')

            noLoginYet = "You haven't logged in!"
            accountDeleted = "Account successfully deleted..."


                # DO NOT DO THIS, THIS DIRECTLY TAMPERS THE CODE, USE HTML/JS
                # if loggedOut == "True":
                #     session['username'] = "You can't delete now! Youve already logged out..."

        return render_template('otherratings.html', usernameP=usernameP,
                                ratings=ratings, reviewText=reviewText, reviewStars=reviewStars,
                               timeStamps=timeStamps, totalReviews=totalReviews, reviewSize=reviewSize,
                               nickname=nickname, phone_number=phone_number, user_name=user_name,)

    else:
        return redirect(url_for("login"))

    return render_template("otherratings.html")
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

        query2 = "SELECT review_text, rating_given, timestamp FROM webDB.reviews WHERE user_name = %s"
        mycursor.execute(query2, (usernameP,))
        reviewsArray = mycursor.fetchall()
        if reviewsArray:  # Check if ratingsArray is not empty
            reviewsGiven = reviewsArray[0][0]
            ratingsGiven = reviewsArray[0][1]
            timestamp = reviewsArray[0][2]
        else:
            reviewText = "N/A"
            ratingsGiven = "N/A"
            timestamp = "N/A"

        #Store each review tab in an array
        reviewText = []
        for i in range(len(reviewsArray)):
            reviewText.append(reviewsArray[i][0])

        reviewSize = len(reviewText)

        reviewStars = []
        for i in range(len(reviewsArray)):
            reviewStars.append(reviewsArray[i][1])

        timeStamps = []
        for i in range(len(reviewsArray)):
            timeStamps.append(reviewsArray[i][2])

        for k in range(len(timeStamps)):
            print(reviewStars[k])
            print(reviewText[k])
            print(timeStamps[k])

        totalReviews = len(timeStamps)

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

        return render_template('profile.html', usernameP=usernameP, loggedIn=loggedIn,
                               errorText=errorText, ratings=ratings, reviewText=reviewText, reviewStars=reviewStars,
                               timeStamps=timeStamps, totalReviews=totalReviews, reviewSize=reviewSize)

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
        attemptedPasswordChange = False

        changepasssworderror = False
        errorText = "placeholder"
        nickname = "placeholder"
        phoneNumber = "placeholder"

        # Retrieve the username from the session or set it to None if the key is missing
        query = "SELECT phone_number, nickname FROM webDB.registeredAccounts WHERE user_name = %s "
        mycursor.execute(query, (usernameP,))
        test1 = mycursor.fetchone()
        if test1 is not None:
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
                    passwordNotSame = False
                    attemptedPasswordChange = True

                else:
                    print("Passwords do not match")
                    passwordNotSame = True
                    attemptedPasswordChange = True

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
                               ratings=ratings, changepasssworderror=changepasssworderror, nickname=nickname,
                               phoneNumber=phoneNumber, passwordNotSame=passwordNotSame,
                               attemptedPasswordChange=attemptedPasswordChange)

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

# @app.route('/testfile')
# def testfile():
#     return render_template('testfile.html')

deen_food = [
    {'name': 'CHICKEN CHOP COMBO (Rice)', 'price': 7.00, 'category': 'Western'},
    {'name': 'CHICKEN CHOP COMBO (Fried Rice)', 'price': 8.50, 'category': 'Western'},
    {'name': 'ROTI BAKAR', 'price': 1.50, 'category': 'Western'},
    {'name': 'SANDWICH AYAM', 'price': 2.50, 'category': 'Western'},
    {'name': 'SANDWICH SARDIN', 'price': 2.50, 'category': 'Western'},
    {'name': 'ROT JOHN', 'price': 5.00, 'category': 'Western'},
    {'name': 'FRIES', 'price': 5.00, 'category': 'Western'},
    {'name': 'WET FRIES', 'price': 5.00, 'category': 'Western'},
    {'name': 'FISH & CHIPS', 'price': 11.00, 'category': 'Western'},
    {'name': 'CHICKEN CHOP (REGULAR)', 'price': 12.00, 'category': 'Western'},
    {'name': 'CHICKEN GRILL', 'price': 15.00, 'category': 'Western'},
    {'name': 'LAMB CHOP', 'price': 18.00, 'category': 'Western'},
    {'name': 'FRIED NOODLES', 'price': 5.00, 'category': 'Chinese'},
    {'name': 'KUEY TIAU GOREN', 'price': 5.00, 'category': 'Chinese'},
    {'name': 'BIHUN GOREN', 'price': 5.00, 'category': 'Chinese'},
    {'name': 'BIHUN SINGAPORE', 'price': 5.00, 'category': 'Chinese'},
    {'name': 'MEE GOREN', 'price': 5.00, 'category': 'Chinese'},
    {'name': 'MEE GORENG MAMAK', 'price': 5.00, 'category': 'Chinese'},
    {'name': 'MAGGIE GOREN', 'price': 5.00, 'category': 'Chinese'},
    {'name': 'YEE MEE GOREN', 'price': 6.00, 'category': 'Chinese'},
    {'name': 'HOKKIEN MEE', 'price': 6.00, 'category': 'Chinese'},
    {'name': 'MAGGIE GORENG XLR', 'price': 7.00, 'category': 'Chinese'},
    {'name': 'CHINESE STYLE', 'price': 0.00, 'category': 'Chinese'},  # Header for Chinese-style dishes
    {'name': 'NASI BUTTER CHICKEN', 'price': 8.00, 'category': 'Chinese'},
    {'name': 'NASI BUTTER FISH', 'price': 8.00, 'category': 'Chinese'},
    {'name': 'NASI BUTTER PRAWN', 'price': 9.00, 'category': 'Chinese'},
    {'name': 'NASI BUTTER SQUID', 'price': 9.00, 'category': 'Chinese'},
    {'name': 'NASI BUTTER CAMPUR', 'price': 10.00, 'category': 'Chinese'},
    {'name': 'NASI BUTTER MILK (CN)', 'price': 10.00, 'category': 'Chinese'},
    {'name': 'TOM YAM SOUP + RICE', 'price': 7.00, 'category': 'Soups'},
    {'name': 'TOM YAM SOUP (CENDAWAN)', 'price': 7.00, 'category': 'Soups'},
    {'name': 'TOM YAM SOUP (AYAM)', 'price': 7.00, 'category': 'Soups'},
    {'name': 'TOM YAM SOUP (DAGING)', 'price': 8.00, 'category': 'Soups'},
    {'name': 'TOM YAM SOUP (SEA FOOD)', 'price': 8.00, 'category': 'Soups'},
    {'name': 'TOM YAM SOUP (CAMPUR)', 'price': 8.50, 'category': 'Soups'},
    {'name': 'MAGGIE SOUP', 'price': 5.00, 'category': 'Soups'},
    {'name': 'KUEY TIAU SOUP', 'price': 5.00, 'category': 'Soups'},
    {'name': 'BIHUN SOUP', 'price': 5.00, 'category': 'Soups'},
    {'name': 'VEGETARIAN + NASI', 'price': 6.00, 'category': 'Soups'},
    {'name': 'CENDAWAN + NASI', 'price': 6.00, 'category': 'Soups'},
    {'name': 'AYAM + NASI', 'price': 6.00, 'category': 'Soups'},  # Likely a mistake on the menu, assuming this should not be Vegetarian
    {'name': 'DAGING + NASI', 'price': 7.00, 'category': 'Soups'},  # Likely a mistake on the menu, assuming this should not be Vegetarian
    {'name': 'KAMBING + NASI', 'price': 10.00, 'category': 'Soups'},
    {'name': 'NASI GORENG / FRIED RICE', 'price': 0.00, 'category': 'Nasi Goreng'},  # Header for Nasi Goreng dishes
    {'name': 'NASI GORENG BIASA (RM5)', 'price': 5.00, 'category': 'Nasi Goreng'},  # Assuming "BIASA" means "Normal"
    {'name': 'NASI GORENG KAMPUNG', 'price': 6.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG CIN', 'price': 5.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG MAMAK', 'price': 5.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG TELUR (EGG)', 'price': 5.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG CILI API', 'price': 5.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG SAUSAGE', 'price': 5.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG TOMYAM', 'price': 6.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG SARDIN', 'price': 6.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG PATTAYA', 'price': 6.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG IKAN MASIN', 'price': 6.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG TOMATO', 'price': 6.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG CENDAWAN', 'price': 6.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG DAGING', 'price': 7.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG SEA FOOD', 'price': 7.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG AYAM (CHICKEN)', 'price': 8.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG PAPRIK AYAM', 'price': 8.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG MSA (EGG)', 'price': 9.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG THAI', 'price': 9.00, 'category': 'Nasi Goreng'},
    {'name': 'NASI GORENG KAMBING', 'price': 12.00, 'category': 'Nasi Goreng'},
    {'name': 'PASTA SPECIAL', 'price': 0.00, 'category': 'Pasta'},  # Header for Pasta dishes
    {'name': 'CARBONARA', 'price': 10.00, 'category': 'Pasta'},
    {'name': 'CHICKEN ALFRED', 'price': 10.00, 'category': 'Pasta'},
    {'name': 'BOLONESE', 'price': 10.00, 'category': 'Pasta'},
    {'name': 'PASTA VEGETARIAN', 'price': 10.00, 'category': 'Pasta'},
    {'name': 'MARINARA', 'price': 12.00, 'category': 'Pasta'},
    {'name': 'CHICKEN SPICY', 'price': 12.00, 'category': 'Pasta'},
    {'name': 'HOT PLATE', 'price': 0.00, 'category': 'Other'},  # Header for Hot Plate dishes
    {'name': 'CHAR KUEY TIAU', 'price': 6.00, 'category': 'Other'},
    {'name': 'SIZZLING RICE', 'price': 6.00, 'category': 'Other'},
    {'name': 'MEE BANDUNG', 'price': 6.00, 'category': 'Other'},
    {'name': 'SIZZLING YEE MEE', 'price': 6.50, 'category': 'Other'},
    {'name': 'CANTONESE YEE MEE', 'price': 7.00, 'category': 'Other'},
    {'name': 'CANTONESE JUEY TIAU', 'price': 7.00, 'category': 'Other'},
    {'name': 'YING YONG', 'price': 8.00, 'category': 'Other'},
    {'name': 'TEH TARIK', 'price': 2.00, 'category': 'Drinks'},  # Assuming Teh refers to Tea
    {'name': 'TEH O', 'price': 1.50, 'category': 'Drinks'},
    {'name': 'TEH O LIMAU', 'price': 2.00, 'category': 'Drinks'},
    {'name': 'TEH O LAICI', 'price': 3.50, 'category': 'Drinks'},
    {'name': 'NESCAFE', 'price': 2.50, 'category': 'Drinks'},
    {'name': 'NESCAFE O', 'price': 2.00, 'category': 'Drinks'},
    {'name': 'NESLO', 'price': 3.00, 'category': 'Drinks'},
    {'name': 'WHITE COFFEE', 'price': 3.00, 'category': 'Drinks'},
    {'name': 'KOPI', 'price': 2.00, 'category': 'Drinks'},
    {'name': 'KOPI O', 'price': 1.50, 'category': 'Drinks'},
    {'name': 'MILO', 'price': 2.50, 'category': 'Drinks'},
    {'name': 'MILO O', 'price': 2.50, 'category': 'Drinks'},
    {'name': 'BARLEY', 'price': 2.00, 'category': 'Drinks'},
    {'name': 'HORLICKS', 'price': 3.00, 'category': 'Drinks'},
    {'name': 'LIMAU PANAS', 'price': 2.00, 'category': 'Drinks'},
    {'name': 'LAICI', 'price': 3.00, 'category': 'Drinks'},  # Assuming referring to juice
    {'name': 'SIRAP BANDUNG', 'price': 2.00, 'category': 'Drinks'},
    {'name': 'FRUIT JUICE', 'price': 0.00, 'category': 'Drinks'},  # Header for Fruit Juices
    {'name': 'ORANGE JUICE', 'price': 4.00, 'category': 'Drinks'},
    {'name': 'APPLE JUICE', 'price': 4.00, 'category': 'Drinks'},
    {'name': 'WATERMELON JUICE', 'price': 4.00, 'category': 'Drinks'},
    {'name': 'EXTRA JASS', 'price': 3.50, 'category': 'Drinks'},
    {'name': 'CARROT JUICE', 'price': 4.00, 'category': 'Drinks'},
]

htc_food = [
    {'name': 'GORENG-GORENG', 'price': 0.00, 'category': 'Goreng'},  # Header for goreng dishes
    {'name': 'NASI GORENG', 'price': 4.50, 'category': 'Goreng'},
    {'name': 'NASI GORENG DOUBLE', 'price': 6.00, 'category': 'Goreng'},
    {'name': 'NASI GORENG CILI PADIR', 'price': 6.00, 'category': 'Goreng'},
    {'name': 'NASI GORENG CINAR', 'price': 5.00, 'category': 'Goreng'},
    {'name': 'NASI GORENG KAMPUNG', 'price': 6.00, 'category': 'Goreng'},
    {'name': 'NASI GORENG AYAM', 'price': 8.00, 'category': 'Goreng'},
    {'name': 'NASI GORENG KAMPUNG [AYAM]', 'price': 9.00, 'category': 'Goreng'},
    {'name': 'NASI GORENG PATTAYA', 'price': 6.00, 'category': 'Goreng'},
    {'name': 'MAGGI', 'price': 4.50, 'category': 'Goreng'},
    {'name': 'MAGGI DOUBLE', 'price': 7.00, 'category': 'Goreng'},
    {'name': 'MAGGI DOUBLE AYAM', 'price': 10.00, 'category': 'Goreng'},
    {'name': 'MEE', 'price': 4.50, 'category': 'Goreng'},
    {'name': 'BIHUN', 'price': 4.50, 'category': 'Goreng'},
    {'name': 'KUEY TEOW', 'price': 4.50, 'category': 'Goreng'},
    {'name': 'ROJAK', 'price': 4.50, 'category': 'Goreng'},
    {'name': 'TELUR MATA', 'price': 1.00, 'category': 'Goreng'},
    {'name': 'TELUR DADAR', 'price': 1.50, 'category': 'Goreng'},
    {'name': 'MEE/KUE TEOW/BIHUN', 'price': 4.50, 'category': 'Goreng'},  # Assuming this refers to a combo
    {'name': 'MEE/NASI GORENG', 'price': 4.50, 'category': 'Goreng'},  # Assuming this refers to a combo
    {'name': 'KUE TEOW/BIHUN GORENG', 'price': 4.50, 'category': 'Goreng'},  # Assuming this refers to a combo
    {'name': 'ROJAK BIASA', 'price': 5.50, 'category': 'Goreng'},
    {'name': 'ROJAK TELUR', 'price': 5.50, 'category': 'Goreng'},
    {'name': 'ROJAK MEE/MEE', 'price': 5.50, 'category': 'Goreng'},  # Assuming this is a typo and should be "ROJAK MEE/BIHUN"
    {'name': 'ROTI CANAI', 'price': 0.00, 'category': 'Roti'},  # Header for Roti dishes
    {'name': 'BIAS', 'price': 1.20, 'category': 'Roti'},
    {'name': 'TELUR', 'price': 2.50, 'category': 'Roti'},
    {'name': 'TELUR BAWANG', 'price': 3.00, 'category': 'Roti'},
    {'name': 'BAWANG', 'price': 2.00, 'category': 'Roti'},
    {'name': 'PLANTAR', 'price': 2.50, 'category': 'Roti'},
    {'name': 'BOOM', 'price': 2.50, 'category': 'Roti'},
    {'name': 'CHEESE', 'price': 3.00, 'category': 'Roti'},
    {'name': 'TELUR CHEESE', 'price': 4.00, 'category': 'Roti'},
    {'name': 'SARDINE', 'price': 4.00, 'category': 'Roti'},
    {'name': 'KAYA', 'price': 2.50, 'category': 'Roti'},
    {'name': 'MADU', 'price': 2.50, 'category': 'Roti'},
    {'name': 'PISANG', 'price': 3.00, 'category': 'Roti'},
    {'name': 'TOSAI', 'price': 0.00, 'category': 'Tosai'},  # Header for Tosai dishes
    {'name': 'BIAS', 'price': 2.00, 'category': 'Tosai'},
    {'name': 'TELUR', 'price': 3.00, 'category': 'Tosai'},
    {'name': 'BAWANG', 'price': 3.00, 'category': 'Tosai'},
    {'name': 'MASALA', 'price': 3.50, 'category': 'Tosai'},
    {'name': 'GHEE', 'price': 3.00, 'category': 'Tosai'},
    {'name': 'MURTABAK', 'price': 4.50, 'category': 'Murtabak'},
    {'name': 'CAPATI', 'price': 2.00, 'category': 'Others'},
    {'name': 'SPECIAL', 'price': 0.00, 'category': 'Others'},  # Header for Special dishes
    {'name': 'ROTI BAKAR', 'price': 1.50, 'category': 'Others'},
    {'name': 'ROTI BAKAR TELUR', 'price': 3.00, 'category': 'Others'},
    {'name': 'ROTI BAKAR SARDIN', 'price': 4.00, 'category': 'Others'},
    {'name': 'MINUMAN', 'price': 0.00, 'category': 'Drinks'},  # Header for Drinks
    {'name': 'AIS TEH', 'price': 2.30, 'category': 'Drinks'},
    {'name': 'TEH O', 'price': 2.00, 'category': 'Drinks'},
    {'name': 'KOPI', 'price': 2.30, 'category': 'Drinks'},
    {'name': 'KOPI O', 'price': 2.00, 'category': 'Drinks'},
    {'name': 'MILO', 'price': 2.80, 'category': 'Drinks'},
    {'name': 'MILO O', 'price': 2.50, 'category': 'Drinks'},
    {'name': 'NESCAFE O', 'price': 2.50, 'category': 'Drinks'},
    {'name': 'NESCAFE', 'price': 2.80, 'category': 'Drinks'},
    {'name': 'BRU', 'price': 3.00, 'category': 'Drinks'},
    {'name': 'HORLICKS', 'price': 3.00, 'category': 'Drinks'},
    {'name': 'TEH LIMAU', 'price': 2.30, 'category': 'Drinks'},
    {'name': 'AIR SIRAP', 'price': 2.30, 'category': 'Drinks'},
    {'name': 'SIRAP LIMAU', 'price': 2.30, 'category': 'Drinks'},
    {'name': 'JUS BUAH-BUAHAN', 'price': 0.00, 'category': 'Drinks'},  # Header for Fruit Juices
    {'name': 'OREN/EPAL', 'price': 3.50, 'category': 'Drinks'},
    {'name': 'BELIMBING', 'price': 3.50, 'category': 'Drinks'},
    {'name': 'MANGGA/KAROT', 'price': 3.50, 'category': 'Drinks'},
    {'name': 'ASAM JAWA', 'price': 2.80, 'category': 'Drinks'},
    {'name': 'BARLI', 'price': 2.80, 'category': 'Drinks'}
]

bakery_food = [
    {'name': 'VANILLA CHOCO TIWIST', 'price': 4.50, 'category': 'Pastry'},
    {'name': 'CHICKEN CURRY PUFF', 'price': 4.50, 'category': 'Pastry'},
    {'name': 'TUNA PUFF', 'price': 4.50, 'category': 'Pastry'},
    {'name': 'BANANA BAR', 'price': 3.80, 'category': 'Pastry'},
    {'name': 'CHICKEN SAUSAGE DONUT', 'price': 4.50, 'category': 'Pastry'},
    {'name': 'GARLIC SAUSAGE ROLL', 'price': 5.50, 'category': 'Pastry'},
    {'name': 'BBQ SAUSAGE ROLL', 'price': 5.50, 'category': 'Pastry'},
    {'name': 'MINI CROISSANT', 'price': 2.00, 'category': 'Pastry'},
    {'name': 'MINI CHICKEN MUSHROOM PIE', 'price': 5.50, 'category': 'Pastry'},
    {'name': 'FIRE CRACKER SAUSAGE', 'price': 7.50, 'category': 'Pastry'},
    {'name': 'CHOCOLATE ROLL', 'price': 3.00, 'category': 'Pastry'},
    {'name': 'CHOCOLATE MUFFIN', 'price': 6.50, 'category': 'Pastry'},
    {'name': 'BLUEBERRY MUFFIN', 'price': 6.50, 'category': 'Pastry'},
    {'name': 'MINI MUFFIN RED VELVET', 'price': 2.50, 'category': 'Pastry'},
    {'name': 'MINI MUFFIN BUTTERSCOTCH', 'price': 2.50, 'category': 'Pastry'},
    {'name': 'CHOCOLATE CHIP COOKIES', 'price': 4.50, 'category': 'Pastry'},
    {'name': 'DOUBLE CHOCO CHIP COOKIES', 'price': 4.50, 'category': 'Pastry'},
    {'name': 'SPICY TUNA EGG SANDWICH', 'price': 4.00, 'category': 'Pastry'},
    {'name': 'EGG MAYO SANDWICH', 'price': 3.50, 'category': 'Pastry'},
    {'name': 'BIHUN GORENG', 'price': 5.00, 'category': 'Pastry'},
    {'name': 'NASI GORENG', 'price': 5.00, 'category': 'Pastry'},
    {'name': 'NASI LEMAK', 'price': 4.00, 'category': 'Pastry'},
    {'name': 'COFFEE', 'price': 0.00, 'category': 'Coffee'},  # Header for Coffee category
    {'name': 'S BLACK COFFEE', 'price': 4.00, 'category': 'Coffee'},
    {'name': 'WHITE COFFEE', 'price': 4.00, 'category': 'Coffee'},
    {'name': 'PREMIUM COFFEE', 'price': 0.00, 'category': 'Coffee'},  # Sub-header for Premium Coffee
    {'name': 'ESPRESSO', 'price': 5.50, 'category': 'Coffee'},
    {'name': 'AMERICAN', 'price': 6.50, 'category': 'Coffee'},
    {'name': 'LATTE', 'price': 7.50, 'category': 'Coffee'},
    {'name': 'CAPPUCCINO', 'price': 7.50, 'category': 'Coffee'},
    {'name': 'MOCHA', 'price': 8.50, 'category': 'Coffee'},
    {'name': 'COCONUT LATTE', 'price': 8.50, 'category': 'Coffee'},
    {'name': 'HAZELNUT LATTE', 'price': 8.50, 'category': 'Coffee'},
    {'name': 'FRENCH VANILLA LATTE', 'price': 8.50, 'category': 'Coffee'},
    {'name': 'SALTED CARAMEL LATTE', 'price': 8.50, 'category': 'Coffee'},
    {'name': 'NON COFFEE', 'price': 0.00, 'category': 'Coffee'},  # Sub-header for Non-Coffee drinks
    {'name': 'CHOCOLATE', 'price': 7.00, 'category': 'Coffee'},
    {'name': 'MATCHA LATTE', 'price': 7.80, 'category': 'Coffee'},
    {'name': 'MILO', 'price': 5.00, 'category': 'Coffee'},  # Likely a mistake, categorized under Coffee
    {'name': 'TEH TARIK', 'price': 5.00, 'category': 'Coffee'},
]


ITEMS = []
ITEMS.extend(bakery_food)
ITEMS.extend(deen_food)
ITEMS.extend(htc_food)


CART_FILE = 'cart.txt'

def read_cart():
    cart = {}
    if os.path.exists(CART_FILE):
        with open(CART_FILE, 'r') as file:
            for line in file:
                parts = line.strip().split(', ')
                if len(parts) >= 3:
                    try:
                        item_name = parts[0]
                        item_price = parts[1]
                        item_quantity = int(parts[2].replace(',', ''))  # Remove any extraneous commas
                        item_remarks = ', '.join(parts[3:]) if len(parts) > 3 else ''
                        cart[item_name] = {'price': item_price, 'quantity': item_quantity, 'remarks': item_remarks}
                    except ValueError as e:
                        print(f"Error parsing line: {line}. Error: {e}")
    return cart

def write_cart(cart):
    with open(CART_FILE, 'w') as file:
        for item_name, details in cart.items():
            file.write(f"{item_name}, {details['price']}, {details['quantity']}, {details['remarks']}\n")


@app.route('/', methods=['GET', 'POST'])
def index():
    store = request.args.get('store')  
    if store == 'htc':
        items = htc_food
    elif store == 'deen':
        items = deen_food
    else:
        items = bakery_food

    selected_item = None
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        selected_item = next((item for item in ITEMS if item['name'] == item_name), None)

    return render_template('dlight_bakery.html', items=items, cart=read_cart(), selected_item=selected_item)


@app.route('/', methods=['GET', 'POST'])
def bakery():
    cart = read_cart()
    selected_item = None
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        selected_item = next((item for item in ITEMS if item['name'] == item_name), None)
        if selected_item and item_name in cart:
            selected_item['quantity'] = cart[item_name]['quantity']
            selected_item['remarks'] = cart[item_name]['remarks']
        else:
            selected_item['quantity'] = 0
            selected_item['remarks'] = ''
    return render_template('dlight_bakery.html', items=ITEMS, cart=cart, selected_item=selected_item)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_name = request.form.get('item_name')
    item_price = request.form.get('item_price')
    cart = read_cart()
    if item_name in cart:
        cart[item_name]['quantity'] += 1
    else:
        cart[item_name] = {'price': item_price, 'quantity': 1, 'remarks': ''}
    write_cart(cart)
    return redirect(url_for('bakery'))

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    item_name = request.form.get('item_name')
    cart = read_cart()
    if item_name in cart:
        if cart[item_name]['quantity'] > 1:
            cart[item_name]['quantity'] -= 1
        else:
            del cart[item_name]
    write_cart(cart)
    return redirect(url_for('bakery'))

@app.route('/update_remarks', methods=['POST'])
def update_remarks():
    item_name = request.form.get('item_name')
    remarks = request.form.get('remarks')
    cart = read_cart()
    if item_name in cart:
        cart[item_name]['remarks'] = remarks
    write_cart(cart)
    return redirect(url_for('bakery'))



@app.route('/home', methods=['GET']) 
def home():
    usernameP = session.get('username', 'Guest')  # Default to 'Guest' if not set
    return render_template('/templates/home.html', usernameP=usernameP)

app.route('/profile')
def profile():
    # Retrieve the username from the session
    usernameP = session.get('username', 'Guest')  # Default to 'Guest' if not set
    return render_template('profile.html', usernameP=usernameP)

@app.route('/deen', methods=['GET']) 
def deen():
    return render_template('deen.html')

@app.route('/htc', methods=['GET']) 
def htc():
    return render_template('htc.html')

# @app.route('/add_to_cart', methods=['POST', 'GET']) 
# def add_to_cart():
#     if request.method == 'POST':
        

#         # remarks = request.form['remarks']
#         # testvalue = "x"
#         # print(remarks)
#         # sql = "INSERT INTO customer.user_remarks (remarks, username) VALUES (%s, %s)"
    
#         # cursor.execute(sql, (remarks, testvalue))
#         # db.commit()
        
#         with open("remarks.txt", "a") as file:
#             file.write(remarks + "\n")
#         print(remarks)

#     return render_template("menu.html", remarks=remarks, testvalue=testvalue)

# @app.route('/')  # Assuming you want to display remarks on the root route
# def display_remarks():
#   # Connect to database (省略 - omitted for brevity)
#   cursor = db.cursor()
#   cursor.execute("SELECT remarks FROM user_remarks")
#   remarks_data = cursor.fetchall()  # Fetch all remarks as a list of tuples
#   cursor.close()  # Close the cursor
#   return render_template('menu.html', remarks=remarks_data)




app.run(debug=True)
