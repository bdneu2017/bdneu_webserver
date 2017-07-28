# coding:utf-8
from app import app
from flask_login import login_required, current_user
from flask import render_template
from flask_socketio import SocketIO, emit
socketio = SocketIO(app)


@app.route('/chat')
@login_required
def chat():  # 聊天页面
    return render_template('chat_online.html')


@socketio.on('my_event')
@login_required
def test_message(message):
    emit(
        'my_response',
        {'data': message['data'], 'username': current_user.username},
        broadcast=True)

