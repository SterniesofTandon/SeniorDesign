# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import hashlib


# Initialize the app from Flask
app = Flask(__name__)
SALT = "sd210699"

# Configure MySQL
conn = pymysql.connect(host='localhost',
                       port = 8889,
                       user='root',
                       password='root',
                       db='FlaskDemo',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

# Define a route to hello function
@app.route('/')
def hello():
    return render_template('index.html')

# Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

# Define route for register
@app.route('/register')
def register():
    return render_template('register.html')

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

# Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password'] + SALT 
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    #information to be encrypted:
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    address = request.form['address']
    phone_number = request.form['phone_number']
    card_number = request.form['card_number']

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
        ins = 'INSERT INTO user VALUES(%s, %s, %s, %s, %s, %s, %s))'
        cursor.execute(ins, (username, password, first_name, last_name, address, phone_number, card_number))
        conn.commit()
        cursor.close()
        return render_template('index.html')

# Displays home page
@app.route('/home')
def home():
    user = session['username']
    cursor = conn.cursor();
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (user))
    data = cursor.fetchall()
    cursor.close()
    return render_template('home.html', username=user, posts=data)

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


'''
AGENT LOGIN:
@app.route('/agent_login_auth', methods=['GET', 'POST'])
def agent_login_auth():
	email = request.form['email']
	password = request.form['password']
	cursor = conn.cursor()
	query = 'SELECT * FROM booking_agent WHERE email = %s and password = MD5(%s)'
	cursor.execute(query, (email, password))
	data = cursor.fetchone()
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = email
		return redirect(url_for('agent_home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or email'
		return render_template('agent_login.html', error=error)

@app.route('/agent_register', methods=['GET', 'POST'])
def agent_register():
	return render_template('agent_register.html')

#Authenticates the register for agent
@app.route('/agent_register_auth', methods=['GET', 'POST'])
def agent_register_auth():
	email = request.form['email']

	cursor = conn.cursor()
	query = 'SELECT * FROM booking_agent WHERE email = %s'
	cursor.execute(query, (email))
	data = cursor.fetchone()
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('agent_register.html', error = error)
	else:
		booking_agent_ID = request.form['booking_agent_ID']
		password = request.form['password']
		
		ins = '''INSERT INTO booking_agent (email,password,booking_agent_ID)
				 VALUES(%s,MD5(%s),%s)'''
		cursor.execute(ins, (email,password,booking_agent_ID))
		conn.commit()
		cursor.close()
		return redirect('/agent_login')

TICKETING CODE TO USE FOR ORDER NUMBER:

@app.route('/view_flights', methods=['GET', 'POST'])
def view_flights():
	cursor = conn.cursor()

	from_home = request.form['from_home']
	data = 0

	start_date = 0
	end_date = 0

	if from_home:
		start_date = request.form['start_date']
		end_date = request.form['end_date']
		query = '''SELECT * FROM flight_expanded
				WHERE departure_date >= %s AND departure_date <= %s
				ORDER BY departure_date DESC,departure_time ASC'''
		cursor.execute(query, (start_date,end_date))
		data = cursor.fetchall()
	else:
		start_date = request.form['start_date']
		end_date = request.form['end_date']
		query = '''SELECT * FROM flight_expanded 
				   WHERE departure_date BETWEEN %s AND %s
			       ORDER BY departure_date DESC'''
		cursor.execute(query, (start_date,end_date))
		data = cursor.fetchall()

	cursor.close()
	return render_template('view_flights.html', data=data, start_date=start_date, end_date=end_date, from_home=False)

@app.route('/view_customers', methods=['GET', 'POST'])
def view_customers():
	airline = session['airline']
	flight_number = request.form['flight_number']
	cursor = conn.cursor()
	query = '''SELECT customer.name, customer.email
			   FROM ticket JOIN customer ON (ticket.customer_email = customer.email)
			   WHERE airline = %s AND flight_number = %s'''
	cursor.execute(query, (airline,flight_number))
	data = cursor.fetchall()
	cursor.close()
	return render_template('view_customers.html',data=data)

'''