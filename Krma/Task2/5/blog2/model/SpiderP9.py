from blog2 import db

class SpiderP9(db.Model):
    #__tablename__ = 'b_category'
    __tablename__ = 'p9'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(20))
    url = db.Column(db.String(100))
    com = db.Column(db.String(5))
    user = db.Column(db.String(20))
    tag  =db.Column(db.String(50))

    def __init__(self,title,url,com,user,tag):
        self.title = title
        self.url = url
        self.com = com
        self.user = user
        self.tag = tag
    def __repr__(self):
        return '<Category %r>' % self.title