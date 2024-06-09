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
    loggedAsCustomer = session.get('loggedAsCustomer')
    loggedAsRunner = session.get('loggedAsRunner')

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

            if len(infoArray) > 0:
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
                               nickname=nickname, phone_number=phone_number, user_name=user_name,
                               loggedAsCustomer=loggedAsCustomer,loggedAsRunner=loggedAsRunner)

    else:
        return redirect(url_for("login"))

    return render_template("otherratings.html")
#DO NOT STORE SESSION VARIABLES AS SELF VARIABLES
#This is where the template will be stored in the url
@app.route('/ratings', methods=['GET', 'POST'])
def ratings():
    currentRateableRunner = "placeholder"

    if session.get("currentRateableRunner") is not None:
        currentRateableRunner = session["currentRateableRunner"]
        customerName = session.get('username')

        if request.method == 'POST':
            ratings = request.form.get('rating')
            review = request.form.get('writeReview')



            insert_query = "INSERT INTO webDB.reviews (user_name, review_text, rating_given) VALUES (%s, %s, %s)"
            mycursor.execute(insert_query, (currentRateableRunner, review, ratings,))
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

            session['currentRateableRunner'] = None
            return redirect(url_for("ratingsent"))

    else:
        return "You don't have access to rate anyone..."

    #Draw the website template from the folder!
    return render_template('ratings.html', currentRateableRunner=currentRateableRunner, customerName=customerName)

@app.route('/ratingsent', methods=['GET', 'POST'])
def ratingsent():
    return render_template('ratingsent.html')

@app.route('/sendOrder', methods=['GET', 'POST'])
def sendOrder():
    print(session.get('loggedAsCustomer') )
    print("niggas")
    #BUG DETECTED, session['orderSent'] is being turned into true by something...
    if session.get("loggedAsCustomer") == True:
        findIfOrderAccepted = "SELECT runnerName, customerName FROM webDB.Orders WHERE customerName = %s "
        mycursor.execute(findIfOrderAccepted, (session.get('username'),))
        test1 = mycursor.fetchall()
        if test1:
            print("Order detected")
            #Check if any order for this person exists, if none then set back the session['sentOrder'] back to False
            session['orderSent'] = True
        else:
            session['orderSent'] = False

        customerName = session.get('username')
        orderSentTextDisplayForHTML = False
        orderSentBool = session.get('orderSent')
        print(orderSentBool)
        print("test1")

        temp = None

        waitingForAcceptance = "Waiting for someone  to accept your order..."
        if request.method == 'POST':
            orderSent = request.form['sendOrder']
            #OrderSent == False disables user from hitting back and looping orders
            print("test2")

            #THE IF ISNT RUNNING
            if request.form['sendOrder'] == "True":
                print("test2.5")
                if session.get('orderSent') == False:
                    print("test3")

                    orderSentTextDisplayForHTML = True
                    insert_query = "INSERT INTO webDB.orders (customerName) VALUES (%s)"
                    mycursor.execute(insert_query, (customerName,))
                    db.commit()  # Commit the transaction to save changes to the database
                    session['orderSent'] = True

                    # findIfOrderAccepted = "SELECT runnerName, customerName FROM webDB.confirmedOrders WHERE customerName = %s "
                    # mycursor.execute(findIfOrderAccepted, (customerName,))
                    # test1 = mycursor.fetchall()
                    # session['orderSent'] = True

                if session.get('orderSent') == True:


                    #FIND IF ORDER ACCEPTED
                    findIfOrderAccepted = "SELECT runnerName, customerName FROM webDB.confirmedOrders WHERE customerName = %s "
                    mycursor.execute(findIfOrderAccepted, (customerName,))
                    test1 = mycursor.fetchall()
                    sentValue = mycursor.fetchall()

                    if test1:
                        #THIS LINE OF CODE ISNT RUNNING
                        delete_query = "DELETE FROM webDB.confirmedOrders WHERE customerName = %s AND orderCompleted = TRUE"
                        mycursor.execute(delete_query, (customerName,))
                        db.commit()
                        #Delete pending order, then transfer to new page

                    if test1:
                        return redirect(url_for("orderInProgressCustomer"))

    else:
        return "You have no permission to send orders."


    return render_template('sendOrder.html', customerName=customerName, orderSentTextDisplayForHTML=orderSentTextDisplayForHTML
                           , orderSentBool=orderSentBool)

