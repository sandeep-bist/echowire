# auth.py
from flask import Blueprint,render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import UserData,db
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login',methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = UserData.query.filter_by(username=username).first()

    if user and user.password == password:
        login_user(user)
        flash('Login successful!', 'success')
        return redirect(url_for('/'))
    else:
        flash('Login failed. Check your username and password.', 'danger')

    return "success"


@auth_blueprint.route('/register',methods=['POST'])
def register():
    print(request.form,"===========request.form")
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    user = UserData.query.filter_by(username=username).first()

    if user:
        flash('Username already exist. Choose another', 'warning')
        return redirect(url_for('login_view'))
    else:
        # user = UserData(username=username,email=email,password=password)
        # db.session.add(user)
        # db.session.commit()

        flash('Successful,Please login', 'success')

    # return "success"



@auth_blueprint.route('/login_view')
def login_view():
    return render_template('login.html')



@auth_blueprint.route('/logout')
def logout():
    return 'Logout'

@auth_blueprint.route('/register_view')
def register_view():
    return render_template('register.html')


