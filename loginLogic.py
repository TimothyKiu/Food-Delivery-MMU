from flask import Flask,render_template, request, redirect, url_for


class loginLogic:

    #Post means send or create, an attempt will be made to the server, if conditions are right it will return you back with a status
    def login(self,session,users,db):
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
                #Redirect using the function name, NOT the app.route(/example)
                return redirect(url_for("successlogin", login_failed=False))

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