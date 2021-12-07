# Import Flask Library
# from flask import Flask, render_template, request, session, url_for, redirect
#import only what we need
from flask import *
import pymysql.cursors
# from flaskext.mysql import MySQL
import hashlib
import os
import time
import random
import string
# from db import *
from flask import request, send_from_directory
from functools import wraps
IMAGES_DIR = os.path.join(os.getcwd(), "images")
from flask_bootstrap import Bootstrap
# import mysql.connector



# Initialize the app from Flask

app = Flask(__name__,
            static_url_path='', 
            static_folder='templates/static',
            template_folder='templates')

# app.config['MYSQL_DATABASE_USER'] = 'b7a4c6df042881'
# app.config['MYSQL_DATABASE_PASSWORD'] = '103d0b48'
# app.config['MYSQL_DATABASE_DB'] = 'heroku_4cd6105b897017f'
# app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-04.cleardb.com'
Bootstrap(app)

# mysql = MySQL()
# mysql.init_app(Bootstrap(app))
SALT = "sd102699"
# mysql.init_app(app)
# conn = pymysql.connect()

# connection = mysql.connector.connect(
#     host="us-cdbr-east-04.cleardb.com", 
#     user="b7a4c6df042881",
#     password="103d0b48",
#     database="heroku_4cd6105b897017f"
#   )
#   port="3306",
#   auth_plugin='mysql_native_password'

# conn = connection.cursor()

# Configure MySQL
conn = pymysql.connect(host='localhost',
                       port = 8889,
                       user='root',
                       password='root',
                       db='FlaskDemo',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


# if __name__ == '__main__':
#     app.run(debug=True)                       

# Define a route to hello function
@app.route('/')
def hello():
    return render_template('index.html')

# Make sure user is logged in
def login_required(func):
    @wraps(func)
    def dec(*args, **kwargs):
        if not 'username' in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return dec

# Define route for login, this can be used by both CSR and customer
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/loginCSR')
def loginCSR():
    return render_template('loginCSR.html') 

# Define route for register for customer
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/registerCSR')
def registerCSR():
    return render_template('registerCSR.html')

# Define route for register
@app.route('/csrPage')
def csrPage():
    return render_template('csrPage.html')

@app.route('/homeCSR')
def homeCSR():
    return render_template('homeCSR.html')

# Define route for register
@app.route('/customerPage')
def customerPage():
    return render_template('customerPage.html')

# Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    # grabs information from the forms
    username = request.form['username']
    pwd = request.form['pwd']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query -> TODO: ADD func called userExists
    query = 'SELECT * FROM user WHERE username = %s and pwd = %s'
    cursor.execute(query, (username, pwd))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data): #user exists
        # creates a session for the the user
        # session is a built in
        session['username'] = username
        return redirect(url_for('home'))
    else:
        # returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)

# Authenticates the login for CSR
@app.route('/loginAuthCSR', methods=['GET', 'POST'])
def loginAuthCSR():
    # grabs information from the forms
    username = request.form['username']
    pwd = request.form['pwd']
    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM user WHERE username = %s and pwd = %s'
    cursor.execute(query, (username, pwd))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data): #user exists
        # creates a session for the the user
        # session is a built in
        session['username'] = username
        return redirect(url_for('homeCSR'))
    else:
        # returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('loginCSR.html', error=error)

# @app.route('/loginAuthCSR', methods=['GET', 'POST'])
# def loginAuthCSR():
#     # grabs information from the forms
#     username = request.form['username']
#     pwd = request.form['pwd']
#     # cursor used to send queries
#     cursor = conn.cursor()
#     # executes query -> TODO: ADD func called userExists
#     query = 'SELECT * FROM csr WHERE username = %s and pwd = %s'
#     cursor.execute(query, (username, pwd))
#     # stores the results in a variable
#     data = cursor.fetchone()
#     # use fetchall() if you are expecting more than 1 data row
#     cursor.close()
#     error = None
#     if(data): #user exists
#         # creates a session for the the user
#         # session is a built in
#         session['username'] = username
#         return redirect(url_for('homeCSR'))
#     else:
#         # returns an error message to the html page
#         error = 'Invalid login or username'
#         return render_template('loginCSR.html', error=error)

