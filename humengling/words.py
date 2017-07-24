# coding:utf-8
from flask_login import login_required,current_user
from flask import render_template,flash, url_for,redirect,request
import time
from app import app, db
from email.mime.text import MIMEText
from email.header import Header
import smtplib
class Word(db.Model):  #用户留言
    __tablename__='words'
    id=db.Column(db.Integer,primary_key=True)
    time_now=db.Column(db.String(20))
    title=db.Column(db.String(50),nullable=False)
    content=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
 
    def __init__(self,title,content,user_id):
        self.title=title
        self.content=content
        self.user_id=user_id
        self.time_now=str(time.strftime('%Y-%m-%d %H:%M:%S'))
class FilterWord(db.Model): #过滤关键字 统计关键字
    __tablename__='filter_words'
    id=db.Column(db.Integer,primary_key=True)
    key=db.Column(db.String(10),nullable=False,unique=True)
    times=db.Column(db.Integer,nullable=False)  
    alert=db.Column(db.Integer)#1为告警 0不告警 希望是选择框“是或否”
    def __init__(self,key='',times=0,alert=1): # word='' 使得能够添加内容
        self.key=key.lower() #关键字不区分大小写
        self.times=times
        self.alert=alert
    def __repr__(self):
        return '%r' %self.key
class AlertMail(db.Model): # 告警邮箱
    __tablename__='alert_mail'
    id=db.Column(db.Integer,primary_key=True) 
    mail=db.Column(db.String(50),nullable=False,unique=True)
    def __init__(self,mail):
        self.mail=mail


#留言系统
@app.route('/words',methods =['GET','POST']) #留言页面
@login_required#登录才可访问

def words():
    result=[]
    try:
        r=Word.query.all()
        for row in r:
            result.append(row.time_now+'  '+row.user.username)
            result.append(row.title)
            result.append(row.content)
            
    except:
        result=u'内部发生错误*·*'
    info=spider_info('zuiyou/1.txt')
    if info==[]:
        try:
            info=spider_info('zuiyou/3.txt')
        except:
            return render_template('word.html',history=result)  
    return render_template('words.html',history=result,info=info) # *. *
@app.route('/updatew',methods=['POST','GET'])#更新留言
@login_required
def update_words():
    if request.method=='GET':
        flash(u'参数错误，请提交留言后访问')
    if request.method=='POST': #将留言更新到数据库
        title=request.form['title']
        content=request.form['content']
        keys=get_key_times()[0]  
        content=fillter(content, keys) 
        word_t=Word(title,content, current_user.id)# *,*
        db.session.add(word_t)
        db.session.commit()
    return redirect(url_for('words'))

def spider_info(f): # 将txt文件内容存到列表，便于网页分行
    fp=open(f)
    thing=[]
    while True: 
        line=fp.readline()      
        thing.append(line)
        if not line:
            break
    fp.close()
    return thing

def fillter(content,keys): # 用 * 替换 content中的key_word 统计关键字出现次数 得到top3次数 告警邮件
    content=content.lower()
    for key_word in keys:
        while key_word in content:
            content=content.replace(key_word,'*',1)
            key_t=FilterWord.query.filter_by(key=key_word).first()      
            key_t.times=key_t.times+1 
            if key_t.alert==1:
                alert_msg=u'用户'+str(current_user)+u'发布了关键字:'+key_word
                mail_to=AlertMail.query.first().mail
                alert_mail(alert_msg,mail_to)  #                          
            db.session.add(key_t)
    db.session.commit()
    Max_Times=top_keys()
    return content   
def get_key_times(): # 数据库中的关键字和出现次数 
     key_ts=FilterWord.query.all()
     keys=[]
     times=[]
     for key in key_ts:
        keys.append(key.key)
        times.append(key.times)
     return [keys,times]

def top_keys(): # 得到关键字top3
    result=get_key_times()
    times=result[1]
    keys=result[0]
    fina=[]
    while len(fina)<3 and len(times)!=0:        
        max_times=max(times)
        top=[]
        i=0  # 下标
        while len(times)!=0 and i<len(times):           
            if times[i]==max_times:
                top.append(keys[i]) #页面显示中文而不是unicode -> 单个中文输出正常，列表中的中文无法显示         
                times.remove(times[i])
                keys.remove(keys[i])
            else:
                i=i+1      
        fina.append(top)#int(max_times),

    return fina

def alert_mail(alert_msg,to_addr):

    from_addr='934454035@qq.com'
    password='plezvteejbxwbgah'
    smtp_server='smtp.qq.com'
    msg=MIMEText(alert_msg,'plain','utf-8')
    msg['From']=from_addr
    msg['To']=to_addr
    msg['Subject']=Header(u'关键字告警邮件','utf-8').encode()
    server=smtplib.SMTP_SSL(smtp_server,465)
    server.set_debuglevel(1)
    server.login(from_addr,password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

















