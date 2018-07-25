from flask import Flask

import config
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# app.config.from_pyfile('thisapp.cfg')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

# adding new value for db.session
db_session = db.session