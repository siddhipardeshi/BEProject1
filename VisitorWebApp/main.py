# importing flask modules
from flask import Flask, render_template,request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

# initializing a variable of Flask
app = Flask(__name__)

app.secret_key = 'frd'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '52Pr@n@li'
app.config['MYSQL_DB'] = 'beproject'

mysql = MySQL(app)
# decorating index function with the app.route with url as /login
@app.route('/')
def home():
   return render_template('HomePage.html')


@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/UserLogin.html')
def UserLogin():
    return render_template('Userlogin.html')

@app.route('/index.html', methods=['GET','POST'])
def index():
    msg = ''
    print("hello")
    if request.method == 'POST'and 'fullname' in request.form and 'password' in request.form and 'email' in request.form and 'confirmpassword' in request.form :
        print("hello")
        username = request.form['fullname']
        password = request.form['password']
        email = request.form['email']
        cpassword = request.form['confirmpassword']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM fake_review_detection WHERE username = % s', (username,))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not re.match(r'[A-Za-z0-9]+', password):
            msg = 'Enter valid password!'
        elif not re.match(password, cpassword):
            msg = 'Enter valid confirm password'
        elif not username or not password or not email or not cpassword:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO fake_review_detection VALUES (% s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return render_template('index.html', msg=msg)

    elif request.method == 'POST' and 'username' in request.form and 'password1' in request.form:
        username = request.form['username']
        password1 = request.form['password1']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM fake_review_detection WHERE username = % s AND password = % s', (username, password1,))
        account = cursor.fetchone()
        print(account)
        if account:
            session['loggedin'] = True
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'

    elif request.method == 'POST':
        return render_template('index.html', msg=msg)

    return render_template('UserLogin.html', msg=msg)

@app.route('/hotelsInPune.html')
def hotelsInPune():
    return render_template('hotelsInPune.html')

@app.route('/hotelsInMumbai.html')
def hotelsInMumbai():
    return render_template('hotelsInMumbai.html')

@app.route('/hotelsInKolkata.html')
def hotelsInKolkata():
    return render_template('hotelsInKolkata.html')

@app.route('/hotelsInBangalore.html')
def hotelsInBangalore():
    return render_template('hotelsInBangalore.html')


if __name__ == "__main__":
   app.run(debug=True)