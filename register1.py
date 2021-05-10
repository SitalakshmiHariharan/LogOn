from flask import Flask
from flask import render_template # to render our html page
from flask import request # to get user input from form
import hashlib # included in Python library, no need to install
import psycopg2 # for database connection

app = Flask(__name__)

@app.route("/")

def showForm():
    # show our html form to the user
    t_message = "Python and Postgres Registration Application"
    return render_template("register.html", message = t_message)

@app.route("/register", methods=["POST","GET"])
def register():
    # get user input from the html form
    t_email = request.form.get("t_email", "")
    t_password = request.form.get("t_password", "")

    # check for blanks
    if t_email == "":
        t_message = "Please fill in your email address"
        return render_template("register.html", message = t_message)

    if t_password == "":
        t_message = "Please fill in your password"
        return render_template("register.html", message = t_message)

    # hash the password they entered
    t_hashed = hashlib.sha256(t_password.encode())
    t_password = t_hashed.hexdigest()

    # database insert
    t_host = "database server address here"
    t_port = "5432"
    t_dbname = "practice"
    t_user = "remote"
    t_pw = "password here"
    db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
    db_cursor = db_conn.cursor()

    # We take the time to build our SQL query string so that
    #   (a) we can easily & quickly read it
    #   (b) we can easily & quickly edit or add/remote lines
    #   The more complex the query, the greater the benefits
    s = "INSERT INTO public.users "
    s += "("
    s += "  t_email"
    s += ", t_password"
    s += ") VALUES ("
    s += " '" + t_email + "'"
    s += ",'" + t_password + "'"
    s += ")"
    # Warning: this format allows for a user to try to insert
    #   potentially damaging code, commonly known as "SQL injection".
    #   In a later article we will show some methods for
    #   preventing this.

    # Here we are catching and displaying any errors that occur
    #   while TRYing to commit the execute our SQL script.
    db_cursor.execute(s)
    try:
        db_conn.commit()
    except psycopg2.Error as e:
        t_message = "Database error: " + e + "/n SQL: " + s
        return render_template("register.html", message = t_message)

    t_message = "Your user account has been added."
    return render_template("register.html", message = t_message)

# this is for command line testing
if __name__ == "__main__":
    app.run(debug=True)