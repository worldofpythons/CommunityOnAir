from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.city import City
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# ---------------------------------------------------
# Login/Registration

@app.route('/')
def index():
    return render_template("index.html")

# ---------------------------------------------------
# USER REGISTER
@app.route('/register', methods=["POST"])
def register():
    if not User.valid(request.form):
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
#USER LOGIN
@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email({"email":request.form['email']})
    if not user:
        flash("Invalid Email","login")
        return redirect('/dashboard')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/dashboard')
    session['user_id'] = user.id
    return redirect('/home')

# ---------------------------------------------------
# USER LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")




