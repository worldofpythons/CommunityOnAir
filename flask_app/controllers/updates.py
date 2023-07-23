from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.report import Report
from flask_app.models.city import city
from flask_app.models.update import Update

# ---------------------------------------------------
# Create Update
@app.route('/update/create/<int:report_id>/<int:user_id>')
def create_update(report_id,user_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {"id":report_id}
    user_data = {"id":user_id}
    return render_template('update.html', user = User.get_by_id(user_data), report = Report.get_reports_by_reportid_cityInfo(data))

@app.route('/create/update/process', methods=['POST'])
def process_update():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Update.is_valid_update(request.form):
        flash("Please enter a valid update", "update")
    data = {
        "details": request.form['details'],
        "users_id": session['user_id'],
        "report_id": request.form['report_id']
    }
    Update.save(data)
    return redirect('/home')