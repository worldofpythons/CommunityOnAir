from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.report import Report
from flask_app.models.city import City
from flask_app.models.update import Update

# ---------------------------------------------------

# CREATE AN UPDATE

@app.route('/update/create/<int:report_id>/<int:user_id>/<int:city_id>')
def create_update(report_id,user_id,city_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {"id":report_id}
    user = {"id":session['user_id']}
    city_data = {"id": city_id}
    return render_template('update.html', user = User.get_by_id(user), report = Report.get_reports_by_reportid_cityInfo(data), city = City.get_one(city_data))

@app.route('/update/create/<int:report_id>/<int:user_id>/<int:city_id>', methods=['POST'])
def process_update(report_id,user_id,city_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Update.is_valid_update(request.form):
        flash("Please enter a valid update", "update")
        return redirect(f'/update/create/{report_id}/{user_id}/{city_id}')
    data = {
        "details": request.form['details'],
        "users_id": session['user_id'],
        "report_id": request.form['report_id'],
        "cities_id": request.form['city_id']
    }
    Update.save(data)
    return redirect(f'/city/show/{report_id}/{city_id}')

# ---------------------------------------------------

# DELETE - USERS CAN DELETE THEIR COMMENTS

@app.route('/delete/comment/<int:id>/<int:idd>/<int:iddd>')
def delete_comment(id,idd,iddd):
    if 'user_id' not in session:
        return redirect('/logout')
    Update.delete_update({'id':id})
    report_id = idd
    city_id = iddd
    return redirect(f'/city/show/{report_id}/{city_id}')

@app.route('/edit/comment/<int:id>/<int:idd>/<int:iddd>')
def edit_comment(id,idd,iddd):
    if 'user_id' not in session:
        return redirect('/logout')
    data = ({'id':id})
    report_data = {"id":idd}
    userr_data = {"id": session['user_id']}
    city_data = {"id": iddd}
    return render_template('edit_update.html', update = Update.get_one_by_id(data), user = User.get_by_id(userr_data), cities = City.all_cities(), report = Report.get_reports_by_reportid_cityInfo(report_data), city = City.get_one(city_data))

@app.route('/update/comment/<int:id>/<int:city_id>/<int:user_id>/<int:report_id>',methods=['POST'] )
def update_comment(id,city_id, user_id, report_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Update.is_valid_update(request.form):
        flash("Please enter a valid update", "update")
        return redirect(f'/update/create/{report_id}/{user_id}/{city_id}')
    data = {"id": id,"details": request.form['details']}
    Update.update(data)
    user_data= {"id":session['user_id']}
    report_id = report_id
    return redirect(f'/city/show/{report_id}/{city_id}')
