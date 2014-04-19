#!bin/python
from flask import Flask
from flask import render_template, flash, redirect, request
from forms import LoginForm, SignupForm, CreateEntryForm
import MySQLdb
import time

#***************Configuration Code. Do Not Modify***************

app = Flask(__name__)
app.config.from_object('config')

if __name__ == '__main__':
   app.run(debug = True)

GlobalUserName = None


@app.route('/index',  methods = ['GET', 'POST', 'DELETE'])
def index():

    form = CreateEntryForm()
    global GlobalUserName
    tasks = []
    x = 1

    if GlobalUserName == None:
        flash("There was a minor connection issue. Please try to login again")
        return redirect('/login')

    #this try/catch populates Index
    try:
        db = MySQLdb.connect(host="mysql.server", user="FInalBoss", passwd="final1", db="FInalBoss$default")
        cur = db.cursor()
        print GlobalUserName
        cur.execute('SELECT * from tblToDo where Username ="' + GlobalUserName + '";')

        for row in cur.fetchall():
            print "Returned rows in tblToDo:"
            print row
            print row[0]
            entry = {'DatabaseID': row[0], 'id': x, 'title': row[2], 'description': row[3], 'date': row[4]}
            tasks.append(entry)
            print "task list is at:" + str(tasks)
            x+=1
    except (AttributeError, MySQLdb.OperationalError):
        print "Database Exception Error has occurred (populating Index)"
        flash("Database error")
        return redirect('/login')
    finally:
        print "Database connection has closed via Finally (populating Index)"
        db.close()

    if request.method == 'POST':
        if request.form['btnCreate'] == 'Create':
            title = form.title.data
            entry = form.entry.data

            #this try/catch Inserts a new Entry
            try:
                db = MySQLdb.connect(host="mysql.server", user="FInalBoss", passwd="final1", db="FInalBoss$default")
                cur = db.cursor()
                cur.execute('Insert Into tblToDo (Username,Title,Entry,Date) Values("' + GlobalUserName + '","' + title +'","' + entry + '","' + time.strftime("%Y/%m/%d") + '");')
                db.commit()
                print "A new entry has been inserted into database"

            except (AttributeError, MySQLdb.OperationalError):
                print "Database Exception Error has occurred (Inserting New Entry)"
                flash("Database error")
                return redirect('/index')
            finally:
                print "Database connection has closed via Finally (Inserting New Entry)"
                db.close()

        return redirect('/index')

        if request.form['btnDel'] == 'Delete':

           print "BTN Delete has been pressed"

           # NEED TO FIND CODE THAT TRIGGERS DELETE BUTTON

           '''
            #this try/catch Deletes a new Entry
            try:
                db = MySQLdb.connect(host="mysql.server", user="FInalBoss", passwd="final1", db="FInalBoss$default")
                cur = db.cursor()
                cur.execute('Delete from tblToDo where ID = ("' + DatabaseID + '");')
                db.commit()
                print "An entry has been deleted from database"

            except (AttributeError, MySQLdb.OperationalError):
                print "Database Exception Error has occurred (Deleting Entry)"
                flash("Database error")
                return redirect('/index')
            finally:
                print "Database connection has closed via Finally (Deleting Entry)"
                db.close()
            '''
        return redirect('/index')

    return render_template('index.html',
        title = 'ToDo List',
        user = GlobalUserName,
        tasks = tasks)












@app.route('/NewUser', methods = ['GET', 'POST'])
def NewUser():
    form = SignupForm()
    if form.validate_on_submit():
        #this executes if button is clicked (both Username and password are required)

        #this try/catch checks if the username is already in database.
        try:
            db = MySQLdb.connect(host="mysql.server", user="FInalBoss", passwd="final1", db="FInalBoss$default")
            cur = db.cursor()
            cur.execute('SELECT * from tblUsers where UserName ="' + form.SignupUserName.data + '";')
            for row in cur.fetchall():
                print "Returned rows in tblUsers:"
                print row
                if row:
                    #Authentication Fail
                    flash('Username is already in database. Please choose another.')
                    return redirect('/NewUser')
        except (AttributeError, MySQLdb.OperationalError):
            print "Database Exception Error has occurred (Validating username)"
            flash("Database error")
            return redirect('/NewUser')
        finally:
            print "Database connection has closed via Finally (Validating username)"
            db.close()

        #Authentication Succesful

        print "Attempting to sign up using UserName: " + form.SignupUserName.data
        print "Attempting to sign up using Password: " + form.SignupPassword.data

        #this try/catch will insert username and password to database
        try:
            db = MySQLdb.connect(host="mysql.server", user="FInalBoss", passwd="final1", db="FInalBoss$default")
            #db.autocommit(True)
            cur = db.cursor()
            cur.execute('Insert Into tblUsers Values("' + form.SignupUserName.data + '","' + form.SignupPassword.data + '");')
            db.commit()
        except (AttributeError, MySQLdb.OperationalError):
            print "Database Exception Error has occurred (Insertion query)"
            flash("Database error")
            return redirect('/NewUser')
        finally:
            print "Database connection has closed via Finally (Insertion query)"
            db.close()
        print "New User Has Succesfully Signed Up"
        return redirect('/login')


    return render_template('NewUser.html',
        title = 'Sign Up',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@app.route('/', methods = ['GET', 'POST'])
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    global GlobalUserName
    GlobalUserName = None;

    if form.validate_on_submit():
        #this executes if button is clicked (both Username and password are required)
        GlobalUserName = form.UserName.data
        #this try/catch authenticates users with password when logging in
        try:
            db = MySQLdb.connect(host="mysql.server", user="FInalBoss", passwd="final1", db="FInalBoss$default")
            cur = db.cursor()
            cur.execute('SELECT * from tblUsers where UserName ="' + form.UserName.data + '" and Password ="' + form.Password.data + '";')
            for row in cur.fetchall() :
                if row:
                    #Authentication Successful

                    print "User has succesfully logged in"
                    print "GlobalUserName has been set to : " + form.UserName.data
                    return redirect('/index')

        except (AttributeError, MySQLdb.OperationalError):
            print "Database Exception Error has occurred"
            flash("Database error")
            return redirect('/login')
        finally:
            print "Connection closed via Finally (Login)"
            db.close()

        #Authentication Fail
        flash('Incorrect username or password')
        return redirect('/login')

    return render_template('login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])


