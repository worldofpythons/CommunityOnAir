from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import user, report, city
from flask_app.models.user import User
from flask_app.models.report import Report


# ---------------------------------------------------
# Show All Reports
@app.route('/home')
def dashboard():
    if 'id' not in session:
        return redirect ('/logout')
    data = {"id": session['id']}
    return render_template('home.html', user= user.User.get_by_id(data), cities = city.City.cities(), reports= report.Report.reports_with_users())

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
    return render_template('/show.html', report= report.Report.get_one(data), reports= report.Report.reports_with_users(), cityy=cityy, user= user.User.get_one(user_data), cities = city.City.city_with_reports(city_data) )

# ---------------------------------------------------

# CREATE FACT PAGE - USERS CAN CREATE A FACT

@app.route('/create')
def create_report():
    if 'user_id' not in session:
        return redirect('/logout')
    user = User.get_by_id({"id":session['user_id']})
    return render_template('create.html', user=user)


@app.route('/create/process', methods=['POST'])
def process():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Report.valid_report(request.form):
        return redirect('/create')
    data = {
        'user_id': session['user_id'],
        'city': request.form['city'],
        'what_happened': request.form['what_happened'],
        'location': request.form['location'],
        'picture': request.form['picture']
    }
    Report.save_report(data)
    return redirect('/home')

# ---------------------------------------------------
# EDIT AND UPDATE PAGE - USERS CAN EDIT AND UPDATE THEIR FACTS

@app.route('/edit/<int:id>')
def edit(id):
    if 'id' not in session:
        return redirect('/logout')
    user = User.get_by_id({"id":session['user_id']})
    return render_template('edit.html', user=user, report=Report.reports_with_users({'id': id}))

@app.route('/city/<city>/edit/<int:id>', methods=['POST'])
def update(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Report.valid_report(request.form):
        return redirect(f'/edit/{id}')
    data = {
        'id': id,
        'user_id': session['user_id'],
        'city': request.form['city'],
        'what_happened': request.form['what_happened'],
        'location': request.form['location'],
        'picture': request.form['picture']
    }
    Report.update_report(data)
    return redirect('/show')

# ---------------------------------------------------
# DELETE - USERS CAN DELETE THEIR FACTS

@app.route('/delete/report/<int:id>')
def delete_report(id):
    if 'id' not in session:
        return redirect('/logout')
    Report.delete_report({'id':id})
    return redirect('/home')