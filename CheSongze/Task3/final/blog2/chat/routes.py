from flask import session, redirect, url_for, render_template, request
from . import chat
from .forms import LoginForm
from blog2 import app
from flask_login import current_user,login_required

'''
@chat.route('/chat/', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('chat.html', form=form)
'''

@chat.route('/chatroom/')
@login_required
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    #name = session.get('name', '')
    name = current_user.login
    #room = session.get('room', '')
    room = '1'
    if name == '' or room == '':
        return redirect(url_for('index'))
    return render_template('chatroom.html', name=name, room=room)
