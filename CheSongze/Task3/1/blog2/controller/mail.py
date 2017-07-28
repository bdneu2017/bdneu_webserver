# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_mail import Mail, Message
from threading import Thread
import os
from blog2 import app

app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'  # 邮件服务器地址
app.config['MAIL_PORT'] = 587               # 邮件服务器端口
app.config['MAIL_USE_TLS'] = True          # 启用 TLS
app.config['MAIL_USERNAME'] = 'flasktest@outlook.com'
app.config['MAIL_PASSWORD'] = 'flask2014'
#app.config['SECURITY_EMAIL_SENDER'] = 'flasktest@outlook.com'

mail = Mail(app)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(mailcon,content):
    msgcon='<br>发现&nbspID:&nbsp'+str(content.userid)+'&nbsp的用户&nbsp'+str(content.username)+'&nbsp发表的新留言中出现高危敏感词：</br><table border="2" bordercolor="grey" cellspacing="0" cellpadding="5" align="center"><tr><td>关键词</td><td>出现次数</td></tr>'
    for i in mailcon:
        msgcon+='<tr><td>'+str(i['key'])+'</td><td>'+str(i['times'])+'次</td></tr>'
    msgcon+='</table><br>请于后台管理系统确认并处理。</br>'
    msg = Message('Warning：关键词', sender=('ethan', 'flasktest@outlook.com'), recipients=['j.krma@hotmail.com'])
    msg.html = msgcon
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return 'send successfully'
'''
# 最基本的发送邮件方式
@app.route('/')
def index():
    msg = Message('Hello', sender=('ethan', 'flasktest@outlook.com'), recipients=['j.krma@hotmail.com'])
    # msg.body = 'The first email!'
    msg.html = '<b>Hello Web</b>'
    mail.send(msg)

    return '<h1>OK!</h1>'
'''
'''
# 异步发送邮件
@app.route('/sync')
def send_email():
    msg = Message('Hello', sender=('ethan', 'flasktest@outlook.com'), recipients=['j.krma@hotmail.com'])
    msg.html = '<b>send email asynchronously</b>'
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return 'send successfully'


# 邮件带附件
@app.route('/attach')
def add_attchments():
    msg = Message('Hello', sender=('ethan', 'flasktest@outlook.com'), recipients=['j.krma@hotmail.com'])
    msg.html = '<b>Hello Web</b>'

    with app.open_resource("/Users/ethan/Documents/pixels.jpg") as fp:
        msg.attach("photo.jpg", "image/jpeg", fp.read())

    mail.send(msg)
    return '<h1>OK!</h1>'


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
    '''