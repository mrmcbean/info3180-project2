import os

from flask import json

from app import app
from flask import render_template, request, redirect, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from app.forms import LoginForm , NewUserForm , AddNewCarForm
from flask.json import jsonify
from flask_login import login_user, login_user, current_user, login_required
from flask_jwt_extended import jwt_required, create_access_token
from app import app, db
from app.models import Cars, Favourites, Users


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    form = NewUserForm()
    uploads = app.config['UPLOAD_FOLDER']

    if request.method == "POST" and form.validate_on_submit():
        username = request.json['username']
        password = request.json['password']
        fullname = request.json['fullname']
        email = request.json['email']
        location = request.json['location']
        biography = request.json['biography']
        date_joined = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        photo = form.photo.data 
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(uploads,filename))
    
        newUser = Users(username,password,fullname, email,location,biography,filename, date_joined)

        takenUsername = Users.query.filter_by(username=username).first()
        takenEmail = Users.query.filter_by(email=email).first()


        if takenUsername is not None: 
            return jsonify(errors= ["Username not available"])
        elif takenEmail is not None:
            return jsonify(errors= ["Email address not available"])

        try: 
            db.session.add(newUser)
            db.session.commit()
            return jsonify(message="Success! New user was added!")
        except Exception as e:
            db.session.rollback()
            print(e)
        return jsonify(errors=["Error!"])
    return jsonify(errors=form_errors(form))
    
        
    

@app.route('/api/auth/login', methods=['POST'])
@login_required
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
    except Exception as e:
        print(e)
        return jsonify('error'), 422


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
