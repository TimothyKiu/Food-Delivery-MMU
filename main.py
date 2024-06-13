from urllib import request
from flask import Flask,render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
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

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='webDB',
            user='root',
            password='0000'
        )
        return connection
    except Exception as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return None


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
    connection = get_db_connection()
    mycursor = connection.cursor(buffered=True)
    loginlogic1 = loginLogic()
    return loginlogic1.login(session, users, db, mycursor)

@app.route('/register', methods=['GET', 'POST'])
def register():
    connection = get_db_connection()
    mycursor = connection.cursor(buffered=True)
    registerlogic = registerLogic()
    return registerlogic.register(session, users, db, mycursor)


@app.route('/otherratings', methods=['GET', 'POST'])
def otherratings():
    loggedAsCustomer = None
    loggedAsRunner = None
    connection = get_db_connection()
    mycursor = connection.cursor(buffered=True)
    query = "SELECT type FROM webDB.registeredAccounts WHERE user_name = %s"

    # Execute the SQL query with the username and password as parameters
    # This is where user enters his credentials in the HTML page
    mycursor.execute(query, (session.get('username'),))

    # Fetch the result (assuming only one row is expected)
    userdata = mycursor.fetchall()
    mycursor.close()
    connection.close()

    print(userdata[0][0])
    print('type')

    if userdata[0][0] == "Runner":
        loggedAsRunner = True
    elif userdata[0][0] == "Customer":
        loggedAsCustomer = True
    else:
        loggedAsCustomer = None
        loggedAsRunner = None

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

            mycursor = db.cursor(buffered=True)
            getInfo = "SELECT nickname, phone_number, user_name FROM webDB.registeredAccounts WHERE user_name = %s"
            mycursor.execute(getInfo, (usernameP,))
            infoArray = mycursor.fetchall()
            mycursor.close()

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
            mycursor = db.cursor(buffered=True)
            query = "SELECT average_rating FROM webDB.average_reviews WHERE username = %s "
            mycursor.execute(query, (username,))
            ratingsArray = mycursor.fetchall()
            mycursor.close()


            if ratingsArray:  # Check if ratingsArray is not empty
                ratings = round(float(ratingsArray[0][0]), 2)
            else:
                ratings = "N/A"

            # Execute the SQL query with the username and password as parameters
            # This is where user enters his credentials in the HTML page, the parameter values then are run into the
            # query, if it finds a match it returns something back, if not then it returns null

            mycursor = db.cursor(buffered=True)
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

            mycursor.close()

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

            connection = get_db_connection()
            mycursor = connection.cursor(buffered=True)
            insert_query = "INSERT INTO webDB.reviews (user_name, review_text, rating_given) VALUES (%s, %s, %s)"
            mycursor.execute(insert_query, (currentRateableRunner, review, ratings,))
              # Commit the transaction to save changes to the database

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
            connection.commit()
            mycursor.close()
            connection.close()

            session['currentRateableRunner'] = None
            return redirect(url_for("profile"))

    else:
        return "You don't have access to rate anyone..."

    #Draw the website template from the folder!
    return render_template('ratings.html', currentRateableRunner=currentRateableRunner, customerName=customerName)

@app.route('/ratingsent', methods=['GET', 'POST'])
def ratingsent():
    return render_template('ratingsent.html')