""" 
Registers the customer
"""
@app.route('/registerAuth', methods=['POST'])
def registerAuth():
    # grabs information from the forms
    username = request.form['username']
    pwd = request.form['pwd'] # + SALT 
    # print(f"{pwd=}")
    hashed_password = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
    randomString = string.ascii_uppercase + string.digits
    anon_code = ''.join(random.choice(randomString) for i in range(8))
    #Information that gets encrypted below
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    addr = request.form['addr']
    phone_number = request.form['phone_number']
    card_number = request.form['card_number']
    #we have to generate anon code
    key_str = "08242007"
    first_nameE = first_name
    last_nameE = last_name
    addrE = addr
    phone_numberE = phone_number
    card_numberE = card_number

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM user WHERE username = %s'
    cursor.execute(query, (username))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        # print("User already exists")
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:
        ins = '''INSERT INTO user VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(ins, (username, pwd, anon_code, first_name, last_name, addr, phone_number, card_number))
        #insert all the encrypted data
        insE = '''INSERT INTO userE VALUES(%s, AES_ENCRYPT(%s, "08242007"), AES_ENCRYPT(%s, "08242007"), 
        AES_ENCRYPT(%s,"08242007"), AES_ENCRYPT(%s, "08242007"), AES_ENCRYPT(%s, "08242007"))'''
        cursor.execute(insE, (anon_code, first_nameE, last_nameE, addrE, phone_numberE, card_numberE))
        conn.commit()
        cursor.close()
        return render_template('login.html')

@app.route('/registerAuthCSR', methods=['POST'])
def registerAuthCSR():
    # grabs information from the forms
    username = request.form['username']
    pwd = request.form['pwd'] # + SALT 
    hashed_password = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
    randomString = string.ascii_uppercase + string.digits
    anon_code = ''.join(random.choice(randomString) for i in range(8))
    #Information that gets encrypted below
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    key_str = "08242007"
    first_nameE = first_name
    last_nameE = last_name

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM user WHERE username = %s'
    cursor.execute(query, (username))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        # If the previous query returns data, then user exists
        error = "This customer service representative already exists"
        return render_template('registerCSR.html', error = error)
    else:
        ins = '''INSERT INTO user VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'''
        cursor.execute(ins, (username, pwd, anon_code, first_name, last_name, None, None, None))
        conn.commit()
        cursor.close()
        return render_template('loginCSR.html')

# Authenticates the register for the customer service representatives
# @app.route('/registerAuthCSR', methods=['GET', 'POST'])
# def registerAuthCSR():
#     # grabs information from the forms
#     username = request.form['username']
#     pwd = request.form['pwd'] # + SALT 
#     hashed_password = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
#     #information to be encrypted:
#     first_name = request.form['first_name']
#     last_name = request.form['last_name']

#     # cursor used to send queries
#     cursor = conn.cursor()
#     # executes query
#     query = 'SELECT * FROM csr WHERE username = %s'
#     cursor.execute(query, (username))
#     # stores the results in a variable
#     data = cursor.fetchone()
#     # use fetchall() if you are expecting more than 1 data row
#     error = None
#     if(data):
#         # If the previous query returns data, then user exists
#         error = "This customer service representative already exists"
#         return render_template('registerCSR.html', error = error)
#     else:
#         ins = '''INSERT INTO csr VALUES(%s, %s, %s, %s)'''
#         cursor.execute(ins, (username, pwd, first_name, last_name))
#         conn.commit()
#         cursor.close()
#         return render_template('loginCSR.html')

# Displays home page
@app.route('/home')
def home():
    user = session['username']
    cursor = conn.cursor()
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (user))
    data = cursor.fetchall()

    query2 = "SELECT first_name FROM user WHERE username = %s"
    # cursor = conn.cursor().execute(query2, user)
    name = conn.cursor().execute(query2, user)
    name = cursor.fetchall() #TODO: Fix; Only displays 1
    
    cursor.close()
    return render_template('home.html', username=user, posts=data, names=name)

# Upload an order
@app.route("/upload")
@login_required
def upload():
    query = "SELECT groupName, groupCreator FROM BelongTo WHERE username = %s"
    with conn.cursor() as cursor:
        cursor.execute(query, (session["username"]))
    data = cursor.fetchall()
    return render_template("upload.html", groups = data)

@app.route("/uploadOrder", methods=["GET", "POST"])
@login_required
def uploadOrder():
    if request.files:
        image_file = request.files.get("imageToUpload", "")
        image_name = image_file.filename
        filePath = os.path.join(IMAGES_DIR, image_name)
        image_file.save(filePath) 

        userName = session["username"]
        caption = request.form.get('caption')
        display = request.form.get('display')
        curr_time = time.strftime('%Y-%m-%d %H:%M:%S')
        ord_num = str(random.randint(0,100))

        #Grab Anoncode
        query = "SELECT anon_code FROM user WHERE username = %s"
        with conn.cursor() as cursor:
            cursor.execute(query, (session["username"]))
            anon_code = cursor.fetchone()
            cursor.close()
        anon_code = anon_code['anon_code']

        #Post to all followers
        if True: 
            query = "INSERT INTO Orders (pID, postingDate, filePath, caption, poster) " \
                    "VALUES (%s, %s, %s, %s, %s)"
            with conn.cursor() as cursor:
                cursor.execute(query, (ord_num, curr_time, image_name, caption, anon_code))
                conn.commit()
                cursor.close()
            # #Encrypted upload
            query = "INSERT INTO OrdersE (pID, postingDate, filePath, caption, posterE) " \
                    "VALUES (%s, %s, %s, %s, %s)"
            with conn.cursor() as cursor:
                cursor.execute(query, (ord_num, curr_time, image_name, caption, anon_code))
                conn.commit()
                cursor.close()

        message = "Order successfully uploaded."
        return render_template("upload.html", message=message)

    else:
        message = "Failed to upload order"
        return render_template("upload.html", message=message)

# View orders (SEVERAL PARTS)
#CUSTOMER SIDE
@app.route("/orders", methods = ["GET"])
@login_required
def orders(): 
    user = session["username"]
    cursor = conn.cursor()
    query = "SELECT pID, poster, filePath FROM Orders ORDER BY postingDate DESC"
    cursor.execute(query)
    photos = cursor.fetchall()
    cursor.close()
    
    return render_template("orders.html", photos = photos)

@app.route("/viewOrders/<int:pID>", methods=["GET", "POST"])
@login_required
def viewOrders(pID):
    user = session["username"]
    
    #query for pID, filePath, postingDate
    cursor = conn.cursor()
    query = "SELECT pID, postingDate, filePath FROM Orders WHERE pID = %s"
    cursor.execute(query, (pID))
    data = cursor.fetchall()

    #first and last name of the poster 
    query2 = "SELECT first_name, last_name FROM user WHERE username = %s"
    cursor = conn.cursor()
    cursor.execute(query2, (user))
    name = cursor.fetchall()

    #username of people who Reacted
    query4 = "SELECT anon_code, reactionTime, comment FROM ReactTo WHERE pID = %s "
    cursor = conn.cursor()
    cursor.execute(query4, (pID))
    comment = cursor.fetchall()

    return render_template("viewOrders.html", photos = data, names = name, comments = comment)

#CSR SIDE
@app.route("/ordersCSR", methods = ["GET"])
@login_required
def ordersCSR(): 
    user = session["username"]
    cursor = conn.cursor()
    query = "SELECT pID, posterE, filePath FROM OrdersE ORDER BY postingDate DESC"
    cursor.execute(query)
    photos = cursor.fetchall()
    cursor.close()
    
    return render_template("ordersCSR.html", photos = photos)

@app.route("/viewOrdersCSR/<int:pID>", methods=["GET", "POST"])
@login_required
def viewOrdersCSR(pID):
    user = session["username"]
    
    #query for pID, filePath, postingDate
    cursor = conn.cursor()
    query = "SELECT pID, postingDate, filePath FROM OrdersE WHERE pID=%s"
    cursor.execute(query, (pID))
    data = cursor.fetchall()
    # print(data)

    #first and last name of the poster 
    query2 = "SELECT first_nameE, last_nameE FROM userE"
    cursor = conn.cursor()
    cursor.execute(query2)
    name = cursor.fetchall()

    #username of people who Reacted
    query4 = "SELECT anon_code, reactionTime, comment FROM ReactTo"
    cursor = conn.cursor()
    cursor.execute(query4)
    comment = cursor.fetchall()

    return render_template("viewOrdersCSR.html", photos = data, names = name, comments = comment)

@app.route("/photo/<image_name>", methods=["GET"])
def image(image_name):
    image_location = os.path.join(IMAGES_DIR, image_name)
    if os.path.isfile(image_location):
        return send_file(image_location, mimetype="image/jpg")

@app.route("/comment/<pID>", methods=["GET", "POST"])
@login_required
def comment(pID):
    cursor = conn.cursor()

    if(request.form): 	
        # user = session["username"]
        
        comment = request.form["comment"]
        #Grab Anoncode
        query = "SELECT anon_code FROM user WHERE username = %s"
        with conn.cursor() as cursor:
            cursor.execute(query, (session["username"]))
            anon_code = cursor.fetchone()
            cursor.close()
        anon_code = anon_code['anon_code']

        cursor = conn.cursor()
        query = "INSERT INTO ReactTo (anon_code, pID, reactionTime, comment) VALUES (%s, %s, %s, %s)"
        # cursor.execute(query, (user, pID, time.strftime('%Y-%m-%d %H:%M:%S'), comment))	
        cursor.execute(query, (anon_code, pID, time.strftime('%Y-%m-%d %H:%M:%S'), comment))	
        cursor.close()

        return redirect(url_for('viewOrders', pID = pID))
        
    cursor.close()
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')
        
app.secret_key = 'somekeythatyouwillneverguess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    # app.run('127.0.0.1', 5000, debug = True)
    app.run()

@app.route('/follow', methods = ["GET", "POST"])
@login_required
def follow(): 

	cursor = conn.cursor()

	if(request.form): 
		user = session["username"]
		followee = request.form["followee"]	
		
		query = "INSERT INTO Follow(follower, followee, followStatus) VALUES (%s, %s, %s)"
		cursor = conn.cursor()
		cursor.execute(query, (user, followee, 1))
		cursor.close()
		return render_template("homeCSR.html")

	return render_template("follow.html")


'''
@app.route('/post', methods=['GET', 'POST'])
def post():
    username = session['username']
    cursor = conn.cursor();
    blog = request.form['blog']
    query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
    cursor.execute(query, (blog, username))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))

@app.route('/select_blogger')
def select_blogger():
    #check that user is logged in
    #username = session['username']
    #should throw exception if username not found

    cursor = conn.cursor();
    query = 'SELECT DISTINCT username FROM blog'
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return render_template('select_blogger.html', user_list=data)

@app.route('/show_posts', methods=["GET", "POST"])
def show_posts():
    poster = request.args['poster']
    cursor = conn.cursor();
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, poster)
    data = cursor.fetchall()
    cursor.close()
    return render_template('show_posts.html', poster_name=poster, posts=data)
'''
