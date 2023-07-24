from flask import Flask
app = Flask(__name__)
app.secret_key = "onair"
app.config['IMAGE_UPLOADS'] = '/Users/STARK 1.1/Pictures'
