# coding:utf-8
from flask_login import login_required,current_user
from classes import Word
from flask import render_template,flash, url_for,redirect,request
import time
from app import app,db
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
        word_t=Word(title,content,current_user.id)# *,*
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








