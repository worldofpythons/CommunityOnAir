from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.city import City
from flask_app.models.user import User
from flask_app.models.report import Report
from flask_app.models.update import Update
from werkzeug.utils import secure_filename
import os


# ---------------------------------------------------

# # SHOW ALL REPORTS

# @app.route('/home')
# def dashboard():
#     if 'user_id' not in session:
#         return redirect ('/logout')
#     data = {"id": session['id']}
#     return render_template('home.html', user= User.get_by_id(data), cities = City.cities(), reports= Report.get_all_reports_with_userInfo())

# ---------------------------------------------------

# SHOW EACH CITY

@app.route('/city/<int:city_id>')
def each_city(city_id):
    if 'user_id' not in session:
        return redirect ('/logout')
    data = {"id": session['user_id']}
    city_data = {"id": city_id}
    print(city_data)
    return render_template('city_display.html', user= User.get_by_id(data), city= City.get_one(city_data), reports = Report.get_reports_by_cityId_userinfo(city_data))

# ---------------------------------------------------

# SHOW REPORTS BY CITY - CITY DISPLAY PAGE

@app.route('/city/reports/<int:report_id>/<int:city_id>')
def city_display(city_id):
    if 'user_id' not in session:
        return redirect ('/logout')
    data = {"id": session['user_id']}
    city_data = {"id": city_id}
    return render_template('show.html', user= User.get_by_id(data), reports = Report.get_reports_by_report_id(city_data))
# reports= report.Report.reports_with_users()


#----------------------------------------------------

# SHOW ONE REPORT - SHOW.HTML

@app.route('/city/show/<int:report_id>/<int:city_id>')
def show_report(report_id,city_id):
    if 'user_id' not in session:
        return redirect ('/logout')
    data = {"id":report_id}
    user_data = {"id":session['user_id']}
    city_data = {"id": city_id}
    return render_template('/show.html', report = Report.get_reports_by_reportid_cityInfo(data), user= User.get_by_id(user_data), updates = Update.updates_with_report_id(data), city = City.get_one(city_data))

# ---------------------------------------------------

# CREATE REPORT 

@app.route('/create')
def create_report():
    if 'user_id' not in session:
        return redirect('/logout')
    user = User.get_by_id({"id":session['user_id']})
    return render_template('create.html', user=user, cities = City.all_cities())


@app.route('/create/process', methods=['POST'])
def process():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Report.valid_report(request.form):
        return redirect('/create')
    image = request.files['image']
    if image.filename == "":
        flash("Please select a file")
        return redirect('/create')
    image.save(os.path.join(app.config['IMAGE_UPLOADS'], image.filename))
    data = {
        'what_happened': request.form['what_happened'],
        'cities_id': request.form['city_id'],
        'users_id': session['user_id'],
        'location': request.form['location'],
        'image': image.filename
    }
    Report.save_report(data)
    return redirect('/city')

# ---------------------------------------------------

# EDIT AND UPDATE PAGE - USERS CAN EDIT AND UPDATE THEIR REPORTS

@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    user = User.get_by_id({"id":session['user_id']})
    Data = {"id": id}
    return render_template('edit.html', user=user, report=Report.get_reports_by_reportid_cityInfo(Data),cities=City.all_cities())

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Report.valid_report(request.form):
        return redirect(f'/edit/{id}')
    data = {
        'what_happened': request.form['what_happened'],
        'cities_id': request.form['city'],
        'users_id': session['user_id'],
        'location': request.form['location'],
        'id': id,
        'image': request.form['image']
    }
    Report.update_report(data)
    return redirect('/city')

# ---------------------------------------------------

# DELETE - USERS CAN DELETE THEIR REPORTS

@app.route('/delete/<int:id>')
def delete_report(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {"id":id}
    Report.delete_report(data)
    return redirect('/city')