# Import Flask Library
# from flask import Flask, render_template, request, session, url_for, redirect
from flask import *
import pymysql.cursors
import hashlib
import os
import time
from functools import wraps
IMAGES_DIR = os.path.join(os.getcwd(), "images")


# Initialize the app from Flask
app = Flask(__name__)
SALT = "sd102699"

# Configure MySQL
conn = pymysql.connect(host='localhost',
                       port = 8889,
                       user='root',
                       password='root',
                       db='FlaskDemo',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


if __name__ == '__main__':
    app.debug = True
    app.run()                       

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

# Define route for register
@app.route('/customerPage')
def customerPage():
    return render_template('customerPage.html')

# Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query -> TODO: ADD func called userExists
    query = 'SELECT * FROM user WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
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

# Authenticates the register for the customer
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password'] + SALT 
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    #information to be encrypted:
    anon_code = "2839473sl"
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    address = request.form['address']
    phone_number = request.form['phone_number']
    card_number = request.form['card_number']
    #we have to generate anon code

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
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:
        ins = '''INSERT INTO user VALUES(%s, %s,anon_code, %s, %s, %s, %s, %s))'''
        cursor.execute(ins, (username, password, anon_code, first_name, last_name, address, phone_number, card_number))
        conn.commit()
        cursor.close()
        return render_template('login.html')

# Authenticates the register for the customer service representatives
@app.route('/registerAuthCSR', methods=['GET', 'POST'])
def registerAuthCSR():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password'] + SALT 
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    #information to be encrypted:
    first_name = request.form['first_name']
    last_name = request.form['last_name']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM csr WHERE username = %s'
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
        ins = '''INSERT INTO csr VALUES(%s, %s, %s, %s))'''
        cursor.execute(ins, (username, password, first_name, last_name))
        conn.commit()
        cursor.close()
        return render_template('login.html')

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

        #Post to all followers
        if True:
            query = "INSERT INTO Order (postingDate, filePath, caption, poster) " \
                    "VALUES (%s, %s, %s, %s)"
            with conn.cursor() as cursor:
                cursor.execute(query, (time.strftime('%Y-%m-%d %H:%M:%S'), image_name, caption, userName))
                conn.commit()
                cursor.close()

        message = "Order successfully uploaded."
        return render_template("upload.html", message=message)

    else:
        message = "Failed to upload order"
        return render_template("upload.html", message=message)

# View orders (SEVERAL PARTS)
@app.route("/orders", methods = ["GET"])
@login_required
def orders(): 
    user = session["username"]
    cursor = conn.cursor()
    query = "SELECT pID, poster, filePath FROM Order ORDER BY postingDate DESC"
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
    query = "SELECT pID, postingDate, filePath FROM Order WHERE pID = %s"
    cursor.execute(query, (pID))
    data = cursor.fetchall()

    #first and last name of the poster 
    query2 = "SELECT first_name, last_name FROM user WHERE username = %s"
    cursor = conn.cursor()
    cursor.execute(query2, (user))
    name = cursor.fetchall()

    #username of people who Reacted
    query4 = "SELECT username, reactionTime, comment FROM ReactTo WHERE pID = %s "
    cursor = conn.cursor()
    cursor.execute(query4, (pID))
    comment = cursor.fetchall()

    return render_template("viewOrders.html", photos = data, names = name, comments = comment)

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
        user = session["username"]
        comment = request.form["comment"]
    
        query = "INSERT INTO ReactTo (username, pID, reactionTime, comment) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (user, pID, time.strftime('%Y-%m-%d %H:%M:%S'), comment))	
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
    app.run('127.0.0.1', 5000, debug = True)

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