@app.route('/sendOrder', methods=['GET', 'POST'])
def sendOrder():
    print(session.get('loggedAsCustomer'))

    loggedAsCustomer = None
    loggedAsRunner = None
    connection = get_db_connection()
    mycursor = connection.cursor(buffered=True)
    query = "SELECT type FROM webDB.registeredAccounts WHERE user_name = %s"

    # Execute the SQL query with the username and password as parameters
    # This is where user enters his credentials in the HTML page
    mycursor.execute(query, (session.get('username'),))

    # Fetch the result (assuming only one row is expected)
    userdata = mycursor.fetchall()
    mycursor.close()
    connection.close()

    print(userdata[0][0])
    print('type')

    if userdata[0][0] == "Runner":
        loggedAsRunner = True
    elif userdata[0][0] == "Customer":
        loggedAsCustomer = True
    else:
        loggedAsCustomer = None
        loggedAsRunner = None

    #BUG DETECTED, session['orderSent'] is being turned into true by something...
    if loggedAsCustomer == True:
        mycursor = db.cursor(buffered=True)
        findIfOrderAccepted = "SELECT runnerName, customerName FROM webDB.Orders WHERE customerName = %s "
        mycursor.execute(findIfOrderAccepted, (session.get('username'),))
        test1 = mycursor.fetchall()
        mycursor.close()
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

            #THE IF ISNT RUNNING
            if request.form['sendOrder'] == "True":
                if session.get('orderSent') == False:
                    orderList = request.form['orderList']
                    restaurant = request.form['restaurant']
                    customerLocation = request.form['customerLocation']

                    orderSentTextDisplayForHTML = True
                    connection = get_db_connection()
                    mycursor = connection.cursor(buffered=True)

                    insert_query = "INSERT INTO webDB.orders (customerName, FoodOrdered, restaurant, customerLocation) VALUES (%s, %s, %s, %s)"
                    mycursor.execute(insert_query, (customerName, orderList, restaurant, customerLocation,))
                    connection.commit()  # Commit the transaction to save changes to the database
                    mycursor.close()
                    connection.close()
                    session['orderSent'] = True

                if session.get('orderSent') == True:


                    #FIND IF ORDER ACCEPTED
                    mycursor = db.cursor(buffered=True)

                    findIfOrderAccepted = "SELECT runnerName, customerName FROM webDB.confirmedOrders WHERE customerName = %s "
                    mycursor.execute(findIfOrderAccepted, (customerName,))
                    test1 = mycursor.fetchall()
                    sentValue = mycursor.fetchall()
                    mycursor.close()

                    if test1:
                        #THIS LINE OF CODE ISNT RUNNING
                        mycursor = db.cursor(buffered=True)
                        delete_query = "DELETE FROM webDB.confirmedOrders WHERE customerName = %s AND orderCompleted = TRUE"
                        mycursor.execute(delete_query, (customerName,))
                        db.commit()
                        mycursor.close()
                        #Delete pending order, then transfer to new page

                    if test1:
                        return redirect(url_for("orderInProgressCustomer"))

    else:
        return "You have no permission to send orders."


    return render_template('sendOrder.html', customerName=customerName, orderSentTextDisplayForHTML=orderSentTextDisplayForHTML
                           , orderSentBool=orderSentBool)

