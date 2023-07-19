from flask_app import app
from flask_app.controllers import users
from flask_app.controllers import cities
from flask_app.controllers import reports
from flask_app.controllers import updates

if __name__=="__main__":
    app.run(debug=True)
