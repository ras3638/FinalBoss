#!bin/python
from flask import Flask, session
from flask import render_template, flash, redirect
from forms import LoginForm, SignupForm, CreateEntryForm, DeleteEntryForm
import MySQLdb
import time


#***************Configuration Code. Do Not Modify***************

app = Flask(__name__)
app.config.from_object('config')

if __name__ == '__main__':
   app.run(debug = True)




@app.route('/index',  methods = ['GET', 'POST', 'DELETE'])
def index():

    form_cr = CreateEntryForm()
    form_del = DeleteEntryForm()
    tasks = []
    x = 1

    #logout if haven't signed in
    if 'username' not in session:
        flash("You are not logged in. Please try to login again")
        return redirect('/login')


    #this try/catch populates Index
    try:
        db = MySQLdb.connect(host="mysql.server", user="FInalBoss", passwd="final1", db="FInalBoss$default")
        cur = db.cursor()

        cur.execute('SELECT * from tblToDo where Username ="' + session['username'] + '";')

        for row in cur.fetchall():
            print "Returned rows in tblToDo:"
            #print row
            #print row[0]
            #entry = {'DatabaseID': row[0], 'id': x, 'title': row[2], 'description': row[3], 'date': row[4]}
            entry = {'HTMLid': x, 'Dbid': row[0], 'title': row[2], 'description': row[3], 'date': row[4]}
            tasks.append(entry)

            #print "task list is at:" + str(tasks)
            x+=1
        #for i in tasks:
            #print "HTML/DB Subset_Dictionary"
            #print {y: i[y] for y in ('HTMLid', 'Dbid')}
    except (AttributeError, MySQLdb.OperationalError):
        print "Database Exception Error has occurred (populating Index)"
        flash("Database error")
        return redirect('/login')
    finally:
        print "Database connection has closed via Finally (populating Index)"
        db.close()




    if form_del.validate_on_submit():
        #this try/catch Deletes a new Entry
        HTMLid = form_del.delete.data
        counter = 0
        for i in tasks:

            if int(HTMLid) == i['HTMLid']:
                counter =1
                break;
        if counter == 0:
            flash("ID NOT FOUND")
            redirect('/index')

        for i in tasks:
             if int(HTMLid) == i['HTMLid']:
                 IDSWAP = i['Dbid']
                 print "FOUND A MATCH"
                 print IDSWAP
                 break


        try:
            db = MySQLdb.connect(host="mysql.server", user="FInalBoss", passwd="final1", db="FInalBoss$default")
            cur = db.cursor()
            print "DELETE STATEMENT"
            print type(IDSWAP)
            u = str(IDSWAP)
            print type(u)
            uni = unicode(u,"utf-8")
            print type(uni)
            cur.execute('Delete from tblToDo where ID = ("' + uni + '");')
            db.commit()
            print "An entry has been deleted from database"

        except (AttributeError, MySQLdb.OperationalError):
            print "Database Exception Error has occurred (Deleting Entry)"
            flash("Database error")
        finally:
            print "Database connection has closed via Finally (Deleting Entry)"
            db.close()
            return redirect('/index')

    if form_cr.validate_on_submit():
        title = form_cr.title.data
        entry = form_cr.entry.data

        if title == '':
            flash("Both title and description are required")
            return redirect('/index')
        elif entry == '':
            flash("Both title and description are required")
            return redirect('/index')

        #this try/catch Inserts a new Entry
        try:
            db = MySQLdb.connect(host="mysql.server", user="FInalBoss", passwd="final1", db="FInalBoss$default")
            cur = db.cursor()
            cur.execute('Insert Into tblToDo (Username,Title,Entry,Date) Values("' + session['username'] + '","' + title +'","' + entry + '","' + time.strftime("%Y/%m/%d") + '");')
            db.commit()
            print "A new entry has been inserted into database"

        except (AttributeError, MySQLdb.OperationalError):
            print "Database Exception Error has occurred (Inserting New Entry)"
            flash("Database error")

        finally:
            print "Database connection has closed via Finally (Inserting New Entry)"
            db.close()
            return redirect('/index')





    return render_template('index.html',
        title = 'ToDo List',
        user = session['username'],
        form_del = form_del,
        form_cr = form_cr,
        tasks=tasks)












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

    #Log out
    session.pop('username', None)

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
                    session['username'] = form.UserName.data
                    print "User has succesfully logged in"
                    print "Session Username has been set to : " + session['username']
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


