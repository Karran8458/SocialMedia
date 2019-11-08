from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection
app = Flask(__name__)
app.secret_key = 'keep it safe'
first_name = " "
last_name = " "
email = " "
password = " "
ident = 1
jobid = 4
title = " "
description = " "
address = " "
@app.route("/")
def index():
    return render_template("registration.html")

@app.route('/success', methods=['POST'])
def success():
    global first_name
    global ident
    ident = ident + 1
    fname_for_form = request.form['fname']
    repeat = request.form['psw-repeat']
    if len(fname_for_form) < 3:
        flash("Too short!!!!")
        return redirect("/")
    lname_for_form = request.form['lname']
    if len(lname_for_form) < 3:
        flash("Too short!!!!")
        return redirect("/")
    email_for_form = request.form['email']
    password_for_form = request.form['psw']
    if len(password_for_form) < 8:
        flash("Too short!!!!")
        return redirect("/")
    if len(password_for_form) > 20:
        flash("Too long!!!!")
        return redirect("/")
    if not any(char.isdigit() for char in password_for_form): 
        flash('Password should have at least one numeral') 
        return redirect("/")
    if not any(char.isupper() for char in password_for_form): 
        flash('Password should have at least one uppercase letter') 
        return redirect("/")
    if not any(char.islower() for char in password_for_form): 
        flash('Password should have at least one lowercase letter') 
        return redirect("/")
    if repeat != password_for_form:
        flash('Your password is not confirmed')
        return redirect("/")
    mysql = connectToMySQL('Gundam')
    query = "INSERT INTO user (id, first_name, last_name, email, password) VALUES (%(id)s, %(fn)s, %(ln)s, %(e)s, %(p)s);"
    data = {
    
        "id": ident,
        "fn": request.form['fname'],
        "ln": request.form['lname'],
        "e": request.form['email'],
        "p": request.form['psw']
        
    }
    new_user_id = mysql.query_db(query, data)
    return render_template("show.html", fname_on_template=fname_for_form, lname_on_template=lname_for_form, email_on_template=email_for_form)

@app.route('/login_successful', methods=['POST'])
def successful_login():
    global email
    global password
    global first_name
    global last_name
    global ident
    # see if the username provided exists in the database
    email_for_form = request.form['email']
    psw_for_form = request.form['psw']
    if len(psw_for_form) < 8:
        flash("Too short!!!!")
        return redirect("/")
    if len(psw_for_form) > 20:
        flash("Too long!!!!")
        return redirect("/")
    if not any(char.isdigit() for char in psw_for_form): 
        flash('Password should have at least one numeral') 
        return redirect("/")
    if not any(char.isupper() for char in psw_for_form): 
        flash('Password should have at least one uppercase letter') 
        return redirect("/")
    if not any(char.islower() for char in psw_for_form): 
        flash('Password should have at least one lowercase letter') 
        return redirect("/")
    email = email_for_form
    if email == "kman@bellsouth.net":
        first_name = "Karran"
        last_name = "Gowda"
        ident = 1
    if email == "jaypeterson@gmail.com":
        first_name = "Jay"
        last_name = "Peterson"
        ident = 2
    password = psw_for_form
    mysql = connectToMySQL("Gundam")
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": request.form['email'] 
        
    }
    result = mysql.query_db(query, data)
    if len(result) > 0:
        return render_template('login.html', all_result = result, email_on_template=email_for_form, first_on_template = first_name)
    flash("You could not be logged in")
    return redirect("/login")
    
@app.route('/logout', methods=['POST'])
def logout():
    global email
    global password
    global first_name
    global last_name
    email = " "
    password = " "
    first_name = " "
    last_name = " "
    return render_template("registration.html")

@app.route('/register', methods=['POST'])
def register():
    return render_template("registration.html")

@app.route('/gfighters/list', methods=['POST'])
def list():
    global first_name
    global ident
    mysql = connectToMySQL("Gundam")
    query = "SELECT * FROM user WHERE id!=%(id)s;"
    data = {
    
        "id": ident 
        
    }
    users = mysql.query_db(query, data)
    mysql = connectToMySQL('Gundam')
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": email
        
    }
    result = mysql.query_db(query, data)
    return render_template("list.html", all_results = users, all_friends = result, first_on_template = first_name)

