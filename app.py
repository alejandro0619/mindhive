from flask import Flask, redirect, render_template, url_for, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
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
                JOIN User_has_project ON project.project_id = User_has_project.Project_project_id
                JOIN user ON project.User_project_creator = user.uid
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

if __name__ == '__main__':
    app.run(debug=True)