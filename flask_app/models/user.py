from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import report, user, city , update   

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

# ---------------------------------------------------

# "User" CLASS

class User:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.comments=[]

# ---------------------------------------------------

# VALIDATION

    @staticmethod
    def is_valid_user(data):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('communityOnAir').query_db(query,data)
        if len(results) >= 1:
            flash("Email already taken.")
            is_valid = False
        if len(data["name"]) < 3:
            flash("User name must be at least 3 characters.","register")
            is_valid = False
        if not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email address.","register")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be 8 characters or longer.","register")
            is_valid = False
        if data['password'] != data['confirm']:
            flash("Passwords don't match","register")
            is_valid = False
        return is_valid

# ---------------------------------------------------

# GET ALL USERS

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('communityOnAir').query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

# ---------------------------------------------------

# SAVE USER NAME, EMAIL AND PASSWORD

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (name, email, password) VALUES (%(name)s, %(email)s, %(password)s);"
        return connectToMySQL('communityOnAir').query_db(query, data)
    
# ---------------------------------------------------

# GET EMAIL

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('communityOnAir').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

# ---------------------------------------------------

# GET USER BY USER ID

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        results = connectToMySQL('communityOnAir').query_db(query,data)
        return cls(results[0])