@app.route('/gfighters/wall', methods=['POST'])
def wall():
    global first_name
    global email
    global ident
    mysql = connectToMySQL("Gundam")
    query = "SELECT * FROM privatemessage WHERE user_id=%(y)s;"
    data = {
    
        "y": ident 
        
    }
    users = mysql.query_db(query, data)
    mysql = connectToMySQL('Gundam')
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": email
        
    }
    result = mysql.query_db(query, data)
    mysql = connectToMySQL("Gundam")
    query = "SELECT * FROM privatemessage WHERE user_id!=%(y)s;"
    data = {
    
        "y": ident 
        
    }
    me = mysql.query_db(query, data)
    return render_template("userdashboard.html", all_me = me, all_users = users, all_results = result, first_on_template = first_name)

@app.route('/gfighters/feed', methods=['POST'])
def feed():
    global first_name
    global ident
    global email
    mysql = connectToMySQL('Gundam')
    users = mysql.query_db('SELECT * FROM message;')
    print(users)
    mysql = connectToMySQL('Gundam')
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": email
        
    }
    result = mysql.query_db(query, data)
    return render_template("feed.html", all_users = users, all_results = result, first_on_template = first_name)

@app.route("/gfighters/profileedit", methods=['POST'])
def edit_profile():
    global first_name
    global email
    mysql = connectToMySQL('Gundam')
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": email
        
    }
    friends = mysql.query_db(query, data)
    return render_template("profileedit.html", all_freaks = friends, first_on_template = first_name)

@app.route("/profile")
def profile():
    global first_name
    global email
    global ident
    mysql = connectToMySQL('Gundam')
    query = "UPDATE user SET first_name = %(f)s, last_name = %(l)s, email = %(e)s, password = %(p)s, description = %(d)s WHERE id = %(id)s;"
    data = {
        "id": ident,
        "fn": request.form['fname'],
        "ln": request.form['lname'],
        "e": request.form['email'],
        "p": request.form['psw'],
        "d": request.form['desc']
    }
    new_user = mysql.query_db(query, data)
    mysql = connectToMySQL('Gundam')
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": email
        
    }
    users = mysql.query_db(query, data)
    return render_template("userdashboard.html", all_results = users, first_on_template = first_name)

@app.route("/gfighters/<ide>/profile", methods=["POST"])
def userprofile(ide):
    global first_name
    global email
    global ident
    first = " "
    mysql = connectToMySQL('Gundam')
    query = "SELECT * FROM user WHERE id = %(id)s;"
    data = {
    
        "id": ide
        
    }
    result = mysql.query_db(query, data)
    mysql = connectToMySQL('Gundam')
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": email
        
    }
    friends = mysql.query_db(query, data)
    return render_template("userprofile.html", all_result=result, all_friends = friends, first_on_template = first_name)

@app.route("/gfighters/<ide>/wall", methods=["POST"])
def userwall(ide):
    global first_name
    global email
    global ident
    first = " "
    mysql = connectToMySQL("Gundam")
    query = "SELECT * FROM privatemessage WHERE user_id=%(y)s;"
    data = {
    
        "y": ident 
        
    }
    users = mysql.query_db(query, data)
    mysql = connectToMySQL("Gundam")
    query = "SELECT * FROM privatemessage WHERE user_id!=%(y)s;"
    data = {
    
        "y": ide
        
    }
    me = mysql.query_db(query, data)
    mysql = connectToMySQL("Gundam")
    query = "SELECT * FROM user WHERE id=%(id)s;"
    data = {
    
        "id": ide 
        
    }
    opp = mysql.query_db(query, data)
    mysql = connectToMySQL('Gundam')
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": email
        
    }
    result = mysql.query_db(query, data)
    return render_template("oppodashboard.html", all_opp = opp, all_me = me, all_users = users, all_results = result, first_on_template = first_name)

@app.route("/gfighters/profile", methods=["POST"])
def view_book():
    global first_name
    global email
    global ident
    first = " "
    mysql = connectToMySQL('Gundam')
    query = "SELECT * FROM user WHERE id = %(id)s;"
    data = {
    
        "id": ident
        
    }
    result = mysql.query_db(query, data)
    mysql = connectToMySQL('Gundam')
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": email
        
    }
    friends = mysql.query_db(query, data)
    return render_template("profile.html", all_result=result, all_friends = friends, first_on_template = first_name)

