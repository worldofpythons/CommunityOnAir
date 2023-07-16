from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import user, report, city
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods=["POST"])
def register():
    if not user.User.valid(request.form):
        return redirect('/')
    data = {
        "first": request.form['first'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']) 
    }
    id = user.User.save(data)
    session['id'] = id
    return redirect ('/home')


@app.route('/login',methods=['POST'])
def login():
    user_login = user.User.get_email(request.form)
    if not user_login:
        flash("Invalid email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_login.password,request.form['password']):
        flash("Invalid password","login")
        return redirect('/')
    session["id"] = user_login.id
    return redirect("/home")


@app.route('/home')
def dashboard():
    if 'id' not in session:
        return redirect ('/logout')
    data = {
        'id' : session['id']
        }
    return render_template('home.html', user= user.User.get_one(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

