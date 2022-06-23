from flask import render_template, jsonify
from config import app
from flask_mysqldb import MySQL
import MySQLdb.cursors
mysql = MySQL(app)
from flask import request
import json

# create a registration form
@app.route("/")
def index():
    print(db())
    return render_template('register.html')

# insert user details into the database
@app.route("/insertToUser", methods=['GET', 'POST'])
def insertToUser():
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            phone_number = request.form.get('phone_number')
            password = request.form.get('password')
            tickbox = request.form.get('tickbox')

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO user VALUES (NULL, %s, %s, %s, %s, %s)', (username, email, phone_number, password, tickbox))
            mysql.connection.commit()
            data = 'You have successfully registered!'
            return data
            
        except Exception as e:
            print("Problem fetch from user table: " + str(e))
            return "fail"

# create REST API
@app.route("/api/v1")
def db():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)                                         
        cursor.execute('SELECT * FROM user where tickbox=1')
        data = cursor.fetchall()

        str1 = []
        for data1 in data:
            str1.append({"email":data1['email'], "phone_number":data1['phone_number']})
        return jsonify(str1)
    
    except Exception as e:
        print("Problem fetch from user table: " + str(e))
        return 'fail'

if __name__ == "__main__":
    # db.create_all
    app.run(debug=True)
    index()