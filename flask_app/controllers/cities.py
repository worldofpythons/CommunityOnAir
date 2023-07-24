from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.report import Report
from flask_app.models.city import City


# ---------------------------------------------------

# SHOW ALL CITIES

@app.route('/city')
def city():
    if 'user_id' not in session:
        return redirect ('/logout')
    data = {"id": session['user_id']}
    return render_template('city.html', user= User.get_by_id(data), cities = City.all_cities())


# @app.route('/<display>/<int:id>')
# def city_display(display, id):
#     if 'id' not in session:
#         return redirect ('/logout')
#     data = {"id": id}
#     user_id = session["id"]
#     user_data = {"id": user_id}
#     return render_template('city_display.html', user= user.User.get_one(user_data), cities=city.City.city_with_reports(data))