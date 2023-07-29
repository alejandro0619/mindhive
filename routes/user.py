from flask import redirect, render_template, url_for, request, session, Blueprint, current_app, request
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import date, datetime
import re
import hashlib

from lib.shareable_code import gen_shareable_code
from lib.query_dispatcher import dispatcher

user_bp = Blueprint("user", __name__)
messages = []


@user_bp.route('/')
def root():
    return redirect(url_for("user.dashboard", by = 1))
    
@user_bp.route("/dashboard/filter", methods=['GET', 'POST'])
def dashboard():
    # We import the current instance of mysql and create a cursor instance
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Filters labels and the filter type by through the request
    filters_labels = ['Todos', 'Creados', 'Fecha inicio', 'Fecha de cierre']
    filter_type = int(request.args['by'])
    query = dispatcher(filter_type)

    # Project joining message
    project_joining_message = request.args.get('msg', '')
    # If request method is post, redirect to logout
    if request.method == "POST":
        return redirect(url_for("auth.logout"))

    # if request is get, check if the user is logged in to show home.html, otherwise, redirect to login
    elif request.method == "GET":
        if "loggedin" in session:

            cursor.execute(query, (session["uid"],))
            projects = [project for project in cursor.fetchall()]
            for project in projects:
                project_id = project['project_id']
                count_query = "SELECT COUNT(User_uid) AS participant_count FROM user_has_project WHERE Project_project_id = %s"
                cursor.execute(count_query, (project_id,))
                participant_count = cursor.fetchone()['participant_count']
                project['participant_count'] = participant_count
            print(projects)
            return render_template("projectList.html", projects=projects, filter = filters_labels[filter_type - 1], msg = project_joining_message)

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
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":
        # Query that gathers the shareable codes from all the projects
        get_shareable_code_query = """
        SELECT shareable_code from project
        """
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
        

        create_project_query = """
        INSERT INTO project VALUES (NULL, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(create_project_query, (project_title, project_description, starting_date, ending_date, shareable_code, user_uid))

        insert_into_user_has_project = """
        INSERT INTO user_has_project VALUES (%s, %s)
        """
        project_id = cursor.lastrowid
        cursor.execute(insert_into_user_has_project, (user_uid, project_id))
        mysql.connection.commit()
        return redirect(url_for("user.dashboard", by=1))
    elif request.method == "GET":
        if 'loggedin' in session: 
            return render_template("projectCreate.html", route = "createProject", project_id  = "", title_label = "Creación", button_label = 'Crear proyecto')
        else: 
            return redirect(url_for("auth.login"))

@user_bp.route("/editProject/<id>", methods=['GET', 'POST'])
def edit_project(id):
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        if 'loggedin' in session:
            project_title = request.form['tituloProyecto']
            project_description = request.form["descripcionProyecto"]
            starting_date = datetime.strptime(request.form['fechaInicioProyecto'], "%Y-%m-%d")
            ending_date = datetime.strptime(request.form["fechaCierreProyecto"], "%Y-%m-%d")

            query = """
            UPDATE project
            SET project_title = %s,
                project_description = %s,
                starting_date = %s,
                ending_date = %s
            WHERE project_id = %s
            """
            cursor.execute(query, (project_title, project_description, starting_date, ending_date, id))
            mysql.connection.commit()
            return redirect(url_for('user.root'))

    elif request.method == 'GET':
        uid = session['uid']
        query = "SELECT User_project_creator from project where project_id = %s"
        cursor.execute(query, (id, ))
        project_creator_id = cursor.fetchone()

        if (str(project_creator_id['User_project_creator']) == str(uid)):
            return render_template("projectCreate.html", route = "editProject", project_id = '/' + id, title_label = "Edición", button_label = 'Editar proyecto')
        else:
            return redirect(url_for('user.root'))
        
@user_bp.route("/deleteAnnouncement/<id>", methods=['GET'])
def delete_announcement(id):
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    get_announcement_creator = "SELECT User_uid as creator, project_project_id as project from announcement where announcement_id = %s" 
    cursor.execute(get_announcement_creator, (id,))
    announcement_creator_id = cursor.fetchone()
    project = announcement_creator_id['project']

    if announcement_creator_id['creator'] != session['uid']:
        return redirect(url_for("user.root"))
    else:

        query = "DELETE FROM announcement WHERE announcement_id = %s"
        cursor.execute(query, (id,))
        mysql.connection.commit()
        return redirect(url_for("user.project_view", id=project))
    
@user_bp.route("/editAnnouncement/<project_id>/<id>", methods=['GET', 'POST'])
def edit_announcement(project_id, id):
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    get_project = 'SELECT * from project where project_id = %s'
    cursor.execute(get_project, (project_id,))
    project = cursor.fetchone()


    if request.method == 'POST':
        if 'loggedin' in session:
            announcement_title = request.form['tituloAnuncio']
            announcement_description = request.form["descripcionAnuncio"]

            query = """
            UPDATE announcement
            SET announcement_name = %s,
                announcement_description = %s
            WHERE announcement_id = %s
            """
            cursor.execute(query, (announcement_title, announcement_description, id))
            mysql.connection.commit()
            return redirect(url_for('user.project_view', id=project_id))

    elif request.method == 'GET':
        uid = session['uid']
        query = "SELECT User_uid from announcement where announcement_id = %s"
        cursor.execute(query, (id, ))
        announcement_creator_id = cursor.fetchone()

        if (str(announcement_creator_id['User_uid']) == str(uid)):
            return render_template("announcementCreate.html",project=project, route = "editAnnouncement", announcement_id = '/' + id, title_label = "Edición", button_label = 'Editar')
        else:
            return redirect(url_for('user.root'))
        
@user_bp.route("/deleteProject/<id>", methods=['GET'])
def delete_project(id):
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    get_project_creator = "SELECT User_project_creator as creator from project where project_id = %s" 
    cursor.execute(get_project_creator, (id,))
    project_creator_id = cursor.fetchone()

    if project_creator_id['creator'] != session['uid']:
        return redirect(url_for("user.root"))
    else:
        cursor.execute("DELETE FROM user_has_project WHERE Project_project_id = %s",(id,))
        cursor.execute("DELETE FROM activity WHERE  Project_project_id = %s", (id,))
        cursor.execute("DELETE FROM announcement WHERE Proje")
        query = "DELETE FROM project WHERE project_id = %s"
        cursor.execute(query, (id,))
        mysql.connection.commit()
        return redirect(url_for("user.root"))

        
@user_bp.route("/leaveProject/<id>", methods=['GET'])
def leave_project(id):
   
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    uid = session['uid']
    # check if the user is not the creator of the project
    query_check_user = "SELECT User_project_creator FROM project WHERE project_id = %s"
    cursor.execute(query_check_user, (id,))
    creator = cursor.fetchone()

    if creator['User_project_creator'] != uid:
        query = "DELETE FROM user_has_project WHERE User_uid = %s AND Project_project_id = %s"
        cursor.execute(query, (uid, id,))
        mysql.connection.commit()
        

        messages.append("Se ha salido del proyecto exitosamente")
        return redirect(url_for("user.root"))
    else:
        # socket.emit('show_notification', "Eres el creador del proyecto, no puedes salir.")
        messages.append("Eres el creador del proyecto, no puedes salir")
        return redirect(url_for("user.root"))
    

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

            #If the query finds a project, then another query will be executed to check whether the user is already in that project or not
            check_user_in_project = """
            SELECT User_uid FROM user_has_project WHERE Project_project_id = %s AND User_uid = %s
            """

            cursor.execute(check_user_in_project, (project_id_query_result['project_id'], session["uid"],))
            user_in_project_result = cursor.fetchone()

            #if the user is already in that project, then it won't try to insert the same user two times into a project
            if user_in_project_result:
                msg="Ya estás en este proyecto"

            else:
                join_project_query = """INSERT INTO user_has_project VALUES (%s,%s)"""
                cursor.execute(join_project_query, (user_uid, project_id_query_result['project_id'],))
                mysql.connection.commit()
                msg="Te uniste al projecto"
            
        else:
            msg="Proyecto no encontrado"
        # Redirect to the dashboard filtering by all projects by default and sending the resulting message when tried to join to a project
        return redirect(url_for("user.dashboard", by = 1, msg = msg))

@user_bp.route("/viewProject/<id>", methods=['GET'])
def project_view(id):
    if request.method == 'GET':
        if 'loggedin' in session: 
            query = """
            SELECT * FROM project WHERE project_id = %s
            """
            mysql = current_app.config['MYSQL']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query, (id,))
            project = cursor.fetchone()
            

            project_activities="""
            SELECT activity.activity_name, activity.activity_id FROM activity WHERE Project_project_id = %s  
              """
            cursor.execute(project_activities, (id,))
            activities = [activity for activity in cursor.fetchall()]

        # Rest of the code

            project_announcements= """
            SELECT announcement.announcement_name, announcement.announcement_id, announcement.announcement_description, announcement.announcement_date, user.uid, user.user_name FROM announcement JOIN user on user.uid = announcement.user_uid WHERE Project_project_id = %s 
              """
            cursor.execute(project_announcements, (id,))
            announcements = [announcement for announcement in cursor.fetchall()]

            project_participants = """
            SELECT user.user_name, user_has_project.user_uid FROM user_has_project JOIN user ON user.uid = user_has_project.User_uid WHERE user_has_project.Project_project_id = %s
              """
            cursor.execute(project_participants, (id,))
            participants = [user_has_project for user_has_project in cursor.fetchall()]
            # print(activities)
            # print(announcements)
            # print(participants)

            return render_template("project.html", project_id = id, project = project, activities = activities, announcements = announcements, participants=participants)
        else:
            return redirect(url_for("auth.login"))
        

@user_bp.route("/activity/<id>", methods=['GET', 'POST'])
def create_activity(id):
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
            SELECT * FROM project WHERE project_id = %s
            """
    cursor.execute(query, (id,))
    project = cursor.fetchone()

    if request.method == "POST":
        activity_title = request.form['tituloActividad']
        activity_insert = """
        INSERT INTO activity VALUES (NULL, %s, %s, 0)
        """
        cursor.execute(activity_insert, (activity_title, id,))

        mysql.connection.commit()
        return redirect(url_for('user.project_view', id=id))     

    elif request.method == 'GET':
        if "loggedin" in session:
            return render_template("activityCreate.html", route = "activity", project_id = id,  project = project, activity_name = "Nombre de la actividad", activity_id = '')
        else:
             return redirect(url_for("auth.login"))
    
