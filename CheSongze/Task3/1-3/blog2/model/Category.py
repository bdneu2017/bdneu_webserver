from blog2 import db

class Category(db.Model):
    #__tablename__ = 'b_category'
    __tablename__ = 'category'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(20),unique=True)
    content = db.Column(db.String(100))
    userid = db.Column(db.Integer)
    username = db.Column(db.String(80))
    '''
    def __init__(self,title,content,userid,username):
        self.title = title
        self.content = content
        self.userid = userid
        self.username = username
    '''
    def __repr__(self):
        return '<Category %r>' % self.title