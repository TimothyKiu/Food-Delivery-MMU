from flask import Flask,render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
class loginLogic:

    #Post means send or create, an attempt will be made to the server, if conditions are right it will return you back with a status
    def login(self,session,users,db,cursor):
        #DO NOT INITIALIZE THIS VARIABLE IN THE FUNCTION, IT WILL KEEPING ON LOOPING THE SAME VARIABLE
        #EVERYTIME A USER DOES A POST REQUEST
        #firstAttempt = True
        session.setdefault('loginAttempts', -1)
        session.setdefault('loggedIn', False)
        session.setdefault('loggedAsRunner', False)

        if session.get('loggedIn') == True:
            return redirect(url_for('profile'))


        elif request.method == 'POST':
            #Request from the html button with the name 'username'
            username = request.form['username']
            password = request.form['password']

            # Prepare the SQL query with placeholders
            query = "SELECT user_name, user_password, type FROM webDB.registeredAccounts WHERE user_name = %s"

            # Execute the SQL query with the username and password as parameters
            #This is where user enters his credentials in the HTML page
            cursor.execute(query, (username,))

            # Fetch the result (assuming only one row is expected)
            userdata = cursor.fetchone()

            if (userdata is not None) and userdata[0] == username and check_password_hash(userdata[1], password):
                #Redirect using the function name, NOT the app.route(/example)
                session['username'] = userdata[0]
                session['loggedIn'] = True

                if userdata[2] == 'Runner':
                    session['loggedAsRunner'] = True

                return redirect(url_for("profile", login_failed=False))

            else:
                # cursor = db.cursor()
                # query = "INSERT INTO clicks (click_id, username) VALUES (%s, %s)"
                # cursor.execute(query, (42069, username,))
                # db.commit()
                # cursor.close()

                return render_template('login.html',login_failed=True)
        else:
            # Check if login failed from query parameter
            login_failed = request.args.get('login_failed', False)
            #                                                     this is to convert python variable into html format variable
            return render_template('login.html',
                                   login_failed=login_failed,
                                   firstAttempt=session.get('firstAttempt'),
                                   )