@app.route('/acceptOrder', methods=['GET', 'POST'])
def acceptOrder():
    print(session.get('loggedAsCustomer'))

    loggedAsCustomer = None
    loggedAsRunner = None
    connection = get_db_connection()
    mycursor = connection.cursor(buffered=True)
    query = "SELECT type FROM webDB.registeredAccounts WHERE user_name = %s"

    # Execute the SQL query with the username and password as parameters
    # This is where user enters his credentials in the HTML page
    mycursor.execute(query, (session.get('username'),))

    # Fetch the result (assuming only one row is expected)
    userdata = mycursor.fetchall()
    mycursor.close()
    connection.close()

    if userdata[0][0] == "Runner":
        loggedAsRunner = True
    elif userdata[0][0] == "Customer":
        loggedAsCustomer = True
    else:
        loggedAsCustomer = None
        loggedAsRunner = None

    if loggedAsRunner == True:
        runnerName = session.get('username')
        currentOrders = []
        acceptOrder = None
        customerLocation = "placeholder"
        session['orderList'] = None
        session['restaurant'] = None

        mycursor = db.cursor(buffered=True)
        query = "SELECT customerName FROM webDB.orders "
        mycursor.execute(query)
        ordersArray = mycursor.fetchall()
        db.commit()  # Commit the transaction to save changes to the database
        mycursor.close()

        for i in range(len(ordersArray)):
            currentOrders.append(ordersArray[i][0])

        orderSize = len(currentOrders)
        acceptedOrderCustomerName = request.form.get('acceptOrder')

        if acceptedOrderCustomerName is not None:

            #look for order infprmation
            mycursor = db.cursor(buffered=True)
            query2 = "SELECT restaurant,FoodOrdered,customerLocation FROM webDB.orders WHERE customerName = %s"
            mycursor.execute(query2, (acceptedOrderCustomerName,))
            orderInfo = mycursor.fetchall()
            mycursor.close()
            if orderInfo:
                session['restaurant'] = orderInfo[0][0]
                session['orderList'] = orderInfo[0][1]
                customerLocation = orderInfo[0][2]



            mycursor = db.cursor(buffered=True)
            insertIntoConfirmedOrders = "INSERT INTO webDB.confirmedOrders (runnerName, customerName, orderList, restaurant, customerLocation) VALUES (%s, %s, %s,%s, %s)"
            insertIntoLocation = "INSERT INTO webDB.location (latitude, longitude, runnerName, username) VALUES (%s, %s, %s, %s)"

            mycursor.execute(insertIntoConfirmedOrders, (runnerName, acceptedOrderCustomerName, session.get('orderList'), session.get('restaurant'), customerLocation,))
            mycursor.execute(insertIntoLocation, (0,0,runnerName, acceptedOrderCustomerName,))

            db.commit()  # Commit the transaction to save changes to the database
            mycursor.close()

            mycursor = db.cursor(buffered=True)


            query = "DELETE FROM webDB.orders WHERE customerName = %s"

            mycursor.execute(query, (acceptedOrderCustomerName,))
            db.commit()  # Commit the transaction to save changes to the database
            mycursor.close()
            print(acceptedOrderCustomerName)

            return redirect("getLocation")

        return render_template('acceptOrder.html', currentOrders=currentOrders,orderSize=orderSize)

    #This is where the runner can see all the available orders that are ready to be accepted
    else:
        return "You dont have access to this page"

# @app.route('/orderInProgressRunner', methods=['GET', 'POST'])
# def orderInProgressRunner():
#     query = "SELECT customerName, runnerName, orderList,restaurant FROM webDB.confirmedOrders where runnerName = %s "
#
#     mycursor.execute(query, (session['username'],))
#     customerName = mycursor.fetchall()
#     customerNameHTML = customerName[0][0]
#     runnerName = customerName[0][1]
#     orderList = customerName[0][2]
#     restaurant = customerName[0][3]
#
#     print(customerNameHTML)
#     print(orderList)
#     print(restaurant)
#
#     if request.method == 'POST':
#         # Now, once runner press order finished. It's done!
#         runnerArrived = request.form.get("runnerArrived")
#         orderCompleted = request.form.get("orderCompleted")
#
#         #QUERY NOT WORKING YET!
#
#
#         if orderCompleted == "True":
#             update_query = """
#                 UPDATE webDB.confirmedOrders
#                 SET orderCompleted = %s
#                 WHERE runnerName = %s
#             """
#
#             mycursor.execute(update_query, (True, runnerName,))
#             db.commit()
#
#     return render_template('orderInProgressRunner.html', runnerName=runnerName,
#                            customerName=customerNameHTML, orderList=orderList, restaurant=restaurant)


