from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import User, Steps
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    if current_user.is_authenticated:
        step = Steps.query.filter_by(user_id=current_user.id).first()
        if step is not None:
            if step.get_last_step() is None:
                    return render_template('index.html', step=step, user=current_user)
            else:
                    s1 = step.step1 if step.step1 is not None else ''
                    s2 = step.step2 if step.step2 is not None else ''
                    s3 = step.step3 if step.step3 is not None else ''
                    return render_template('home.html', uid=current_user.id, step1=s1, step2=s2, step3=s3, user=current_user)
        else:
            new_step = Steps(user_id=current_user.id)
            db.session.add(new_step)
            db.session.commit()
    else:
            new_step = Steps(user_id=current_user.id)
            db.session.add(new_step)
            db.session.commit()
            return render_template('home.html', uid=current_user.id, user=current_user)
    return render_template("home.html", user=current_user)