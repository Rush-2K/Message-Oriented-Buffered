from flask import Flask
import secrets

app = Flask(__name__)

# setup localhost and database
app.secret_key = secrets.token_hex(16)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rusyaididatabase'
app.config['MYSQL_DB'] = 'messagebrokerdb'