from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Update:
    def __init__( self, data):
        self.id = data['id']
        self.what_happened = data['what']
        self.location = data['location']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.report_id = data['report_id']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO updates (what, location, users_id, report_id) VALUES(%(what)s, %(location)s, %(users_id)s, %(report_id)s);"
        return connectToMySQL('communityOnAir').query_db(query, data)
    
    @classmethod
    def updates(cls):
        query = "SELECT * FROM updates;"
        results = connectToMySQL('communityOnAir').query_db(query)
        updates = []
        for update in results:
            updates.append(cls(update))
        return updates
