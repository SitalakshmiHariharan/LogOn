from flask import Flask
from flask import render_template, redirect
from flask import request 
import hashlib 
import psycopg2  
from flask_mail import Message
from datetime import datetime

app = Flask(__name__)

# Database creds
t_host = "localhost"
t_port = "5432" #default postgres port
t_dbname = "postgres"
t_user = "postgres"
t_pw = ""
db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
db_cursor = db_conn.cursor()

@app.route("/")
def showForm():
    t_message = "Login Application"
    return render_template("sign-in.html", message = t_message)

@app.route("/sign_in", methods=["POST","GET"])
def sign_in():    
    print("Inside the sign in route")
    ID_user = request.args.get("ID_user")
    t_email = request.form.get("t_email", "")
    t_stage = request.args.get("stage")
    print(ID_user)
    print(t_email)
    print(t_stage)
    if t_stage == "login" :
        t_password = request.form.get("t_password", "")
        print("At the login stage with password", t_password)
        
        if t_email == "":            
            if t_stage == "forgot":
                t_message = "Reset Password: Please fill in your email address"
            else:
                t_message = "Login: Please fill in your email address"
            
            return render_template("sign_in.html", message = t_message)
        
        if (t_stage == "login" or t_stage == "reset") and t_password == "":
            t_message = "Login: Please fill in your password"            
            return render_template("sign_in.html", message = t_message)
        
    if t_stage == "login" or t_stage == "reset":
        # Hash the password
        #t_hashed = hashlib.sha256(t_password.encode())
        #t_password = t_hashed.hexdigest()
        print("********** 1. Before the query ************") 
        # Get user ID from PostgreSQL users table
        s = ""
        s += "SELECT ID FROM users"
        s += " WHERE"
        s += " ("
        s += " t_email ='" + t_email + "'"
        if t_stage != "login":
            s += " AND"
            s += " t_password = '" + t_password + "'"
        s += " )"
        print(s)
        db_cursor.execute(s)
        print("*********** 1. Query is executed **************")
       
        try:
            array_row = db_cursor.fetchone()
        except psycopg2.Error as e:
            t_message = "Database error: " + e + "/n SQL: " + s
            return render_template("sign_in.html", message = t_message)
       
        #db_cursor.close()
        #db_conn.close()
        print("it is above array_row", array_row)
        if array_row is None:
            t_message = "Your credentials does not exist. Please register !!"
            return render_template("sign-in.html", message = t_message)         
        else:
            ID_user = array_row[0]
    
    if t_stage == "login":       
        
        now = datetime.now()
        now_str = now.strftime("%m/%d/%Y %H:%M:%S")
        
        print("**********2. Before the query************")
        s = ""
        s += "UPDATE users SET"
        s += " d_visit_last = '" + now_str + "'"
        s += " WHERE"
        s += "("
        s += " t_email='" + t_email + "'"
        s += ")"
        
        db_cursor.execute(s)
        print("***********2. Query is executed**************")
        try:
            db_conn.commit()
        except psycopg2.Error as e:
            t_message = "Login: Database error: " + e + "/n SQL: " + s
            return render_template("sign_in.html", message = t_message)
        
        db_cursor.close()
        db_conn.close()

        # Redirect user to the rest of the application
        return redirect("http://jobsage-c629c.web.app", code=302) 

# This is for command line testing
if __name__ == "__main__":
    app.run(debug=True)