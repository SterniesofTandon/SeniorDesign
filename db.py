from init1 import app
from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'b7a4c6df042881'
app.config['MYSQL_DATABASE_PASSWORD'] = '103d0b48'
app.config['MYSQL_DATABASE_DB'] = 'heroku_4cd6105b897017f'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-04.cleardb.com'
mysql.init_app(app)


# mysql --host=us-cdbr-east-04.cleardb.com --user=b7a4c6df042881 --password=103d0b48 --reconnect heroku_4cd6105b897017f