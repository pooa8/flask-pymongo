from flask import Flask
from flask import request
from flask import render_template
from flask_pymongo import PyMongo
from datetime import datetime
from datetime import timedelta
from bson.objectid import ObjectId
from flask import abort
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
import time
import math


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myweb"
app.config["SECRET_KEY"] = "abcde"  # 유출되면 안되는 중요한 키
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)  # 세션 유지 시간 30분
mongo = PyMongo(app)

from .common import login_required
from .filter import format_datetime
from . import board
from . import member

app.register_blueprint(board.blueprint)
app.register_blueprint(member.blueprint)