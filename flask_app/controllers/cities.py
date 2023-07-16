from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import user, report, city
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/<display>/<int:id>')
def city_display(display, id):
    if 'id' not in session:
        return redirect ('/logout')
    data = {"id": id}
    user_id = session["id"]
    user_data = {"id": user_id}
    return render_template('city_display.html', user= user.User.get_one(user_data), cities=city.City.city_with_reports(data))