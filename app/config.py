import os

class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Som3$ec5etK*y'
    UPLOAD_FOLDER = './app/static/uploads'
    UPLOAD_PROFILE = os.environ['UPLOAD_PROFILEPIC'] = './app/static/uploads/profile' 
    UPLOAD_CARPHOTO = os.environ['UPLOAD_CARPHOTO'] = './app/static/uploads/cars'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://yourusername:yourpassword@localhost/databasename'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'postgresql://dndyufqhgpsofl:0c7b169281a44d80ea56cb1b147e30114b84f963f3b79b94024f05838895853d@ec2-54-163-254-204.compute-1.amazonaws.com:5432/d3np874d3ev5su'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development Config that extends the Base Config Object"""
    #FLASK_ENV = 'development'
    #ENV = 'development'
    DEVELOPMENT = True
    DEBUG = True

class ProductionConfig(Config):
    """Production Config that extends the Base Config Object"""
    DEBUG = False 