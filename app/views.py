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
from app.models import *
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import exc
from functools import wraps
from app.config import *
from sqlalchemy import func


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

def token_authenticate(t):
    @wraps(t)
    def decorated(*args, **kwargs):
        
        auth = request.headers.get('Authorization', None)
        
        if not auth:
            return jsonify({'error': 'Access Denied : No Token Found'}), 401
        else:
            try:
                userdata = jwt.decode(auth.split(" ")[1], app.config['SECRET_KEY'])
                currentUser = Users.query.filter_by(username = userdata['user']).first()
                
                if currentUser is None:
                    return jsonify({'error': 'Access Denied'}), 401
                
            except jwt.exceptions.InvalidSignatureError as e:
                print (e)
                return jsonify({'error':'Invalid Token'})
            except jwt.exceptions.DecodeError as e:
                print (e)
                return jsonify({'error': 'Invalid Token'})
            return t(*args, **kwargs)
    return decorated


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

@app.route('/api/register', methods=['POST'])
def register():
    form = NewUserForm()
    uploadFolder = app.config['UPLOAD_FOLDER']

    if request.method == "POST" and form.validate_on_submit():

        try: 

            username=request.form['username']
            password=request.form['password']
            fullname=request.form['fullname']
            email=request.form['email']
            location=request.form['location']
            biography=request.form['biography']
            photo=request.files['photo'] 
            filename=secure_filename(photo.filename)
            date_joined=datetime.datetime.now()

            newUser=Users(username=username,password=password,fullname=fullname, email=email, location=location, biography=biography,photo=filename,date_joined=date_joined)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if newUser is not None:
                db.session.add(newUser)
                db.session.commit()
                return jsonify(message = "User successfully registered")
                
        except Exception as e:
            db.session.rollback()
            print (e)
            return jsonify(errors=["Internal Error"])
    
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
@token_authenticate
def logout():
    return jsonify(message= "User successfully logged out.")
    
@app.route('/api/cars', methods = ['POST','GET'])
@token_authenticate
def carDem():
    if request.method == 'GET':
        carDem = Cars.query.all()
        carsList = []
        for car in carDem:
            obCar = {"id": car.id, "user_id": car.user_id, "color": car.colour,"make": car.make,"model": car.model,"year": car.year,"price": car.price,"photo": os.path.join(app.config['UPLOAD_CARPHOTO'],car.photo) }
            carList.append(obCar)
        
        return jsonify(cars=carList)

    elif request.method == 'POST':
        
        form = AddNewCarForm()
        
        if request.method == 'POST' and form.validate_on_submit():
            
            description = form.description.data
            make = form.make.data
            model = form.model.data
            colour = form.colour.data
            year = form.year.data
            transmission = form.transmission.data
            car_type = form.car_type.data
            price = form.price.data
            photo= form.photo.data
            user_id = form.user_id.data
            
            newUser = Users.query.filter_by(id=user_id).first()
            
            filename = newUser.username+secure_filename(photo.filename)
            
            
            car = Cars(description=description,make=make,model=model,colour=colour,year=year,transmission=transmission,car_type=car_type,price=price,photo=filename,user_id=user_id)

            photo.save(os.path.join(app.config['UPLOAD_CARPHOTOs'],filename))
            db.session.add(car)
            db.session.commit()
            
            return jsonify(status=201, message="Car Created")
            
            
        print (form.errors.items())
        return jsonify(status=200, errors=form_errors(form))

@app.route('/api/cars/<car_id>', methods =['GET'])
@token_authenticate
def car(car_id):

        car = Cars.query.filter_by(id=car_id).first()
      
        response = {"status": "ok", "carInfo":{"id": car.id, "make": car.make,"model": car.model,"year": car.year,"price": car.price,"photo": os.path.join("../", app.config['UPLOAD_CARPHOTO'],car.photo), "description":car.description,"colour": car.colour, "transmission":car.transmission,"car_type": car.car_type, "user_id": car.user_id}}
        return jsonify(response)

@app.route('/api/cars/<car_id>/favourite',methods = ['POST'])
@token_authenticate
def fave(car_id):
    
    request_payload = request.get_json()
    user_id = request_payload["user_id"]
    car_id = request_payload["car_id"]
    
    car = Cars.query.filter_by(id=car_id).first()
    faves = Favourites.query.filter_by(car_id=car_id).all()
    
    if car is None:
        return jsonify(staus="", message="The post is unavailable!")
        
    if faves is not None:
        for fave in faves:
            if fave.user_id == user_id:
                return jsonify(status=200, message="You have favorited this car!")
        
    FavCar = Favourites(car_id = car_id, user_id = user_id)
    
    db.session.add(FavCar)
    db.session.commit()
    
    return jsonify({"status":201,'message': 'Added to Favourites!'})



@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))  


@app.route('/api/search', methods = ['GET'])
@token_authenticate
def search():
    makeSearch = request.args.get("make")
    modelSearch = request.args.get("model")

    carsGen = Cars.query.filter((func.lower(Cars.make)==func.lower(make)) | (func.lower(Cars.model)==func.lower(model)))
    carList = []
    for car in carsGen:
        obCar = {"id": car.id, "user_id": car.user_id,"make": car.make,"model": car.model,"year": car.year,"price": car.price,"photo": os.path.join(app.config['UPLOAD_CARPHOTOS'],car.photo) }
        carList.append(obCar)
        
    return jsonify(cars=carList)



def convJoinedDate(yy,mm,dd):
    return datetime.date(yy,mm,dd).strftime("%B %d,%Y")



 

@app.route('/api/users/<user_id>', methods =['GET'])
@token_authenticate
def profile(user_id):
        user = Users.query.filter_by(id=user_id).first()
        joinedYear = int(user.date_joined.split("-")[0])
        joinedMonth = int(user.date_joined.split("-")[1])
        joinedDay = int(user.date_joined.split("-")[2])
    
        user.date_joined = convJoinedDate(joinedYear, joinedMonth, joinedDay)
      
        response = {"status": "ok", "userInfo":{"name":user.fullname, "location": user.location,"email": user.email,"username": "@"+user.username, "date_joined":user.date_joined , "biography": user.biography, "photo": os.path.join("../", app.config['UPLOAD_PROFILEPIC'],user.photo)}}
        
        return jsonify(response)

@app.route('/api/users/<user_id>/favourites',methods = ['GET'])
@token_authenticate
def favourites(user_id):
    faves = Favourites.query.filter_by(user_id = user_id).all()
    faveCarList = []
    for fav in faveCarList:
        car = Cars.query.filter_by(id=fav.car_id).first()
        favOb = {"id": car.id, "user_id": car.user_id,"make": car.make,"model": car.model,"year": car.year,"price": car.price,"photo": os.path.join("../",app.config['UPLOAD_CARPHOTOS'],car.photo) }
        fvcars.append(favOb)
        
    return jsonify(cars=faveCarList)


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
