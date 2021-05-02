from flask import Flask
from app.config import Config, DevelopmentConfig
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
csrf = CSRFProtect(app)
app.config.from_object(DevelopmentConfig)


db = SQLAlchemy(app)


app.config ['UPLOAD_FOLDER'] = './app/static/uploads'




from app import views