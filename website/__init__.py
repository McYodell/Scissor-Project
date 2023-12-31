from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

base_dir = os.path.dirname(os.path.realpath(__file__))

#uri = os.environ.get('DATABASE_URL')
#if uri.startswith('postgres://'):
    #uri = uri.replace('postgres://', 'postgresql://', 1)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    #os.path.join(base_dir, 'test.db')
#app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
#postgres://scissor_project_user:QXVxaUGxbsPlTqaebWLpG7rLomwp0cmF@dpg-ck95d9v0vg2c7386nisg-a.oregon-postgres.render.com/scissor_project
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

cache = Cache(app)
limiter = Limiter(get_remote_address)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from . import routes
from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

with app.app_context():
    db.create_all()