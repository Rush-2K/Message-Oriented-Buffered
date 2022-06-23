from flask import Flask
import secrets

app = Flask(__name__)

# setup localhost and database
app.secret_key = secrets.token_hex(16)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = '<YOUR_USERNAME>'
app.config['MYSQL_PASSWORD'] = '<YOUR_PASSWORD>'
app.config['MYSQL_DB'] = '<YOUR_DATABASE_NAME>'