@user_bp.route("/editActivity/<project_id>/<id>", methods=['GET','POST'])
def edit_activity(project_id, id):
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
            SELECT * FROM project WHERE project_id = %s
            """
    cursor.execute(query, (project_id,))
    project = cursor.fetchone()

    if request.method == "POST":
        activity_title = request.form['tituloActividad']
        activity_update = """
        UPDATE activity
        SET activity_name = %s
        WHERE activity_id = %s
        """
        cursor.execute(activity_update, (activity_title, id,))

        mysql.connection.commit()

        return redirect(url_for('user.project_view', id = project_id)) 

    elif request.method == "GET":
        if "loggedin" in session:
            query_retrieve_activity_title = "SELECT activity_name FROM activity WHERE activity_id = %s"
            cursor.execute(query_retrieve_activity_title, (id, ))
            activity = cursor.fetchone()
            return render_template("activityCreate.html", route = "editActivity", project_id =  project_id,  project = project, activity_name =  activity['activity_name'], activity_id = '/' + id)
    else: 
        return redirect(url_for('auth.login'))
    
@user_bp.route("/deleteActivity/<project_id>/<id>", methods =['GET'])
def delete_activity(project_id, id):
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
            SELECT * FROM project WHERE project_id = %s
            """
    cursor.execute(query, (project_id,))
    project = cursor.fetchone()

    if "loggedin" in session:

        if request.method == "GET":
            activity_delete = """
            DELETE FROM activity
            WHERE activity_id = %s
            """
            cursor.execute(activity_delete, ( id,))
            mysql.connection.commit()

            return redirect(url_for('user.project_view', id = project_id)) 

    else: 
        return redirect(url_for('auth.login'))

