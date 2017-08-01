# -*- coding: utf-8 -*-
import zh_cn
from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
import time
from flask_login import current_user

@socketio.on('joined', namespace='/chatroom')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': str(current_user.login) + ' 进入了聊天室。'}, room=room)


@socketio.on('text', namespace='/chatroom')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': '  '+message['msg'],'time':str(current_user.login) +'  ' + time.strftime("%H:%M:%S", time.localtime()) }, room=room)


@socketio.on('left', namespace='/chatroom')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': str(current_user.login) + ' has left the room.'}, room=room)

