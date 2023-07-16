from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import user, report, city
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/<city>')
def city_display():
    return render_template('city_display.html',cities=city.City.city_with_reports())