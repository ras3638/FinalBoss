#!bin/python
from flask import Flask, jsonify
from flask import render_template, flash, redirect

from forms import LoginForm

app = Flask(__name__)
app.config.from_object('config')


@app.route('/index',  methods = ['GET', 'POST'])
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
      'description': u'Need to find finish project for Networking class',
      'done': False
   }
]
    return render_template('index.html',
        title = 'ToDo List',
        user = user,
        tasks = tasks)


if __name__ == '__main__':
   app.run(debug = True)


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
      'description': u'Need to find finish project for Networking class',
      'done': False
   }
]

@app.route('/todo/api/v1.0/tasks', methods = ['GET'])
def get_tasks():
   return jsonify( { 'tasks': tasks } )



@app.route('/NewUser', methods = ['GET', 'POST'])
def NewUser():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Signup Username="' + form.openid.data + '", Signup Password=')
        return redirect('/login')
    return render_template('NewUser.html',
        title = 'Sign Up',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@app.route('/')
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])