@user_bp.route("/createAnnouncement/<id>", methods=['GET', 'POST'])
def create_announcement(id):
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
            SELECT * FROM project WHERE project_id = %s
            """
    cursor.execute(query, (id,))
    project = cursor.fetchone()

    if request.method == "POST":
        announcement_title = request.form['tituloAnuncio']
        announcement_description = request.form['descripcionAnuncio']

        announcement_insert = """
        INSERT INTO announcement VALUES (NULL, %s, %s, NULL, %s, %s)
        """
        cursor.execute(announcement_insert, (announcement_title, announcement_description, session['uid'], id))
        test = cursor.fetchall()
        mysql.connection.commit()
        return redirect(url_for('user.project_view', id=id))     

    elif request.method == 'GET':
        if "loggedin" in session:           
            return render_template("announcementCreate.html", project_id = id,  project = project , route = "createAnnouncement", title_label = "Creación", button_label = 'Crear')
        else:
             return redirect(url_for("auth.login"))
            

@user_bp.route("/shareCode/<id>", methods=['GET'])
def share_code(id):
    mysql = current_app.config['MYSQL']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
            SELECT * FROM project WHERE project_id = %s
            """
    cursor.execute(query, (id,))
    project = cursor.fetchone()

    if request.method == 'GET':
        if "loggedin" in session:           
            return render_template("addMember.html", project_id = id,  project = project)
        else:
             return redirect(url_for("auth.login"))
        
