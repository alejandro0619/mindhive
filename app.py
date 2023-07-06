from flask import Flask, redirect, render_template, url_for, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import pymysql
import MySQLdb.cursors, re, hashlib
from datetime import date
app = Flask(__name__)

app.secret_key = 'arremangala arrepujala sí, arremangala arrepujala no'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mindhive'

# Initialize MySQL
mysql = MySQL(app)

@app.route("/")
def route():
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    
    msg = ''
    #check if user is logged in to redirect to homepage
    if "loggedin" in session: 
        return redirect(url_for("homePage"))
    # Check if username and password fields exist in the form
    elif request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Variables creation
        username = request.form['username']
        password = request.form['password']

        #Password Hashing
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        # Attempt to log-in
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = %s AND password_hash = %s', (username, password,))
        
        account = cursor.fetchone()
        # If account exists in db
        if account:
            # Creates session data
            session['loggedin'] = True
            session['uid'] = account['uid']
            session['email'] = account['email']
            session["user_name"] = account["user_name"]
            session["password"] = password
            return redirect(url_for('homePage'))
        else:
            # Log-in failure
            msg = 'Email o contraseña incorrectas'
    return render_template('/auth/login.html', msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    #check if user is logged in to redirect to homepage
    if "loggedin" in session: 
        return redirect(url_for("homePage"))

    # Check if required fields exist in the form
    elif request.method == 'POST' and all(field in request.form for field in ['email', 'nombre', 'apellido', 'password', 'confirmarPassword']):  
        # Variables creation
        email = request.form['email']
        nombre = request.form["nombre"]+" "+request.form["apellido"]
        password = request.form['password']
        confirmarPassword = request.form["confirmarPassword"]
        fechaCreacion = date.today()
        
          # Check if a user already exists with that email
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        account = cursor.fetchone()
        #If email is already in use
        if account:
            msg = 'Este email ya está en uso'
        #If email fails regex verification
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Dirección e-mail inválida'
        #If form hasn't been completely filled
        elif not email or not nombre or not password or not confirmarPassword:
            msg = 'Llena todos los campos'
        #If password confirmation fails
        elif password != confirmarPassword:
            msg = "La contraseñas no coinciden"
        else:
            # Password hashing
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()
            # Database tuple insertion
            cursor.execute('INSERT INTO user VALUES (NULL, %s, %s, %s, %s)', (nombre, email, password, fechaCreacion))
            mysql.connection.commit()
            msg = 'Usuario registrado exitosamente'
    elif request.method == "POST":   
           msg = 'Llena todos los campos'
    return render_template('/auth/register.html', msg=msg)

@app.route("/logout")
def logout():
    #Logout endpoint that logs the user out and redirects it to login page
    session.pop("loggedin", None)
    session.pop ('uid', None)
    session.pop ('email', None)
    session.pop ("user_name", None)
    session.pop ("password", None)
    return redirect(url_for("login"))

@app.route("/home", methods=['GET', 'POST'])
def homePage():
    #If request method is post, redirect to logout
    if request.method == "POST":  
        return redirect(url_for("logout"))
    #if request is get, check if the user is logged in to show home.html, otherwise, redirect to login
    elif request.method == "GET":
        if "loggedin" in session: 
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
                SELECT *
                FROM project
                INNER JOIN User_has_project ON project.project_id = User_has_project.Project_project_id
                INNER JOIN user ON project.User_project_creator = user.uid
                WHERE User_has_project.User_uid = %s
                GROUP BY project.project_id, project.project_title
                """
            
            cursor.execute(query, (session["uid"],))
            projects = [project for project in cursor.fetchall()]
            

            for project in projects:
                project_id = project['project_id']  
                count_query = "SELECT COUNT(User_uid) AS participant_count FROM User_has_project WHERE Project_project_id = %s"
                cursor.execute(count_query, (project_id,))
                participant_count = cursor.fetchone()['participant_count']
                project['participant_count'] = participant_count

            print(projects)
            return render_template("projectList.html", projects=projects)

        else:
            return redirect(url_for("login"))

@app.route("/profile", methods=['GET', 'POST'])
def ProfileView():
    msg = ""

    if request.method == "POST":
        # Variable creation
        email = request.form['email']
        nombre = request.form["nombre"]
        password = request.form['password']
        newPassword = request.form["newPassword"]
        confirmarNewPassword = request.form["confirmarNewPassword"]

        # Check if the email has already been taken by another user
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        account = cursor.fetchone()

        # If email is already in use by a different user
        if account and account['uid'] != session['uid']:
            msg = 'Este email ya está en uso'
        # If email fails regex verification
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Dirección e-mail inválida'

        # Fetch the password from the database if not found in session
        if 'password' not in session:
            cursor.execute('SELECT password_hash FROM user WHERE uid = %s', (session['uid'],))
            password_hash = cursor.fetchone()
            if password_hash:
                session['password'] = password_hash['password_hash']

        # If password fields are not empty, perform password verification
        if password or newPassword or confirmarNewPassword:
            # Verify the current password
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()
            if password != session["password"]:
                msg = "La contraseña actual es incorrecta"
            # Verify the new password and confirmation
            elif newPassword != confirmarNewPassword:
                msg = "Las contraseñas no coinciden"

        # If there are no validation errors, update the user information
        if not msg:
            cursor.execute(
                """UPDATE user SET user_name = %s, email = %s
                WHERE uid = %s;""",
                (nombre, email, session["uid"])
            )
            mysql.connection.commit()

            # Update the session data with the new values
            session["user_name"] = nombre
            session["email"] = email

            if newPassword:
                # Update the password if a new password is provided
                hash = newPassword + app.secret_key
                hash = hashlib.sha1(hash.encode())
                newPassword = hash.hexdigest()
                cursor.execute(
                    """UPDATE user SET password_hash = %s
                    WHERE uid = %s;""",
                    (newPassword, session["uid"])
                )
                mysql.connection.commit()

            msg = "Edición satisfactoria"
            session.pop("loggedin", None)
            session.pop ('uid', None)
            session.pop ('email', None)
            session.pop ("user_name", None)
            session.pop ("password", None)
            return redirect(url_for("login"))

    if request.method == "GET":
        if "loggedin" in session:
            return render_template("profile.html", msg=msg)
        else:
            return redirect(url_for("login"))

    return render_template("profile.html", msg=msg)



        

@app.route("/createProject", methods=['GET', 'POST'])
def CreateView():
    if request.method == "GET":
        return render_template("projectCreate.html")

if __name__ == '__main__':
    app.run(debug=True)