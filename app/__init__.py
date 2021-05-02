from flask import Flask
from flask_login import LoginManager
from app.config import Config, DevelopmentConfig
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SECRET_KEY']="abc123"
app.config['SQLALCHEMY_DATABASE_URI']= "postgresql://yourusername:yourpassword@localhost/databasename"
csrf = CSRFProtect(app)

db = SQLAlchemy(app)
app.config.from_object(Config)
app.config ['UPLOAD_FOLDER'] = './app/static/uploads'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


from app import views