# -*- coding: utf-8 -*-
import zh_cn
import sys
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required
from flask_login import current_user


class LoginForm(FlaskForm):
    """Accepts a nickname and a room."""
    name = StringField('用户', validators=[Required()])
    #name = current_user.username
    room = StringField('房间号', validators=[Required()])
    submit = SubmitField('进入聊天室')