@app.route("/gfighters/<ide>/destroy", methods=["POST"])
def destroy_user(ide):
    global ident
    global name
    global email
    global first_name
    mysql = connectToMySQL('Gundam')
    query = "DELETE FROM privatemessage WHERE id = %(id)s;"
    data = {
    
        "id": ide
    }
    new_user = mysql.query_db(query, data)
    mysql = connectToMySQL("Gundam")
    query = "SELECT * FROM message WHERE user_id=%(y)s;"
    data = {
    
        "y": ident
        
    }
    users = mysql.query_db(query, data)
    mysql = connectToMySQL('Gundam')
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": email
        
    }
    result = mysql.query_db(query, data)
    return render_template("userdashboard.html", all_users = users, all_results = result, first_on_template = first_name)

@app.route('/new', methods=['POST'])
def new_wall():
    global ident
    global jobid
    global email
    jobid = jobid + 1
    dest_for_form = request.form['title']
    if len(dest_for_form) < 3:
        flash("Too short!!!!")
        return redirect('/gfighters/wall')
    plan_for_form = request.form['desc']
    if len(plan_for_form) < 3:
        flash("Too short!!!!")
        return redirect('/gfighters/wall')
    mysql = connectToMySQL('Gundam')	        # call the function, passing in the name of our db
    query = "INSERT INTO privatemessage (id, title, description, created_at, user_id) VALUES (%(id)s, %(t)s, %(d)s, NOW(), %(y)s);"
    data = {
    
        "id": jobid,
        "t": request.form['title'],
        "d": request.form['desc'],
        "y": ident
        
    }
    new_user = mysql.query_db(query, data)
    mysql = connectToMySQL('Gundam')
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": email
        
    }
    result = mysql.query_db(query, data)
    return render_template("login.html", all_result = result, first_on_template = first_name)

@app.route('/new/<ide>/wall', methods=['POST'])
def new_userwall(ide):
    global ident
    global jobid
    global email
    jobid = jobid + 1
    dest_for_form = request.form['title']
    if len(dest_for_form) < 3:
        flash("Too short!!!!")
        return redirect('/gfighters/wall')
    plan_for_form = request.form['desc']
    if len(plan_for_form) < 3:
        flash("Too short!!!!")
        return redirect('/gfighters/wall')
    mysql = connectToMySQL('Gundam')	        # call the function, passing in the name of our db
    query = "INSERT INTO privatemessage (id, title, description, created_at, user_id) VALUES (%(id)s, %(t)s, %(d)s, NOW(), %(y)s);"
    data = {
    
        "id": jobid,
        "t": request.form['title'],
        "d": request.form['desc'],
        "y": ide
        
    }
    new_user = mysql.query_db(query, data)
    mysql = connectToMySQL('Gundam')
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": email
        
    }
    result = mysql.query_db(query, data)
    return render_template("login.html", all_result = result, first_on_template = first_name)

@app.route('/newfeed', methods=['POST'])
def new_feed():
    global ident
    global jobid
    global email
    jobid = jobid + 1
    dest_for_form = request.form['title']
    if len(dest_for_form) < 3:
        flash("Too short!!!!")
        return redirect('/gfighters/wall')
    plan_for_form = request.form['desc']
    if len(plan_for_form) < 3:
        flash("Too short!!!!")
        return redirect('/gfighters/wall')
    mysql = connectToMySQL('Gundam')	        # call the function, passing in the name of our db
    query = "INSERT INTO message (id, title, description, created_at, user_id) VALUES (%(id)s, %(t)s, %(d)s, NOW(), %(y)s);"
    data = {
    
        "id": jobid,
        "t": request.form['title'],
        "d": request.form['desc'],
        "y": ident
        
    }
    new_user = mysql.query_db(query, data)
    mysql = connectToMySQL('Gundam')
    users = mysql.query_db('SELECT * FROM message;')
    print(users)
    mysql = connectToMySQL('Gundam')
    query = "SELECT * FROM user WHERE email = %(e)s;"
    data = {
    
        "e": email
        
    }
    result = mysql.query_db(query, data)
    return render_template("feed.html", all_users = users, all_results = result, first_on_template = first_name)

@app.route('/home', methods=['POST'])
def home():
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