@user_bp.route("/projectAnnouncement/<id>", methods=['GET', 'POST'])
def announcement(id):
     if request.method == 'POST':
        mysql = current_app.config['MYSQL']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        commentary = request.form['comentario']
        insert_comment = '''
         INSERT INTO comment VALUES (NULL, %s, NULL, %s, %s )            
        ''' 
        query = """
                    SELECT announcement.announcement_id, announcement.announcement_name, announcement.announcement_description, announcement.announcement_Date, User.uid, User.user_name, announcement.project_project_id FROM announcement JOIN user ON user.uid = announcement.user_uid WHERE announcement_id = %s
                """
        cursor.execute(query, (id,))
        announcement = cursor.fetchone()
        
        cursor.execute(insert_comment, (commentary, session['uid'], announcement['announcement_id'],))   
        mysql.connection.commit()
        comment_query = """
            SELECT comment.comment_id, comment_content, comment.comment_date, comment.User_uid, user.user_name  FROM comment JOIN user ON user.uid = comment.User_uid WHERE comment.Announcement_announcement_id = %s;
            """
        cursor.execute(comment_query, (announcement['announcement_id'],))
        comments = [comment for comment in cursor.fetchall()]
    
        return render_template("announcement.html", announcement = announcement, comments=comments, id=id)

     elif request.method == 'GET':
        if "loggedin" in session: 
            mysql = current_app.config['MYSQL']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = """
                    SELECT announcement.announcement_id, announcement.announcement_name, announcement.announcement_description, announcement.announcement_Date, User.uid, User.user_name, announcement.project_project_id FROM announcement JOIN user ON user.uid = announcement.user_uid WHERE announcement_id = %s
                    """
            cursor.execute(query, (id,))
            announcement = cursor.fetchone()

            comment_query = """
            SELECT comment.comment_id, comment_content, comment.comment_date, comment.User_uid, user.user_name  FROM comment JOIN user ON user.uid = comment.User_uid WHERE comment.Announcement_announcement_id = %s;
            """
            cursor.execute(comment_query, (announcement['announcement_id'],))
            comments = [comment for comment in cursor.fetchall()]

            
            return render_template("announcement.html", announcement = announcement, comments=comments, id=id)
        else:
            return redirect(url_for("auth.login"))
            return redirect(url_for("auth.login"))
