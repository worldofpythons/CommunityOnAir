from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import user, report, city
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/<cityy>/<int:idd>/show/<int:iid>')
def show_report(cityy,idd,iid):
    if 'id' not in session:
        return redirect ('/logout')
    data = {"id":iid}
    user_data = {"id":session['id']}
    city_data = {"id":idd}
    return render_template('/show.html', report= report.Report.one(data), reports= report.Report.reports_with_users(), cityy=cityy, user= user.User.get_one(user_data), cities = city.City.city_with_reports(city_data) )