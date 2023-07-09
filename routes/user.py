from flask import redirect, render_template, url_for, request, session, Blueprint, current_app, request
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import date, datetime
import re
import hashlib

from lib.shareable_code import gen_shareable_code
from lib.query_dispatcher import dispatcher

user_bp = Blueprint("user", __name__)

@user_bp.route('/')
def root():
    return redirect(url_for("user.dashboard", by = 1))

@user_bp.route("/dashboard/filter", methods=['GET', 'POST'])
def dashboard():
    mysql = current_app.config['MYSQL']
    # If request method is post, redirect to logout
    if request.method == "POST":
        return redirect(url_for("auth.logout"))
    # if request is get, check if the user is logged in to show home.html, otherwise, redirect to login
    elif request.method == "GET":
        if "loggedin" in session:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = dispatcher(int(request.args['by']))
            cursor.execute(query, (session["uid"],))
            projects = [project for project in cursor.fetchall()]
            for project in projects:
                project_id = project['project_id']
                count_query = "SELECT COUNT(User_uid) AS participant_count FROM user_has_project WHERE Project_project_id = %s"
                cursor.execute(count_query, (project_id,))
                participant_count = cursor.fetchone()['participant_count']
                project['participant_count'] = participant_count
            return render_template("projectList.html", projects=projects)

        else:
            return redirect(url_for("auth.login"))

@user_bp.route("/profile", methods=['GET', 'POST'])
def profile_view():
    msg = ""
    mysql = current_app.config['MYSQL']
    if request.method == "POST":
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

        # If password fields are not empty, perform password verificatio
        if password and newPassword and confirmarNewPassword:
            # Verify the current password
            hash = password + current_app.secret_key
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
                hash = newPassword + current_app.secret_key
                hash = hashlib.sha1(hash.encode())
                newPassword = hash.hexdigest()
                cursor.execute(
                    """UPDATE user SET password_hash = %s
                    WHERE uid = %s;""",
                    (newPassword, session["uid"])
                )
                mysql.connection.commit()

            return redirect(url_for("auth.logout"))
    if request.method == "GET":
        if "loggedin" in session:
            return render_template("profile.html", msg=msg)
        else:
            return redirect(url_for("auth.login"))

    return render_template("profile.html", msg=msg)

@user_bp.route("/createProject", methods=['GET', 'POST'])
def create_project_view():
    mysql = current_app.config['MYSQL']
    
    if request.method == "POST":
        # Query that gathers the shareable codes from all the projects
        get_shareable_code_query = """
        SELECT shareable_code from project
        """

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(get_shareable_code_query)
        # We turn the array of dicts into a array of just the shareable codes
        codes = [code['shareable_code'] for code in cursor.fetchall()]
        # Retrieves the information from the form
        project_title = request.form['tituloProyecto']
        project_description = request.form["descripcionProyecto"]
        starting_date = datetime.strptime(request.form['fechaInicioProyecto'], "%Y-%m-%d")
        ending_date = datetime.strptime(request.form["fechaCierreProyecto"], "%Y-%m-%d")
        
        # User info
        user_uid = session['uid']

        # We generate the shareable code as long as the code already exists
        shareable_code = gen_shareable_code()
        if codes:
            while shareable_code in codes:
                shareable_code = gen_shareable_code()
        # Once the information needed to create the project is filled. I need to create a group chat for this project 
        create_group_chat_query = """
        INSERT INTO group_chat VALUES (NULL)
        """
        cursor.execute(create_group_chat_query)
        # This is potentially dangerous in case of multiple requests at the same time. Because there's no way to relate the last row to the user that's requesting the ID. This all depends on the order of the operations.
        group_chat_id = cursor.lastrowid

        create_project_query = """
        INSERT INTO project VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(create_project_query, (project_title, project_description, starting_date, ending_date, shareable_code, user_uid, group_chat_id))

        insert_into_user_has_project = """
        INSERT INTO user_has_project VALUES (%s, %s)
        """
        project_id = cursor.lastrowid
        cursor.execute(insert_into_user_has_project, (user_uid, project_id))
        mysql.connection.commit()

    elif request.method == "GET":
        return render_template("projectCreate.html")
    return redirect(url_for('user.root'))

@user_bp.route('/adduser', methods=['POST'])
def add_member():
    if request.method == "POST":
        mysql = current_app.config['MYSQL']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        user_uid = session["uid"]
        shareable_code = request.form['joinProject']

        obtain_project_id_query = """
        SELECT project_id FROM project WHERE shareable_code = %s
        """
        cursor.execute(obtain_project_id_query, (shareable_code,))

        project_id_query_result = cursor.fetchone()

        if project_id_query_result:
            join_project_query = """INSERT INTO user_has_project VALUES (%s,%s)"""
            cursor.execute(join_project_query, (user_uid, project_id_query_result['project_id'],))
            mysql.connection.commit()
            msg="Te uniste al projecto"
        else:
            msg="El codigo ingreso no existe para ningún proyecto actual"
        return redirect(url_for("user.root"))

@user_bp.route("/viewProject/<id>", methods=['GET'])
def project_view(id):
    return render_template("project.html", project_id = id)