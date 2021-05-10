from flask import Flask
from flask import render_template 
from flask import request, redirect, url_for

import hashlib 
import psycopg2 

from flask_mail import Mail
from flask_mail import Message

app = Flask(__name__)

def smtp_config(config_name, smtp=1):
    with open(config_name) as f:
            config_data = json.load(f)
    if smtp not in {1,2}:
        raise ValueError("smtp can only be 1 or 2")
    if smtp==2:
        MAIL_USERNAME = config_data['MAIL_USERNAME'][1]
        MAIL_PASSWORD = config_data['MAIL_PASSWORD'][1]
    else:
        MAIL_USERNAME = config_data['MAIL_USERNAME'][0]
        MAIL_PASSWORD = config_data['MAIL_PASSWORD'][0]
    MAIL_SERVER = config_data['MAIL_SERVER']
    MAIL_PORT = config_data['MAIL_PORT']
    MAIL_USE_TLS = bool(config_data['MAIL_USE_TLS'])
    return [MAIL_USERNAME, MAIL_PASSWORD, MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS]

mail = Mail()

# Database creds
t_host = "localhost"
t_port = "5432"
t_dbname = "postgres"
t_user = "postgres"
t_pw = ""
db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
db_cursor = db_conn.cursor()

@app.route("/")

def showForm():
    t_message = "Python and Postgres Registration Application"
    return render_template("register.html", message = t_message)

@app.route("/register", methods=["POST","GET"])
def register():
    print("In the register route")
    ID_user = request.args.get("confirm", "")    
    t_password = request.files.get("t_Password")
    
    if ID_user == "":
        t_email = request.form.get("t_Email", "")
        t_password = request.form.get("t_Password", "")
        print("t_email is")
        print(t_email)
        print("t_password is")
        print(t_password)
        if t_email == "":
            t_message = "Please fill in your email address in here"
            return render_template("register.html", message = t_message)

        if t_password == "":
            t_message = "Please fill in your password in here"
            return render_template("register.html", message = t_message)        
        
        s = ""
        s += "INSERT INTO users "
        s += "("
        s += " t_email"
        s += ",t_password"
        s += ",b_enabled"
        s += ") VALUES ("
        s += " '" + t_email + "'"
        s += ",'" + t_password + "'"
        s += ", false"
        s += ")"
        
        db_cursor.execute(s)
        print("Query executed")
        try:
            db_conn.commit()
        except psycopg2.Error as e:
            print("There was an error in the query execution")
            t_message = "Database error: " + e + "/n SQL: " + s
            return render_template("error.html", message = t_message)
        
        s = ""
        s += "SELECT ID FROM users "
        s += "WHERE"
        s += "("
        s += " t_email ='" + t_email + "'"
        s += " AND"
        s += " b_enabled = false"
        s += ")"
    
        db_cursor.execute(s)
       
        try:
            array_row = db_cursor.fetchone()
        except psycopg2.Error as e:
            t_message = "Database error: " + e + "/n SQL: " + s
            return render_template("register.html", message = t_message)

        ID_user = array_row[0]
        
        db_cursor.close()
        db_conn.close()   
        
        t_message = "Your user account has been added. Check your email for confirmation link."
        return render_template("register.html", message = t_message)
    else:
        s = ""
        s += "UPDATE users SET"
        s += ",b_enabled = flase"
        s += "WHERE"
        s += "("
        s += " ID=" + ID_user
        s += ")"
       
        db_cursor.execute(s)
        try:
            db_conn.commit()
        except psycopg2.Error as e:
            t_message = "Database error: " + e + "/n SQL: " + s
            return render_template("register.html", message = t_message)
        db_cursor.close()        
        t_message = "Your user account has been added. Thanks for verifying your email address!"
        return render_template("register.html", message = t_message)

   
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)