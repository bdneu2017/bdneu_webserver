from flask_login import UserMixin
from blog2 import db

# Create user model.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(64))
    admin = db.Column(db.Boolean)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username
    '''
    def __init__(self,username,password,admin):
        self.username  = username
        self.password = password
        self.admin = admin
    '''

'''
class User(db.Model, UserMixin):
    __tablename__ = 'b_user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(10),unique=True)
    password = db.Column(db.String(16))

    def __init__(self,username,password):
        self.username  = username
        self.password = password
    def __repr__(self):
        return '<User %r>' % self.username
'''