@app.route('/showLocation', methods=['GET', 'POST'])
def orderInProgressCustomer():

    loggedAsCustomer = None
    loggedAsRunner = None
    connection = get_db_connection()
    mycursor = connection.cursor(buffered=True)
    query = "SELECT type FROM webDB.registeredAccounts WHERE user_name = %s"

    # Execute the SQL query with the username and password as parameters
    # This is where user enters his credentials in the HTML page
    mycursor.execute(query, (session.get('username'),))

    # Fetch the result (assuming only one row is expected)
    userdata = mycursor.fetchall()
    mycursor.close()
    connection.close()

    if userdata[0][0] == "Runner":
        loggedAsRunner = True
    elif userdata[0][0] == "Customer":
        loggedAsCustomer = True
    else:
        loggedAsCustomer = None
        loggedAsRunner = None


    if loggedAsCustomer == True:
        customerName = session.get('username')
        runnerNameHTML = "placeholder"
        restaurant = "placeholder"
        orderList = "placeholder"
        orderReceived = session.get('orderReceived')
        customerLocation = "placeholder"

        connection = get_db_connection()
        mycursor = connection.cursor(buffered=True)
        #DISABLE CUSTOMER FROM FORCING BACKBUTTON

        query = "SELECT runnerName, orderCompleted, restaurant,orderList, customerLocation FROM webDB.confirmedOrders where customerName = %s "
        mycursor.execute(query, (customerName,))
        orderData = mycursor.fetchall()

        if orderData:
            runnerNameHTML = orderData[0][0]
            restaurant = orderData[0][2]
            orderList = orderData[0][3]
            customerLocation = orderData[0][4]

        if orderData:
            print('orderData is not null')
            print(orderData[0][1])

            if orderData[0][1] == 1:
                session['orderReceived'] = True
                connection = get_db_connection()
                mycursor = connection.cursor(buffered=True)
                delete_query2 = "DELETE FROM webDB.confirmedorders WHERE customerName = %s"
                mycursor.execute(delete_query2, (customerName,))
                mycursor.close()
                connection.close()
                return redirect(url_for("orderCompletedCustomer"))
        mycursor.close()

        connection = get_db_connection()
        mycursor = connection.cursor(buffered=True)
        mycursor.execute("SELECT latitude, longitude FROM webDB.location WHERE runnerName = %s", (runnerNameHTML,))
        locations = mycursor.fetchall()
        mycursor.close()
        print(locations)
        return render_template('showLocation.html', locations=locations
                               ,orderReceived=orderReceived,runnerNameHTML=runnerNameHTML
                               , customerName=customerName, restaurant=restaurant,
                               orderList=orderList, customerLocation=customerLocation)

    else:
        return "You have no permission to view now..."



