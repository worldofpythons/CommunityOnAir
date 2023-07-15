from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import report, city
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first = data['first']
        self.email = data['email']
        self.passw = data['passw']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.reports = []

   