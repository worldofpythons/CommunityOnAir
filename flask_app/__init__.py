from flask import Flask
app = Flask(__name__)
app.secret_key = "onair"
app.config['IMAGE_UPLOADS'] = '/Users/ricardopalafox/Desktop/COMMUNITY_ON-AIR/CommunityOnAir/flask_app/static/img/uploads'
