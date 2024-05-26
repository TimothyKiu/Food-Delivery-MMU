
from flask import Flask,render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
class registerLogic:

    #̶N̶O̶T̶E̶S̶ F̶O̶R̶ T̶O̶M̶O̶R̶R̶O̶W̶, A̶D̶D̶ A̶ F̶U̶N̶C̶T̶I̶O̶N̶ W̶H̶E̶R̶E̶ I̶T̶ D̶E̶T̶E̶C̶T̶S̶ I̶F̶ A̶ D̶U̶P̶L̶I̶C̶A̶T̶E̶ U̶S̶E̶R̶N̶A̶M̶E̶ I̶S̶ D̶E̶T̶E̶C̶T̶E̶D̶ W̶I̶T̶H̶I̶N̶ T̶H̶E̶ S̶Q̶L̶ D̶B̶
    #BUG WHEN USERNAME IS RETRIEVED FROM DB, IT MESSES SOMETHING UP..
    def register(self, session, users, db, cursor):
        if request.method == 'POST':
            # Request from the html button with the name 'username'
            #BUG: when registering twice, website stops workign
            usernamereg = request.form['usernamereg']
            passwordreg = request.form['passwordreg']
            confirmpasswordreg = request.form['confirmpasswordreg']

            accountTypereg = request.form['usertype']
            print(accountTypereg)

            query = "SELECT user_name FROM webDB.registeredAccounts WHERE user_name = %s "

            # Execute the SQL query with the username and password as parameters
            # This is where user enters his credentials in the HTML page, the parameter values then are run into the
            # query, if it finds a match it returns something back, if not then it returns null
            cursor.execute(query, (usernamereg,))
            # Fetch the result (assuming only one row is expected)
            userdata = cursor.fetchone()

            # if(userdata is not None) and not(usernamereg == userdata[0]):
            if len(passwordreg) >= 6 and (passwordreg == confirmpasswordreg) and ((userdata is None)):
                # No user with this username exists, proceed with registration
                cursor = db.cursor()
                insert_query = "INSERT INTO webDB.registeredAccounts (user_name, user_password, type) VALUES (%s, %s, %s)"
                hashedPassword = generate_password_hash(passwordreg)

                cursor.execute(insert_query, (usernamereg, hashedPassword, accountTypereg))
                db.commit()  # Commit the transaction to save changes to the database
                cursor.close()

                #Idk where to put this, because the user cannot use the back button to reset the ordersent default value
                session.setdefault('orderSent', False)

                return redirect(url_for("accountcreatedsuccess"))

            else:
                #BUG FOUND! ONLY ONE RETURN STATEMENT CAN BE RETURNED!!!!
                if (len(passwordreg) < 6 or len(passwordreg) > 10) and (not (passwordreg == confirmpasswordreg)) and (userdata is not None and userdata[0] == usernamereg):
                    print('All three')
                    return render_template('register.html', allfalse=True)

                #All combinations of password/username errors, I have to do this individually because only one return statement is allowed

                elif(len(passwordreg) < 6 or len(passwordreg) > 10) and (not (passwordreg == confirmpasswordreg)):
                    return render_template('register.html', passnotproperlength=True, passnotsame=True)
                elif(not (passwordreg == confirmpasswordreg)) and (userdata is not None and userdata[0] == usernamereg):
                    return render_template('register.html', passnotsame=True, nametaken=True)
                elif((len(passwordreg) < 6 or len(passwordreg) > 10) and (userdata is not None and userdata[0] == usernamereg)):
                    return render_template('register.html', passnotproperlength=True, nametaken=True)
                elif(userdata is not None and userdata[0] == usernamereg):
                    return render_template('register.html',nametaken=True)

                #BUG: BOTH CONDITIONS CANT RUN AT THE SAME TIME
                elif len(passwordreg) < 6 or len(passwordreg) > 10:
                    # session['passproperlength'] = False
                    print("Password not proper length")
                    #RUNS FINE!
                    return render_template('register.html', passnotproperlength=True)

                elif(not(passwordreg == confirmpasswordreg)):
                    # session['passSameWithConfirm'] = False
                    print("Password not same")
                    return render_template('register.html', passnotsame=True)


        passnotproperlength = request.args.get('passnotproperlength', False)
        passnotsame = request.args.get('passnotsame', False)
        allfalse = request.args.get('allfalse', False)
        nametaken = request.args.get('nametaken', False)
        # passSameWithConfirm = session.get('passSameWithConfirm')
        # DO NOT STORE THESE AS SESSION VARIABLES, SINCE ITS MERELY COSMETIC
        return render_template('register.html',
                               passproperlength=passnotproperlength,
                               passnotsame=passnotsame,
                               allfalse=allfalse,
                               nametaken=nametaken)
                               # passSameWithConfirm=passSameWithConfirm)



        # else:
        #     passproperlength = request.args.get('passproperlength', True)
        #     passSameWithConfirm = request.args.get('passSameWithConfirm', True)
        #     #                                                     this is to convert python variable into html format variable
        #     return render_template('register.html',
        #                        passproperlength=passproperlength,
        #                        passSameWithConfirm=passSameWithConfirm
        #                        )
