from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import city, user
from flask import flash
from werkzeug.utils import secure_filename
import os

# ---------------------------------------------------

# "Report" CLASS
class Report:
    def __init__( self , data ):
        self.id = data['id']
        self.what_happened = data['what_happened']
        self.location = data['location']
        self.image = data['image']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.cities_id = data['cities_id']
        self.users_id = data['users_id']
        self.reporter = None
        self.updates =[]
        
# ---------------------------------------------------

# GET REPORTS BY CITY AND ID

    @classmethod
    def get_reports_by_reportid_cityInfo(cls, data):
        query = "SELECT * FROM reports LEFT JOIN cities ON cities_id = cities.id LEFT JOIN users ON users_id = users.id WHERE reports.id = %(id)s;"
        results = connectToMySQL('communityOnAir').query_db(query, data)
        reports = []
        print(results)
        for report in results:
            this_report = cls(report)
            user_data = {
                "id": report['users.id'],
                "name": report['name'],
                "email": report['email'],
                "password": "",
                "created_at": report['users.created_at'],
                "updated_at": report['users.updated_at']
            }
            this_report.reporter = user.User(user_data)
            reports.append(report)

        for report in results:
            this_report = cls(report)
            city_data = {
                "id": report['cities.id'],
                "city_name": report['city_name'],
                "created_at": report['cities.created_at'],
                "updated_at": report['cities.updated_at']
            }
            this_report.reporter = city.City(city_data)
            reports.append(report)
        
        return reports[0]
            
# ---------------------------------------------------

# GET REPORTS BY REPORT ID AND CITY NAME

    @classmethod
    def get_reports_by_report_id(cls, data):
        query = "SELECT * FROM reports LEFT JOIN users ON users_id = users.id WHERE reports.id = %(id)s;"
        results = connectToMySQL('communityOnAir').query_db(query, data)
        reports = []
        print(results)
        for report in results:
            this_report = cls(report)
            user_data = {
                "id": report['users.id'],
                "name": report['name'],
                "email": report['email'],
                "password": "",
                "created_at": report['users.created_at'],
                "updated_at": report['users.updated_at']
            }
            this_report.reporter = user.User(user_data)
            reports.append(report)
        print(reports)
        return reports
    
# ---------------------------------------------------

# GET ALL REPORTS JOINS WITH USERS AND CITIES
    @classmethod
    def reports_with_users(cls):
        query = """
                SELECT * FROM reports LEFT
                JOIN users on reports.user_id = users.id
                LEFT JOIN cities on reports.city_id = cities.id;
                """
        results = connectToMySQL('communityOnAir').query_db(query)
        reports = []
        for row in results:
            this_report = cls(row)
            user_data = {
                "id": row['users.id'],
                "first": row['first'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            city_data = {
                "id": row['cities.id'],
                "name":row['name'],
                "created_at": row['cities.created_at'],
                "updated_at": row['cities.updated_at'],
                "reports": None
            }
            this_report.user_id = user.User(user_data)
            this_report.city_id = city.City(city_data)
            reports.append(this_report)
        return reports
    
# ---------------------------------------------------

# SAVE REPORT

    @classmethod
    def save_report(cls, data):
        query = "INSERT INTO reports (what_happened, cities_id, users_id, location, image) VALUES(%(what_happened)s, %(cities_id)s, %(users_id)s, %(location)s, %(image)s);"
        return connectToMySQL('communityOnAir').query_db(query, data)

# ---------------------------------------------------

# GET REPORT BY ID
    @classmethod
    def get_one(cls, id):
        query  = "SELECT * FROM reports WHERE id = %(id)s;"
        results = connectToMySQL('communityOnAir').query_db(query, id)
        
        return cls(results[0])
    
# ---------------------------------------------------

# UPDATE REPORT

    @classmethod
    def update_report(cls,data):
        query = """UPDATE reports 
               SET what_happened =%(what_happened)s, cities_id = %(cities_id)s, users_id = %(users_id)s, location=%(location)s, image= %(image)s, updated_at =NOW()
                WHERE (id = %(id)s);"""
        return connectToMySQL('communityOnAir').query_db(query,data) 

# ---------------------------------------------------

# DELETE REPORT

    @classmethod
    def delete_report(cls, id):
        query  = "DELETE FROM reports WHERE id = %(id)s;"
        return connectToMySQL('communityOnAir').query_db(query, id)

# ---------------------------------------------------

# VALIDATION

    @staticmethod
    def valid_report(report):
        valid=True
        if len(report['what_happened']) < 5:
            flash("What happened must be at least 5 characters","report")
            valid=False
        if len(report['location']) < 3:
            flash("Location must be at least 3 characters","location")
            valid=False
        return valid
    
    @classmethod
    def get_reports_by_city_id(cls,data):
        query = "SELECT * FROM reports WHERE cities_id = %(id)s;"
        results = connectToMySQL('communityOnAir').query_db(query, data)
        reports = []
        for report in results:
            reports.append(cls(report))
        return reports
    