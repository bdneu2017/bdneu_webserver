# -*- coding: utf-8 -*-
import zh_cn
from flask import session
from flask_socketio import emit, join_room, leave_room, close_room, disconnect
from .. import socketio
import time
from flask_login import current_user

users=[]

@socketio.on('joined', namespace='/chatroom')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = '1'#session.get('room')
    join_room(room)
    if current_user.login not in users:
        users.append(current_user.login)
        strusers=''
        for user in users:
            strusers+=str(user)+'\n'
        emit('status', {'msg': str(current_user.login) + ' 进入了聊天室。','users':strusers}, room=room)


@socketio.on('text', namespace='/chatroom')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = '1'#session.get('room')
    emit('message', {'msg': '  '+message['msg'],'time':str(current_user.login) +'  ' + time.strftime("%H:%M:%S", time.localtime()) }, room=room)


@socketio.on('left', namespace='/chatroom')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = '1'#session.get('room')
    leave_room(room)
    if current_user.login in users:
        users.remove(current_user.login)
        strusers=''
        for user in users:
            strusers+=str(user)+'\n'
        emit('status', {'msg': str(current_user.login) + ' 离开了聊天室。','users':strusers}, room=room)

@socketio.on('disconnect', namespace='/chatroom')
def discon():
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = '1'#session.get('room')
    #leave_room(room)
    disconnect()
    if current_user.login in users:
        users.remove(current_user.login)
        strusers=''
        for user in users:
            strusers+=str(user)+'\n'
        emit('status', {'msg': str(current_user.login) + ' 离开了聊天室。','users':strusers}, room=room)