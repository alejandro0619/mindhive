from flask import redirect, render_template, url_for, request, session, Blueprint, current_app
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import date

user_bp = Blueprint("user", __name__)

@user_bp.route('/')
def root():
    return redirect(url_for("user.dashboard"))

@user_bp.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    mysql = current_app.config['MYSQL']
    # If request method is post, redirect to logout
    if request.method == "POST":
        return redirect(url_for("auth.logout"))
    # if request is get, check if the user is logged in to show home.html, otherwise, redirect to login
    elif request.method == "GET":
        if "loggedin" in session:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            query = """
                SELECT *
                FROM project
                INNER JOIN user_has_project ON project.project_id = user_has_project.Project_project_id
                INNER JOIN user ON project.User_project_creator = user.uid
                WHERE user_has_project.User_uid = %s
                GROUP BY project.project_id, project.project_title
                """

            cursor.execute(query, (session["uid"],))
            projects = [project for project in cursor.fetchall()]

            for project in projects:
                project_id = project['project_id']
                count_query = "SELECT COUNT(User_uid) AS participant_count FROM user_has_project WHERE Project_project_id = %s"
                cursor.execute(count_query, (project_id,))
                participant_count = cursor.fetchone()['participant_count']
                project['participant_count'] = participant_count

            print(projects)
            return render_template("projectList.html", projects=projects)

        else:
            return redirect(url_for("auth.login"))

@user_bp.route("/profile", methods=['GET', 'POST'])
def ProfileView():
    if request.method == "GET":
        return render_template("profile.html")

@user_bp.route("/createProject", methods=['GET', 'POST'])
def CreateView():
    if request.method == "GET":
        return render_template("projectCreate.html")
