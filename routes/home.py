from flask import Blueprint, redirect, url_for, render_template

home_bp = Blueprint("home", __name__)

@home_bp.get("/")
def home():
  return render_template('/projectList.html') # need to change it later

@home_bp.route("/dash", methods = ('GET', 'POST'))
def dashboard():
  print("need to finish")
