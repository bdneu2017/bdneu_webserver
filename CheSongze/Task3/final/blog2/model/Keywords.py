from blog2 import db

class Keywords(db.Model):
    #__tablename__ = 'b_category'
    __tablename__ = 'keywords'
    id = db.Column(db.Integer,primary_key=True)
    key = db.Column(db.String(20),unique=True)
    times = db.Column(db.Integer)
    warning = db.Column(db.Boolean)
    def __init__(self):
        self.key = 'NULL'
        self.times=0
        self.warning=False
    '''
    def __init__(self,key):
        self.key = key
        self.times=0
        self.warning=False
    '''
    def __repr__(self):
        return '<Keywords %r>' % self.key