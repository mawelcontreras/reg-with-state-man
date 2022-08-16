from email.policy import default
from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#users db
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))

#steps db
class Steps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    step1 = db.Column(db.String(250))
    step2 = db.Column(db.String(250))
    step3 = db.Column(db.String(250))
    steps = (step1, step2, step3)
    user = db.relationship('User', backref='user')

    def get_last_step(self):
        if not self.step1:
            return 1
        if not self.step2:
            return 2
        if not self.step3:
            return 3
    
    def __repr__(self):
        return '<Steps> {} {} {}'.format(self.step1, self.step2, self.step3)