@app.route('/orderCompleted', methods=['GET', 'POST'])
def orderCompletedCustomer():
    session['orderReceived'] = False

    customerName = "placeholder"
    runnerNameHTML = "placeholder"

    if session['orderSent'] == True:

        customerName = session.get('username')
        session.setdefault('currentRateableRunner', None)


        mycursor = db.cursor(buffered=True)
        query = "SELECT runnerName, orderCompleted FROM webDB.confirmedOrders where customerName = %s "
        mycursor.execute(query, (customerName,))
        orderData = mycursor.fetchall()
        mycursor.close()

        if orderData:

            runnerNameHTML = orderData[0][0]
            session['orderSent'] = False
            session["currentRateableRunner"] = runnerNameHTML

        session['orderSent'] = False



    #Now, do the yes or no, if yes, send customer to review him
    if request.method == 'POST' and session["currentRateableRunner"] is not None:
        yesButton = request.form.get("yesButton")
        noButton = request.form.get("noButton")

        #Now delete the row containing your confirmed order in orders. NOT confirmedOrder
        # s
        mycursor = db.cursor(buffered=True)
        delete_query = "DELETE FROM webDB.orders WHERE customerName = %s"
        mycursor.execute(delete_query, (customerName,))
        db.commit()
        mycursor.close()

        if yesButton == "True":
            session['orderSent'] = False

            return redirect(url_for("ratings"))

        if noButton == "True":
            session['orderSent'] = False

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
    loggedAsCustomer = None
    loggedAsRunner = None
    connection = get_db_connection()
    mycursor = connection.cursor(buffered=True)
    query = "SELECT type FROM webDB.registeredAccounts WHERE user_name = %s"

    # Execute the SQL query with the username and password as parameters
    # This is where user enters his credentials in the HTML page
    mycursor.execute(query, (session.get('username'),))

    # Fetch the result (assuming only one row is expected)
    userdata = mycursor.fetchall()
    mycursor.close()
    connection.close()

    print('type')

    if userdata:
        if userdata[0][0] == "Runner":
            loggedAsRunner = True
        elif userdata[0][0] == "Customer":
            loggedAsCustomer = True
        else:
            loggedAsCustomer = None
            loggedAsRunner = None

    print(session.get('loggedIn'))

    if session.get('loggedIn') == True:
        usernameP = session.get('username')
        loggedIn = session.get('loggedIn')

        errorText = "placeholder"

        connection = get_db_connection()
        mycursor = connection.cursor(buffered=True)
        query = "SELECT average_rating FROM webDB.average_reviews WHERE username = %s "
        mycursor.execute(query, (usernameP,))
        ratingsArray = mycursor.fetchall()
        mycursor.close()
        connection.close()


        if ratingsArray:  # Check if ratingsArray is not empty
            ratings = round(float(ratingsArray[0][0]), 2)
        else:
            ratings = "N/A"

        # Execute the SQL query with the username and password as parameters
        # This is where user enters his credentials in the HTML page, the parameter values then are run into the
        # query, if it finds a match it returns something back, if not then it returns null

        connection = get_db_connection()
        mycursor = connection.cursor(buffered=True)
        query2 = "SELECT review_text, rating_given, timestamp FROM webDB.reviews WHERE user_name = %s"
        mycursor.execute(query2, (usernameP,))
        reviewsArray = mycursor.fetchall()
        mycursor.close()

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
                mycursor = db.cursor(buffered=True)
                deleteQuery = "DELETE FROM webDB.registeredAccounts WHERE user_name = %s"
                mycursor.execute(deleteQuery, (session['username'],))
                db.commit()
                mycursor.close()

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
    loggedAsCustomer = None
    loggedAsRunner = None
    connection = get_db_connection()
    mycursor = connection.cursor(buffered=True)
    query = "SELECT type FROM webDB.registeredAccounts WHERE user_name = %s"

    # Execute the SQL query with the username and password as parameters
    # This is where user enters his credentials in the HTML page
    mycursor.execute(query, (session.get('username'),))

    # Fetch the result (assuming only one row is expected)
    userdata = mycursor.fetchall()
    mycursor.close()
    connection.close()

    print(userdata[0][0])
    print('type')

    if userdata[0][0] == "Runner":
        loggedAsRunner = True
    elif userdata[0][0] == "Customer":
        loggedAsCustomer = True
    else:
        loggedAsCustomer = None
        loggedAsRunner = None

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
        mycursor = db.cursor(buffered=True)
        query = "SELECT phone_number, nickname FROM webDB.registeredAccounts WHERE user_name = %s "
        mycursor.execute(query, (usernameP,))
        test1 = mycursor.fetchone()
        mycursor.close()
        if test1 is not None:
            phoneNumber = test1[0]
            nickname = test1[1]

        mycursor = db.cursor(buffered=True)
        query = "SELECT average_rating FROM webDB.average_reviews WHERE username = %s "
        mycursor.execute(query, (usernameP,))
        ratingsArray = mycursor.fetchall()
        mycursor.close()

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
                mycursor = db.cursor(buffered=True)
                deleteQuery = "DELETE FROM webDB.registeredAccounts WHERE user_name = %s"
                mycursor.execute(deleteQuery, (session['username'],))
                db.commit()
                mycursor.close()


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


                mycursor = db.cursor(buffered=True)
                getpassword = "SELECT user_password from webDb.registeredAccounts WHERE user_name = %s "
                mycursor.execute(getpassword, (session['username'],))
                db.commit()
                userdata = mycursor.fetchone()
                mycursor.close()


                if(newpassword == confirmnewpassword) and check_password_hash(userdata[0], oldpassword) :
                    mycursor = db.cursor(buffered=True)
                    alter_query = "UPDATE webDB.registeredAccounts SET user_password = %s WHERE user_name = %s"

                    hashedNewPassword = generate_password_hash(newpassword)
                    mycursor.execute(alter_query, (hashedNewPassword, usernameP))
                    db.commit()
                    mycursor.close()
                    passwordNotSame = False
                    attemptedPasswordChange = True

                else:
                    print("Passwords do not match")
                    passwordNotSame = True
                    attemptedPasswordChange = True

            if changedNickname == "True":
                newNickname = request.form['newNickname']
                mycursor = db.cursor(buffered=True)
                setNickname = "UPDATE webDb.registeredAccounts SET nickname = %s WHERE user_name = %s"

                mycursor.execute(setNickname, (newNickname, session['username']))
                db.commit()
                mycursor.close()

            if changedPhoneNumber == "True":
                newPhoneNumber = request.form['newPhoneNumber']
                mycursor = db.cursor(buffered=True)
                setNickname = "UPDATE webDb.registeredAccounts SET phone_number = %s WHERE user_name = %s"
                mycursor.execute(setNickname, (newPhoneNumber, session['username']))
                db.commit()
                mycursor.close()
        return render_template('settings.html', usernameP=usernameP, loggedIn=loggedIn, errorText=errorText,
                               ratings=ratings, changepasssworderror=changepasssworderror, nickname=nickname,
                               phoneNumber=phoneNumber, passwordNotSame=passwordNotSame,
                               attemptedPasswordChange=attemptedPasswordChange, loggedAsRunner=loggedAsRunner,loggedAsCustomer=loggedAsCustomer)

    else:
        return redirect(url_for("settings"))

