# coding:utf-8
from app import db
from classes import Role,User
from md5 import to_md5
from words import FilterWord,AlertMail

db.drop_all()
db.create_all()

admin_role = Role(1,'Admin')    
user_role = Role(2,'User')  # 没有id
admin = User('admin',to_md5('123456'),admin_role.id)  # 添加一个管理员账户

filter_1=FilterWord(u'傻逼',0) #初始过滤 测试功能
filter_2=FilterWord(u'辣鸡',0)
filter_3=FilterWord(u'共产党',0)
filter_4=FilterWord(u'枪',0)
filter_5=FilterWord(u'法轮功',0)
filter_6=FilterWord('fuck',0)
filter_7=FilterWord('shit',0)
filter_8=FilterWord('mom',0)

alert_mail=AlertMail('3102281319@qq.com')

#try:
db.session.add(admin_role)
db.session.add(user_role)   
db.session.add(admin) 
db.session.add(filter_1)
db.session.add(filter_2)
db.session.add(filter_3)
db.session.add(filter_4)
db.session.add(filter_5)
db.session.add(filter_6)
db.session.add(filter_7)
db.session.add(filter_8)
db.session.add(alert_mail)
db.session.commit()
#except:
 #   pass


