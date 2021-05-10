from flask import Flask
from flask import render_template # to render the html form
from flask import request # to get user input from sign-in form
import hashlib # included in Python library, no need to install
import psycopg2 # for database connection
    # IMPORTANT
    # In a later part of this article series we will add code here
    # IMPORTANT
from flask_mail import Message

app = Flask(__name__)

# Mail creds
    # IMPORTANT
    # In a later part of this article series we will add code here
    # IMPORTANT

# Database creds
t_host = "database address"
t_port = "5432" #default postgres port
t_dbname = "database name"
t_user = "database user name"
t_pw = "database user password"
db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
db_cursor = db_conn.cursor()

@app.route("/")

def showForm():
    # Show our html form to the user.
    t_message = "Login Application"
    return render_template("sign_in.html", message = t_message)

@app.route("/sign_in", methods=["POST","GET"])
def sign_in():
    t_stage = request.args.get("forgot")
    ID_user = request.args.get("ID_user")
    t_email = request.form.get("t_email", "")
    # The test for "reset" we see here will become relevant later in this article series.
    if t_stage == "login" OR t_stage == "reset":
        t_password = request.form.get("t_password", "")

    # Check for email field left empty
    if t_email == "":
        # "forgot" test below is for later part of our multi-part article, fine here for now:
        if t_stage == "forgot":
            t_message = "Reset Password: Please fill in your email address"
        else:
            t_message = "Login: Please fill in your email address"
        # If empty, send user back, along with a message
        return render_template("sign_in.html", message = t_message)

    # Check for password field left empty
    # Note we are checking the t_stage variable to see if they are signing in or they forgot their password
    #   If they forgot their password, we don't want their password here. We only want their email address
    #   so we can send them a link in the next part of this article.
    # In both 1st stage and 3rd, we harvest password, so t_stage is "login" or "reset"
    if (t_stage == "login" OR t_stage == "reset") AND t_password == "":
        t_message = "Login: Please fill in your password"
        # If empty, send user back, along with a message
        return render_template("sign_in.html", message = t_message)

    # In both 1st stage and 3rd, we harvest password, so t_stage is "login" or "reset"
    if t_stage == "login" OR t_stage == "reset":
        # Hash the password
        t_hashed = hashlib.sha256(t_password.encode())
        t_password = t_hashed.hexdigest()

    # Get user ID from PostgreSQL users table
    s = ""
    s += "SELECT ID FROM users"
    s += " WHERE"
    s += " ("
    s += " t_email ='" + t_email + "'"
    if t_stage != "login":
        s += " AND"
        s += " t_password = '" + t_password + "'"
    s += " AND"
    s += " b_enabled = true"
    s += " )"

    db_cursor.execute(s)

    # Here we catch and display any errors that occur
    #   while TRYing to commit the execute our SQL script.
    try:
        array_row = cur.fetchone()
    except psycopg2.Error as e:
        t_message = "Database error: " + e + "/n SQL: " + s
        return render_template("sign_in.html", message = t_message)

    # Cleanup our database connections
    db_cursor.close()
    db_conn.close()

    ID_user = array_row(0)

    # If they have used the link in the email we sent them then t_stage is "reset"
    if t_stage == "reset":
        # IMPORTANT
        # In a later part of this article series we will add code here
        # IMPORTANT

    # First stage. They have filled in username and password, so t_stage is "login"
    if t_stage == "login":
        # UPDATE the database with a logging of the date of the visit
        s = ""
        s += "UPDATE users SET"
        s += " d_visit_last = '" & now() & "'"
        s += "WHERE"
        s += "("
        s += " ID=" + ID_user
        s += ")"
        # IMPORTANT WARNING: this format allows for a user to try to insert
        #   potentially damaging code, commonly known as "SQL injection".
        #   In a later article we will show some methods for
        #   preventing this.

        # Here we are catching and displaying any errors that occur
        #   while TRYing to commit the execute our SQL script.
        db_cursor.execute(s)
        try:
            db_conn.commit()
        except psycopg2.Error as e:
            t_message = "Login: Database error: " + e + "/n SQL: " + s
            return render_template("sign_in.html", message = t_message)
        db_cursor.close()

        # Redirect user to the rest of your application
        return redirect("http://your-URL-here", code=302)

    # If they have clicked "Send me a password reset link" then t_stage is "forgot"
    if t_stage == "forgot":
        # IMPORTANT
        # In a later part of this article series we will add code here
        # IMPORTANT

    # If they have used the link in the email we sent them then t_stage is "reset"
    if t_stage == "reset":
        # IMPORTANT
        # In a later part of this article series we will add code here
        # IMPORTANT

# This is for command line testing
if __name__ == "__main__":
    app.run(debug=True)