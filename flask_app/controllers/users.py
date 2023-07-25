from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.city import City
from flask_app.models.report import Report
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# ---------------------------------------------------

# Login/Registration

@app.route('/')
def index():
    return render_template("index.html")

# ---------------------------------------------------

# DASHBOARD

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect ('/')
    data = {"id": session['user_id']}
    return render_template('home.html', user= User.get_by_id(data), cities = City.all_cities(), chicagoReports = Report.get_all_reports_with_chicago(),
                            newYorkReports = Report.get_all_reports_with_newyork(), miamiReports = Report.get_all_reports_with_miami(), 
                            losAngelesReports = Report.get_all_reports_with_losangeles(), bostonReports = Report.get_all_reports_with_boston(), 
                            austinReports = Report.get_all_reports_with_austin())


# ---------------------------------------------------

# USER REGISTER

@app.route('/register', methods=["POST"])
def register():
    if not User.is_valid_user(request.form):
        return redirect('/')
    data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']) 
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect ('/home')

# ---------------------------------------------------

# USER LOGIN

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email({"email":request.form['email']})
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/home')

# ---------------------------------------------------

# USER LOGOUT

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")