@app.route('/getLocation', methods=['POST', 'GET'])
def getLocation():


    loggedAsCustomer = None
    loggedAsRunner = None
    connection = get_db_connection()
    mycursor = connection.cursor(buffered=True)
    query = "SELECT type FROM webDB.registeredAccounts WHERE user_name = %s"

    # Execute the SQL query with the username and password as parameters
    # This is where user enters his credentials in the HTML page
    mycursor.execute(query, (session.get('username'),))

    # Fetch the result (assuming only one row is expected)
    userdata = mycursor.fetchall()
    mycursor.close()
    connection.close()

    if userdata[0][0] == "Runner":
        loggedAsRunner = True
    elif userdata[0][0] == "Customer":
        loggedAsCustomer = True
    else:
        loggedAsCustomer = None
        loggedAsRunner = None

    if loggedAsRunner == True:
        customerNameHTML = None
        orderList = None
        restaurant = None
        runnerName = session.get('username')
        customerLocation = "placeholder"

        connection = get_db_connection()
        if connection is None:
            return "Database connection failed", 500

        try:
            mycursor = connection.cursor(buffered=True)
            query = "SELECT customerName, runnerName, orderList, restaurant, customerLocation FROM webDB.confirmedOrders WHERE runnerName = %s"
            mycursor.execute(query, (runnerName,))
            customerName = mycursor.fetchall()
            mycursor.close()
            connection.close()

            if customerName:
                customerNameHTML = customerName[0][0]
                orderList = customerName[0][2]
                restaurant =customerName[0][3]
                customerLocation = customerName[0][4]
            else:
                return "No orders found for runner", 404

        except Exception as e:
            print(f"Error reading data from MySQL table: {e}")
            if connection.is_connected():
                mycursor.close()
                connection.close()
            return "Database query failed", 500

        if request.method == 'POST':
            runnerArrived = request.form.get("runnerArrived")
            orderCompleted = request.form.get('orderCompleted')

            if orderCompleted == "True":
                connection = get_db_connection()
                if connection is None:
                    return "Database connection failed", 500

                try:
                    mycursor = connection.cursor(buffered=True)
                    update_query = "UPDATE webDB.confirmedOrders SET orderCompleted = %s WHERE runnerName = %s"
                    delete_query = "DELETE FROM webDB.location WHERE runnerName = %s"
                    mycursor.execute(update_query, (1, runnerName,))
                    mycursor.execute(delete_query, (runnerName,))
                    connection.commit()
                    mycursor.close()
                    connection.close()

                    session['orderList'] = None
                    session['restaurant'] = None

                    return redirect('profile')

                except Exception as e:
                    print(f"Error updating data in MySQL table: {e}")
                    if connection.is_connected():
                        mycursor.close()
                        connection.close()
                    return "Database update failed", 500

        if request.method == 'POST':
            data = request.get_json()
            latitude = data['latitude']
            longitude = data['longitude']

            connection = get_db_connection()
            if connection is None:
                return "Database connection failed", 500

            try:
                mycursor = connection.cursor(buffered=True)
                sql = "UPDATE webDB.location SET latitude = %s, longitude = %s, last_updated_at = %s WHERE runnerName = %s"
                last_updated_at = datetime.now()
                print('updated!')
                # Execute the query
                mycursor.execute(sql, (latitude, longitude, last_updated_at, runnerName))
                connection.commit()
                mycursor.close()
                connection.close()

            except Exception as e:
                print(f"Error updating data in MySQL table: {e}")
                if connection.is_connected():
                    mycursor.close()
                    connection.close()
                return "Database update failed", 500

        return render_template('getCurrentLocation.html', customerLocation=customerLocation, runnerName=runnerName, customerName=customerNameHTML, orderList=orderList, restaurant=restaurant)

    else:
        return "You have no permission to view right now..."
