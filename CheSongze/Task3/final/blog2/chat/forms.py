# -*- coding: utf-8 -*-
import zh_cn
import sys
from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required


class LoginForm(Form):
    """Accepts a nickname and a room."""
    name = StringField('用户', validators=[Required()])
    room = StringField('房间号', validators=[Required()])
    submit = SubmitField('进入聊天室')
