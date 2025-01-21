from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

#описание моделей
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), )
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    balance = db.Column(db.Integer)
    commission_rate = db.Column(db.Integer)
    URL_webhook = db.Column(db.String(100))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Transaction(db.Model):
    __tablename__ = "Transactions"
    id = db.Column(db.Integer, primary_key=True)
    sum = db.Column(db.Integer)
    commission = db.Column(db.Integer)
    status = db.Column(db.String(100), default='Ожидание', nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('transactions', lazy=True))