# @app.route('/showLocation', methods=['POST', 'GET'])
# def showLocation():
#     if session.get('loggedAsCustomer'):
#         mycursor = db.cursor(buffered=True)
#         mycursor.execute("SELECT latitude, longitude FROM webDB.location WHERE username = 1")
#         locations = mycursor.fetchall()
#         mycursor.close()
#
#         return render_template('showLocation.html', locations=locations)
#
#     else:
#         return "You have no permission to view now..."



@app.route('/testfile',  methods=['GET', 'POST'])
def testfile():

    if session.get("loggedAsRunner"):
        runnerName = session.get('username')
        currentOrders = []
        acceptOrder = None
        session['orderList'] = None
        session['restaurant'] = None

        mycursor = db.cursor(buffered=True)
        query = "SELECT customerName FROM webDB.orders "
        mycursor.execute(query)
        ordersArray = mycursor.fetchall()
        db.commit()  # Commit the transaction to save changes to the database
        mycursor.close()

        for i in range(len(ordersArray)):
            currentOrders.append(ordersArray[i][0])

        orderSize = len(currentOrders)
        acceptedOrderCustomerName = request.form.get('acceptOrder')

        if acceptedOrderCustomerName is not None:

            #look for order infprmation
            mycursor = db.cursor(buffered=True)
            query2 = "SELECT restaurant,FoodOrdered,customerLocation FROM webDB.orders WHERE customerName = %s"
            mycursor.execute(query2, (acceptedOrderCustomerName,))
            orderInfo = mycursor.fetchall()
            mycursor.close()
            if orderInfo:
                session['restaurant'] = orderInfo[0][0]
                session['orderList'] = orderInfo[0][1]
                customerLocation = orderInfo[0][2]



            mycursor = db.cursor(buffered=True)
            insertIntoConfirmedOrders = "INSERT INTO webDB.confirmedOrders (runnerName, customerName, orderList, restaurant, customerLocation) VALUES (%s, %s, %s,%s, %s)"
            insertIntoLocation = "INSERT INTO webDB.location (latitude, longitude, runnerName, username) VALUES (%s, %s, %s, %s)"

            mycursor.execute(insertIntoConfirmedOrders, (runnerName, acceptedOrderCustomerName, session.get('orderList'), session.get('restaurant'),customerLocation))
            mycursor.execute(insertIntoLocation, (0,0,runnerName, acceptedOrderCustomerName,))

            db.commit()  # Commit the transaction to save changes to the database
            mycursor.close()

            mycursor = db.cursor(buffered=True)


            query = "DELETE FROM webDB.orders WHERE customerName = %s"

            mycursor.execute(query, (acceptedOrderCustomerName,))
            db.commit()  # Commit the transaction to save changes to the database
            mycursor.close()
            print(acceptedOrderCustomerName)

            return redirect("getLocation")

        return render_template('testfile.html', currentOrders=currentOrders,orderSize=orderSize)

    #This is where the runner can see all the available orders that are ready to be accepted
    else:
        return "You dont have access to this page"




if __name__ == '__main__':
    app.run(debug=True)