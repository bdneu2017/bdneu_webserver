# coding:utf-8
from flask_login import login_required, current_user
from flask import render_template, flash, redirect, request
import time
from app import app, db
from email.mime.text import MIMEText
from email.header import Header
import smtplib


class Word(db.Model):  # 用户留言
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    time_now = db.Column(db.String(20))
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # 留言表与用户表是多对一的关系

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.time_now = str(time.strftime('%Y-%m-%d %H:%M:%S'))


class FilterWord(db.Model):  # 关键字
    __tablename__ = 'filter_words'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(10), nullable=False, unique=True)
    times = db.Column(db.Integer, nullable=False)  # 关键字出现次数
    alert = db.Column(db.Integer, nullable=False)  # 1为告警 0不告警

    def __init__(self, key='', alert=0, times=0):  # 初始化使得能够添加内容
        self.key = key.lower()  # 关键字不区分大小写
        self.alert = alert
        self.times = times

    def __repr__(self):
        return '%r' % self.key


class AlertMailBox(db.Model):  # 告警邮箱  邮箱内容匹配
    __tablename__ = 'alert_mailbox'
    id = db.Column(db.Integer, primary_key=True)
    mailbox = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, mailbox):
        self.mailbox = mailbox


# 留言系统
@app.route('/words', methods=['GET'])  # 留言页面
@login_required  # 登录才可访问
def words():
    result = []
    r = Word.query.all()
    for row in r:
        result.append(row.time_now + '  ' + row.user.username)
        result.append(row.title)
        result.append(row.content)
    try:
        info = spider_info('zuiyou/3.txt')
    except all:
        return render_template('word.html', history=result)
    return render_template('words.html', history=result, info=info)  # *. *


@app.route('/updatew', methods=['POST'])  # 更新留言
@login_required
def update_words():
    # 将留言更新到数据库
    title = request.form['title']
    content = request.form['content']
    if title == '':
        flash(u'留言标题不能为空qwq')
        return redirect('words')
    if content == '':
        flash(u'留言内容不能为空qwq')
        return redirect('words')
    keys = get_key_times()[0]
    content = fillter(content, keys)
    word_t = Word(title, content, current_user.id)  # *,*
    db.session.add(word_t)
    db.session.commit()
    return redirect('words')


def spider_info(f):  # 将txt文件内容存到列表，便于网页分行
    fp = open(f)
    thing = []
    while True:
        line = fp.readline()
        thing.append(line)
        if not line:
            break
    fp.close()
    return thing


def fillter(content, keys):  # 用 * 替换 content 中出现的关键字 统计关键字出现次数 发送告警邮件
    content = content.lower()  # 关键字匹配不区分大小写
    for key_word in keys:
        while key_word in content:
            content = content.replace(key_word, '*', 1)
            # 每次只替换一个关键字，便于计算关键字出现次数
            key_t = FilterWord.query.filter_by(key=key_word).first()
            key_t.times = key_t.times + 1  # 出现次数加1
            if key_t.alert == 1:  # 如果需要告警
                alert_msg = u'用户' + str(current_user) + u'发布了关键字:' + key_word
                # 邮件内容
                mailbox = AlertMailBox.query.first().mailbox  # 告警邮箱
                alert_mail(alert_msg, mailbox)  # 发送告警邮件
            db.session.add(key_t)
    db.session.commit()
    return content


def get_key_times():  # 数据库中的关键字和出现次数
    key_ts = FilterWord.query.all()
    keys = []
    times = []
    for key_t in key_ts:
        keys.append(key_t.key)
        times.append(key_t.times)
    return [keys, times]


def top_keys():  # 得到关键字top3
    result = get_key_times()
    times = result[1]
    keys = result[0]
    fina = []
    while len(fina) < 3 and len(times) != 0:
        max_times = max(times)
        top = []
        i = 0  # 下标
        while i < len(times):
            if times[i] == max_times:
                top.append(keys[i])  # 页面显示中文而不是unicode -> 单个中文输出正常，列表中的中文无法显示
                times.remove(times[i])
                keys.remove(keys[i])
            else:
                i = i + 1
        fina.append(top)
    return fina


def alert_mail(alert_msg, to_addr):  # 发送告警邮件
    from_addr = '934454035@qq.com'  # 发送邮箱
    password = 'plezvteejbxwbgah'
    smtp_server = 'smtp.qq.com'
    msg = MIMEText(alert_msg, 'plain', 'utf-8')
    msg['From'] = from_addr
    msg['To'] = to_addr  # 接收邮箱（告警邮箱）
    msg['Subject'] = Header(u'关键字告警邮件', 'utf-8').encode()  # 包含中文 需要Header对象编码
    server = smtplib.SMTP_SSL(smtp_server, 465)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


















