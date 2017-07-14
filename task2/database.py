# coding:utf-8
from app import db
from classes import Role,User
from md5 import to_md5

db.drop_all()
db.create_all()

admin_role = Role(1,'Admin')    
user_role = Role(2,'User')  # 没有id
admin = User('admin',to_md5('123456'),admin_role.id)  # 添加一个管理员账户

try:
    db.session.add(admin_role)
    db.session.add(user_role)   
    db.session.add(admin) 
    db.session.commit()
except:
    pass