@app.route('/acceptOrder', methods=['GET', 'POST'])
def acceptOrder():

    if session.get("loggedAsRunner"):
        runnerName = session.get('username')
        currentOrders = []
        acceptOrder = None

        query = "SELECT customerName FROM webDB.orders "
        mycursor.execute(query)
        ordersArray = mycursor.fetchall()
        db.commit()  # Commit the transaction to save changes to the database

        for i in range(len(ordersArray)):
            currentOrders.append(ordersArray[i][0])

        orderSize = len(currentOrders)
        acceptedOrderCustomerName = request.form.get('acceptOrder')

        if acceptedOrderCustomerName is not None:
            query = "DELETE FROM webDB.orders WHERE customerName = %s"

            mycursor.execute(query, (acceptedOrderCustomerName,))
            db.commit()  # Commit the transaction to save changes to the database
            print(acceptedOrderCustomerName)

            insertIntoConfirmedOrders = "INSERT INTO webDB.confirmedOrders (runnerName, customerName) VALUES (%s, %s)"
            insertIntoLocation = "INSERT INTO webDB.location (runnerName, username) VALUES (%s, %s)"

            mycursor.execute(insertIntoConfirmedOrders, (runnerName, acceptedOrderCustomerName))
            mycursor.execute(insertIntoLocation, (runnerName, acceptedOrderCustomerName))

            db.commit()  # Commit the transaction to save changes to the database

            return redirect("getLocation")

        return render_template('acceptOrder.html', currentOrders=currentOrders,orderSize=orderSize)

    #This is where the runner can see all the available orders that are ready to be accepted
    else:
        return "You dont have access to this page"

@app.route('/orderInProgressRunner', methods=['GET', 'POST'])
def orderInProgressRunner():
    query = "SELECT customerName, runnerName FROM webDB.confirmedOrders where runnerName = %s "
    mycursor.execute(query, (session['username'],))
    customerName = mycursor.fetchall()
    customerNameHTML = customerName[0][0]
    runnerName = customerName[0][1]

    if request.method == 'POST':
        # Now, once runner press order finished. It's done!
        runnerArrived = request.form.get("runnerArrived")
        orderCompleted = request.form.get("orderCompleted")

        #QUERY NOT WORKING YET!


        if orderCompleted == "True":
            update_query = """
                UPDATE webDB.confirmedOrders
                SET orderCompleted = %s
                WHERE runnerName = %s
            """

            mycursor.execute(update_query, (True, runnerName,))
            db.commit()

    return render_template('orderInProgressRunner.html', runnerName=runnerName, customerName=customerNameHTML)


@app.route('/showLocation', methods=['GET', 'POST'])
def orderInProgressCustomer():
    if session.get('loggedAsCustomer'):
        customerName = session.get('username')
        runnerNameHTML = "placeholder"
        #DISABLE CUSTOMER FROM FORCING BACKBUTTON
        query = "SELECT runnerName, orderCompleted FROM webDB.confirmedOrders where customerName = %s "
        mycursor = db.cursor(buffered=True)
        mycursor.execute(query, (customerName,))
        orderData = mycursor.fetchall()

        if orderData:
            runnerNameHTML = orderData[0][0]

            if orderData[0][1] == True:

                return redirect(url_for("orderCompletedCustomer"))

        mycursor.execute("SELECT latitude, longitude FROM webDB.location WHERE username = 'john'")
        locations = mycursor.fetchall()
        return render_template('showLocation.html', locations=locations, runnerNameHTML=runnerNameHTML)

    else:
        return "You have no permission to view now..."



