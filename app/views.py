import os, datetime

from flask import json

from app import app, login_manager
from app import models
from flask import render_template, request, redirect, jsonify,url_for,flash,session
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from .forms import LoginForm,NewUserForm,AddNewCarForm
from flask.json import jsonify
from flask_login import login_user, login_user, current_user, login_required
from flask_jwt_extended import jwt_required, create_access_token
from app import db
from app.models import Cars, Favourites, Users
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import exc
from app.config import *


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    form = NewUserForm()
    uploadFolder = app.config['UPLOAD_FOLDER']

    if request.method == "POST" and form.validate_on_submit():

        try: 
            username = form.username.data
            password = form.password.data
            fullname = form.fullname.data
            email = form.email.data
            location = form.location.data
            biography = form.biography.data
            date_joined = str(datetime.date.today())

            photo = form.photo.data 
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(uploadFolder,filename))
        
            newUser = Users(username=username,password=password,fullname=fullname, email=email,location=location,biography=biography,photo=filename, date_joined=date_joined)
            print(newUser)

            db.session.add(newUser)
            db.session.commit()
            print(newUser)
            return jsonify(message="Success! New user was added!")

        except Exception as exc:
            db.session.rollback()
            print(exc)
            return jsonify(errors=["Error!"])
    return jsonify(errors=form_errors(form))

            

        #takenUsername = Users.query.filter_by(username=username).first()
        #takenEmail = Users.query.filter_by(email=email).first()
        
            


        #if takenUsername is not None: 
        #    return jsonify(errors= ["Username not available"])
        #elif takenEmail is not None:
        #    return jsonify(errors= ["Email address not available"])

    
        
    

@app.route('/api/auth/login', methods=['POST'])

def login():
    try:
        form = LoginForm()
        if form.validate_on_submit():
            username = request.json['username']
            password = request.json['password']
            print(username, password)
            user = Users.query.filter_by(username=username).first()
            if user is not None and check_password_hash(user.password, password):

                return jsonify('success')
            else:
                return jsonify(errors={'message': ["Username or Password is incorrect"]}), 422
        else:
            errors = form_errors(form)
            return jsonify(errors={'message': errors}), 422
    except Exception as exc:
        print(exc)
        return jsonify('error'), 422

@app.route('/api/auth/logout', methods = ['GET'])
@jwt_required
def logout():
    return jsonify(message= "User successfully logged out.")
    


def form_errors(form):
    error_messages = []
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                getattr(form, field).label.text, error)
            error_messages.append(message)
    return error_messages


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
