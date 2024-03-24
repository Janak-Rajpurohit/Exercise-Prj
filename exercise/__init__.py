from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from jinja2 import Markup
from markupsafe import Markup 

app = Flask(__name__)
app.config['SECRET_KEY'] = '63eaaf3e93b5a96769795a915492c910'     #got from secret module secrets.token_hex(bytes) //16
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///site.db"         # /// -> relative path of current file 
db = SQLAlchemy(app)
bcr = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view='login'  #function name of our route, checking that user is login otherwise he has no access to account route
login_manager.login_message_category='info'

from flaskblog import routes