@app.route('/orderCompleted', methods=['GET', 'POST'])
def orderCompletedCustomer():

    customerName = "placeholder"
    runnerNameHTML = "placeholder"

    if session['orderSent'] == True:

        customerName = session.get('username')
        session.setdefault('currentRateableRunner', None)
        session["currentRateableRunner"] = False

        query = "SELECT runnerName, orderCompleted FROM webDB.confirmedOrders where customerName = %s "
        mycursor.execute(query, (customerName,))
        orderData = mycursor.fetchall()

        if orderData:

            runnerNameHTML = orderData[0][0]
        session['orderSent'] = False
        session["currentRateableRunner"] = runnerNameHTML


    #Now, do the yes or no, if yes, send customer to review him
    if request.method == 'POST' and session["currentRateableRunner"] is not None:
        yesButton = request.form.get("yesButton")
        noButton = request.form.get("noButton")

        #Now delete the row containing your confirmed order in orders. NOT confirmedOrders
        delete_query = "DELETE FROM webDB.orders WHERE customerName = %s"
        mycursor.execute(delete_query, (customerName,))
        db.commit()

        if yesButton == "True":
            return redirect(url_for("ratings"))

        if noButton == "True":
            session['currentRateableRunner'] = None
            return redirect(url_for("profile"))


    return render_template('orderCompletedCustomer.html', runnerNameHTML=runnerNameHTML)



def index():
    #Draw the website template from the folder!
    return render_template('frontpage.html')

@app.route('/accountcreatedsuccess')
def accountcreatedsuccess():

    return render_template('accountcreatedsuccess.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():

    loggedAsCustomer = session.get('loggedAsCustomer')
    loggedAsRunner = session.get('loggedAsRunner')

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
                               timeStamps=timeStamps, totalReviews=totalReviews, reviewSize=reviewSize,
                               loggedAsCustomer=loggedAsCustomer,loggedAsRunner=loggedAsRunner)

    else:
        return redirect(url_for("login"))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    loggedAsCustomer = session.get('loggedAsCustomer')
    loggedAsRunner = session.get('loggedAsRunner')

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
                               attemptedPasswordChange=attemptedPasswordChange, loggedAsRunner=loggedAsRunner,loggedAsCustomer=loggedAsCustomer)

    else:
        return redirect(url_for("settings"))

@app.route('/getLocation', methods=['POST', 'GET'])
def getLocation():
    if session.get('loggedAsRunner'):
        print("test 1 ")
        query = "SELECT customerName, runnerName FROM webDB.confirmedOrders where runnerName = %s "
        mycursor = db.cursor(buffered=True)
        mycursor.execute(query, (session['username'],))
        customerName = mycursor.fetchall()
        customerNameHTML = customerName[0][0]
        runnerName = customerName[0][1]

        #NOTE: orderCompletedButtons must be the if statement, else it will confuse as javascript variables (pardon the poor explanation!)

        if request.method == 'POST':
            # Now, once runner press order finished. It's done!
            runnerArrived = request.form.get("runnerArrived")
            orderCompleted = request.form.get('orderCompleted')
            # QUERY NOT WORKING YET!

            if orderCompleted == "True":
                update_query = """
                        UPDATE webDB.confirmedOrders
                        SET orderCompleted = %s
                        WHERE runnerName = %s
                    """
                mycursor.execute(update_query, (True, runnerName,))
                db.commit()
                return redirect('profile')
            
        # AUTO LOCATION UPDATER
        if request.method == 'POST':
            print("sent location")
            data = request.get_json()
            latitude = data['latitude']
            longitude = data['longitude']
            # Process location data as needed

            sql = "INSERT INTO webDB.location (latitude, longitude, username, runnerName) VALUES (%s, %s, %s, %s)"
            print('logged')
            mycursor.execute(sql, (latitude,longitude, customerNameHTML, runnerName,))
            db.commit()

        # GET USER INFO
        #


        return render_template('getCurrentLocation.html', runnerName=runnerName, customerName=customerNameHTML)

    else:
        return "You have no permission to view right now..."

@app.route('/showLocation', methods=['POST', 'GET'])
def showLocation():
    if session.get('loggedAsCustomer'):
        mycursor.execute("SELECT latitude, longitude FROM webDB.location WHERE username = 1")
        locations = mycursor.fetchall()
        return render_template('showLocation.html', locations=locations)

    else:
        return "You have no permission to view now..."

if __name__ == '__main__':
    app.run(debug=True)
    mycursor.close()

@app.route('/testfile')
def testfile():
    return render_template('testfile.html')



