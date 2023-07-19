from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import city, user
from flask import flash

# ---------------------------------------------------
# "Report" CLASS
class Report:
    def __init__( self , data ):
        self.id = data['id']
        self.city = data['city']
        self.what_happened = data['what_happened']
        self.location = data['location']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.city_id = data['city_id']
        self.user_id = data['user_id']
        
# ---------------------------------------------------
# GET ALL REPORTS Joins with USERS and CITIES
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
# Save REPORT
    @classmethod
    def save(cls, data):
        query = "INSERT INTO reports (what_happened, location, city_id, user_id) VALUES(%(what_happened)s, %(location)s, %(city_id)s, %(user_id)s);"
        return connectToMySQL('communityOnAir').query_db(query, data)

# ---------------------------------------------------
#GET REPORT BY ID
    @classmethod
    def get_one(cls, id):
        query  = "SELECT * FROM reports WHERE id = %(id)s;"
        results = connectToMySQL('communityOnAir').query_db(query, id)
        
        return cls(results[0])
    
# ---------------------------------------------------
# UPDATE REPORT
    @classmethod
    def update(cls,data):
        query = """UPDATE reports 
               SET what_happened =%(what_happened )s,location=%(location)s, updated_at =NOW()
                WHERE (id = %(id)s);"""
        return connectToMySQL('communityOnAir').query_db(query,data) 

# ---------------------------------------------------
# DELETE REPORT

    @classmethod
    def delete(cls, id):
        query  = "DELETE FROM reports WHERE id = %(id)s;"
        return connectToMySQL('communityOnAir').query_db(query, id)

# ---------------------------------------------------
# VALIDATION
    @staticmethod
    def valid(report):
        valid=True
        if len(report['what_happened ']) < 5:
            flash("What happened must be at least 5 characters","report")
            valid=False
        if len(report['location']) < 3:
            flash("Location must be at least 3 characters","location")
            valid=False
        return valid