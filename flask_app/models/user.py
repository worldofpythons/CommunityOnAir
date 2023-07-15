from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models. import
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash