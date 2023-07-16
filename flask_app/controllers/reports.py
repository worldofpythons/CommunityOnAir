from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import user, report, city
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/<city>/show/<id:id>')
def show_report(id):
    data = {"id":id}
    return redirect ('/show.html', report= report.Report.one(data), reports= report.Report.reports_with_users())