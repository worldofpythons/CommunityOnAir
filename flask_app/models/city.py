from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import report, user, city , update
from flask import flash

# ---------------------------------------------------

# "City" CLASS

class City:
    def __init__( self , data ):
        self.id = data['id']
        self.city_name = data['city_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.reports = []

# ---------------------------------------------------

# SAVE CITY
    @classmethod
    def save_city(cls, data):
        query = "INSERT INTO cities (city_name) VALUES(%(city_name)s);"
        return connectToMySQL('communityOnAir').query_db(query, data)
    

# ---------------------------------------------------

# GET ALL CITIES

    @classmethod
    def all_cities(cls):
        query = "SELECT * FROM cities;"
        results = connectToMySQL('communityOnAir').query_db(query)
        cities = []
        for city in results:
            cities.append(cls(city))
        return cities

# ---------------------------------------------------

# GET CITY BY CITY ID

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM cities WHERE id = %(id)s;"
        results = connectToMySQL('communityOnAir').query_db(query, data)
        print("------------------------------------------------------------")
        print(results)
        return cls(results[0])
    
    # def city_with_reports(cls, id):
    #     query  = "SELECT * FROM cities LEFT JOIN reports ON reports.city_id = cities.id WHERE cities.id = %(id)s;"
    #     results = connectToMySQL('communityOnAir').query_db(query, id)
    #     city = cls(results[0])
    #     for row in results:
    #         reports_data = {
    #         'id': row['reports.id'],
    #         'what': row['what'],
    #         'location': row['location'],
    #         'created_at': row['reports.created_at'],
    #         'updated_at': row['reports.updated_at'],
    #         'city_id': row['city_id'],
    #         'user_id': row['user_id']
    #         }
    #         city.reports.append(report.Report(reports_data))
    #     return city