from flask import Flask
app = Flask(__name__)
app.secret_key = "onair"
app.config['IMAGE_UPLOADS'] = '/Users/ricardopalafox/desktop/COMMUNITY_ON-AIR/python_for_CommunityOnAir/flask_app/static/img/uploads'
