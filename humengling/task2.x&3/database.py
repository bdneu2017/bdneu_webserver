# coding:utf-8
from app import db
from users_class import Role, User
from words import FilterWord, AlertMailBox

db.drop_all()
db.create_all()

admin_role = Role(1, 'Admin')  # 管理员
user_role = Role(2, 'User')    # 普通用户

admin = User('admin', '123456', admin_role.id)  # 添加一个管理员账户

filter_1 = FilterWord(u'傻逼', 1)  # 初始过滤 测试功能   1：出现关键字时给告警邮箱发送告警邮件
filter_2 = FilterWord(u'垃圾')  # 后台可添加 修改
filter_3 = FilterWord(u'法轮功')
filter_4 = FilterWord('fuck', 1)
filter_5 = FilterWord('shit')

alert_mailbox = AlertMailBox('3102281319@qq.com')  # 设置初始告警邮箱，后台可修改


db.session.add(admin_role)
db.session.add(user_role)
db.session.add(admin)
db.session.add(filter_1)
db.session.add(filter_2)
db.session.add(filter_3)
db.session.add(filter_4)
db.session.add(filter_5)
db.session.add(alert_mailbox)
db.session.commit()
