from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import city, user
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Report:
    def __init__( self , data ):
        self.id = data['id']
        self.what = data['what']
        self.location = data['location']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.city_id = data['city_id']