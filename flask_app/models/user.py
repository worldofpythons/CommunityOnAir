from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import report, city
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (name, email, password) VALUES(%(name)s, %(email)s, %(password)s)"
        return connectToMySQL('communityOnAir').query_db(query, data)
    
    @classmethod
    def get_one(cls, id):
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('communityOnAir').query_db(query, id)
        return cls(results[0])
    
    @classmethod
    def get_email(cls, email):
        query  = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('communityOnAir').query_db(query, email)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def valid(user):
        valid=True
        query  = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('communityOnAir').query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken!","register")
            valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Bad email format.", "register")
            valid=False
        if len(user['name']) < 3:
            flash("Name must be at least 3 characters","register")
            valid=False
        if len(user['password']) < 8:
            flash("Password must be at least 8 char","register")
            valid=False
        if user['password'] != user['confirm']:
            flash("Passwords don't match!","register")
            valid=False
            
        return valid