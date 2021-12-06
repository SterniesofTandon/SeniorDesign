from init1 import app
from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'b57540bad9807c'
app.config['MYSQL_DATABASE_PASSWORD'] = '443e8670'
app.config['MYSQL_DATABASE_DB'] = 'heroku_9cf2aa10a1189'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-04.cleardb.com'
mysql.init_app(app)


# mysql --host=us-cdbr-east-04.cleardb.com --user=b57540bad9807c --password=443e8670 --reconnect heroku_9cf2aa10a1189fb
