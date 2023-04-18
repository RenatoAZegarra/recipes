from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.user_model import User

@app.route( "/", methods=["GET"] )
def display_login_registration():
    return render_template( "index.html" )

@app.route( "/user/new", methods=["POST"] )
def create_user():
    if User.validate_user( request.form ) == False:
        return redirect( "/" )
    encrypted_password = User.encrypt_string( request.form["password"] )
    data = {
        **request.form,
        "password" : encrypted_password
    }
    user_id = User.create_one( data )
    session["user_id"] = user_id
    session["full_name"] = request.form["first_name"] + " " + request.form["last_name"]
    return redirect( "/recipes" )

@app.route( "/login", methods=["POST"] )
def proccess_login():
    current_user = User.get_one( request.form )
    if current_user == None:
        flash( "This email doesn't exists in our DB.", "error_login_email" )
        return redirect( "/" )
    if User.validate_password( request.form["password"], current_user.password ) == False:
        return redirect( "/" )
    session["user_id"] = current_user.id
    session["full_name"] = current_user.first_name + " " + current_user.last_name
    return redirect( "/recipes" ) 