from flask import Flask, redirect, render_template, url_for, request, session
from flask_mysqldb import MySQL
from routes.auth import auth_bp
from routes.home import home_bp
import MySQLdb.cursors
import MySQLdb.cursors
import re
import hashlib
from datetime import date
app = Flask(__name__)

app.secret_key = 'arremangala arrepuj ala sí, arremangala arrepujala no'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mindhive'
app.config['MYSQL_UNIX_SOCKET'] = '/opt/lampp/var/mysql/mysql.sock'

app.config['MYSQL'] = MySQL(app)

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)

# @app.route("/logout")
# def logout():
#     # Logout endpoint that logs the user out and redirects it to login page
#     session.pop("loggedin", None)
#     session.pop('uid', None)
#     session.pop('email', None)
#     session.pop("user_name", None)
#     return redirect(url_for("login"))


# @app.route("/home", methods=['GET', 'POST'])
# def homePage():
#     # If request method is post, redirect to logout
#     if request.method == "POST":
#         return redirect(url_for("logout"))
#     # if request is get, check if the user is logged in to show home.html, otherwise, redirect to login
#     elif request.method == "GET":
#         if "loggedin" in session:
#             cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

#             query = """
#                 SELECT *
#                 FROM project
#                 INNER JOIN user_has_project ON project.project_id = user_has_project.Project_project_id
#                 INNER JOIN user ON project.User_project_creator = user.uid
#                 WHERE user_has_project.User_uid = %s
#                 GROUP BY project.project_id, project.project_title
#                 """

#             cursor.execute(query, (session["uid"],))
#             projects = [project for project in cursor.fetchall()]

#             for project in projects:
#                 project_id = project['project_id']
#                 count_query = "SELECT COUNT(User_uid) AS participant_count FROM user_has_project WHERE Project_project_id = %s"
#                 cursor.execute(count_query, (project_id,))
#                 participant_count = cursor.fetchone()['participant_count']
#                 project['participant_count'] = participant_count

#             print(projects)
#             return render_template("projectList.html", projects=projects)

#         else:
#             return redirect(url_for("login"))


# @app.route("/profile", methods=['GET', 'POST'])
# def ProfileView():
#     if request.method == "GET":
#         return render_template("profile.html")


# @app.route("/createProject", methods=['GET', 'POST'])
# def CreateView():
#     if request.method == "GET":
#         return render_template("projectCreate.html")


if __name__ == '__main__':
    app.run(debug=True)
