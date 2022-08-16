from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, Steps
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged In Successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, Try Again!', category='error')
        else:
            flash('Email does not exist', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exist', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(firstName) < 2:
            flash('First Name must be greater than 2 characters', category='error')
        elif password1 != password2:
            flash('Password don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters', category='error')
        else:
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created!', category='success')
            return redirect(url_for('views.home', id=new_user.id))
    return render_template("sign_up.html", user=current_user)

@auth.route('/home', methods=['GET'])
def steps():
    if not current_user.is_authenticated:
        return jsonify({'error': 'user is not logged in'})
    if 'id' in request.args:
        print("print testing")
        print(request.args)
        id = int(request.args['id'])
        step = Steps.query.filter_by(user_id=id).first()
        if step is not None:
            return jsonify({'last_step_taken': step.get_last_step(),
            'steps': {
                'step1': step.step1,
                'step2': step.step2,
                'step3': step.step3
            }})
    else:
        return jsonify(None)

@auth.route('/home/add', methods=['POST'])
def add_step():
    if not current_user.is_authenticated:
        return jsonify({'error': 'user is not logged in'})

    dd = request.get_json()

    if 'id' in dd:
        id = int(dd['id'])
        data = str(dd['data'])

        step = Steps.query.filter_by(user_id=id).first()
        if step is not None:
            last_step = dd['last_step']
            if last_step == 1: step.step1 = data
            elif last_step == 2: step.step2 = data
            elif last_step == 3: step.step3 = data
            db.session.add(step)
            db.session.commit()
            return jsonify({'last_step_taken': step.get_last_step()})
    else:
        return jsonify(None)