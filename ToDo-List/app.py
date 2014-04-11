#!bin/python
from flask import Flask
from flask import render_template, flash, redirect, request
from forms import LoginForm, SignupForm, CreateEntryForm
import MySQLdb

#***************Configuration Code. Do Not Modify***************

app = Flask(__name__)
app.config.from_object('config')

if __name__ == '__main__':
   app.run(debug = True)


##################################################


@app.route('/index',  methods = ['GET', 'POST', 'DELETE'])
def index():

    user = { 'nickname': 'User' }

    tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    },
          {
      'id': 3,
      'title': u'Finish Project',
      'description': u'Need to find finish project for Networking classs',
      'done': False
   },
   {
      'id': 4,
      'title': u'Finish Project',
      'description': u'Need to find finish project for Networking classs',
      'done': False}]


    #Need to find code that triggers an event from the Create button######

    #if request.method == 'POST':


    form = CreateEntryForm()
    if request.method == 'POST':
        if request.form['btnCreate'] == 'Create':
            title = form.title.data
            entry = form.entry.data
            flash('Create Entry requested for Title= "' + title + 'Entry = "' + entry)
        return redirect('/index')

    return render_template('index.html',
        title = 'ToDo List',
        user = user,
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
            print "Database connection has closed via Exception (Validating username)"
            db.close()
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
            print "Database connection has closed via Exception (Insertion query)"
            db.close()
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

    if form.validate_on_submit():
        #this executes if button is clicked (both Username and password are required)

        #this try/catch authenticates users with password when logging in
        try:
            db = MySQLdb.connect(host="mysql.server", user="FInalBoss", passwd="final1", db="FInalBoss$default")
            cur = db.cursor()
            cur.execute('SELECT * from tblUsers where UserName ="' + form.UserName.data + '" and Password ="' + form.Password.data + '";')
            for row in cur.fetchall() :
                if row:
                    #Authentication Successful
                    flash('Login requested for UserName="' + form.UserName.data + '" Password="' + form.Password.data + '", remember_me=' + str(form.remember_me.data))
                    print "User has succesfully logged in"
                    return redirect('/index')

        except (AttributeError, MySQLdb.OperationalError):
            print "Database connection has closed via Exception (Login)"
            db.close()
        finally:
            print "Connection closed via Finally (Login)"
            db.close()

        #Authentication Fail
        flash('Login failed')
        return redirect('/login')

    return render_template('login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])


