from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import user, report, city


# ---------------------------------------------------
# Show All Reports
@app.route('/home')
def dashboard():
    if 'id' not in session:
        return redirect ('/logout')
    data = {"id": session['id']}
    return render_template('home.html', user= user.User.get_one(data), cities = city.City.cities(), reports= report.Report.reports_with_users())

# ---------------------------------------------------
#Home Page Route
# @app.route('/home')
# def dashboard():
#     if 'user_id' not in session:
#         return redirect ('/logout')
#     data = {
#         'user_id' : session['user_id']
#         }
#     return render_template('home.html', user= User.get_one(data), cities = City.cities())


# ---------------------------------------------------
# Show Reports by City
@app.route('/<city>/<int:id>')
def city_display(city, id):
    if 'id' not in session:
        return redirect ('/logout')
    data = {"id": session['id']}
    city_data = {"id": id}
    return render_template('city.html', user= user.User.get_one(data), cities = city.City.cities(), reports= report.Report.reports_with_users(), city= city.City.get_one(city_data))




@app.route('/<city>/<int:idd>/show/<int:iid>')
def show_report(cityy,idd,iid):
    if 'id' not in session:
        return redirect ('/logout')
    data = {"id":iid}
    user_data = {"id":session['id']}
    city_data = {"id":idd}
    return render_template('/show.html', report= report.Report.one(data), reports= report.Report.reports_with_users(), cityy=cityy, user= user.User.get_one(user_data), cities = city.City.city_with_reports(city_data) )