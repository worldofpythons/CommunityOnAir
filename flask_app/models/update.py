from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, report


# ---------------------------------------------------
# "Update" CLASS
class Update:
    def __init__( self, data):
        self.id = data['id']
        self.details = data['details']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.report_id = data['report_id']

# ---------------------------------------------------
# VALIDATION

    @staticmethod
    def is_valid_update(data):
        is_valid = True
        if len(data['details']) < 3:
            flash("Details must be at least 3 characters.","update")
            is_valid = False
        return is_valid
    
# ---------------------------------------------------
# Save UPDATE with USER ID and REPORT ID

    @classmethod
    def save(cls, data):
        query = "INSERT INTO updates (details, users_id, report_id) VALUES(%(details)s, %(users_id)s, %(report_id)s);"
        return connectToMySQL('communityOnAir').query_db(query, data)
    
# ---------------------------------------------------
# GET ALL UPDATES
    @classmethod
    def updates(cls):
        query = "SELECT * FROM updates;"
        results = connectToMySQL('communityOnAir').query_db(query)
        updates = []
        for update in results:
            updates.append(cls(update))
        return updates
# ---------------------------------------------------
# GET ONE UPDATE

    @classmethod
    def get_one_by_id(cls, data):
        query = "SELECT * FROM updates WHERE id = %(id)s;"
        result = connectToMySQL('communityOnAir').query_db(query, data)
        if result:
            update = cls(result[0])
            return update
        else:
            return cls(result[0])
# ---------------------------------------------------
#UPDATE AN UPDATE

    @classmethod
    def update(cls, data):
        query = "UPDATE updates SET details = %(details)s, updated_at = NOW() WHERE id = %(id)s;"
        result = connectToMySQL('communityOnAir').query_db(query, data)
        return result

# ---------------------------------------------------
# DELETE A COMMENT

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM updates WHERE id = %(id)s;"
        result = connectToMySQL('communityOnAir').query_db(query, data)
        return result