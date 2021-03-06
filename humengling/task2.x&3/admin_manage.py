# coding:utf-8
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from users_class import User
from app import app, db
from words import Word, FilterWord, top_keys, AlertMailBox
from flask_login import current_user


class MyView1(ModelView):  # 用户管理 可以创建
    def is_accessible(self):
        if current_user.is_authenticated and current_user.role.name == 'Admin':
            return True
        return False

    def on_model_change(self, form, User, is_created):
        User.password = form.password_hash.data

    column_labels = dict(
        username=u'用户名',
        password_hash=u'密码散列（创建时填入密码即可）',
        role=u'用户级别',
        word=u'留言')


class MyView2(ModelView):  # 留言管理 不能创建 （觉得在后台创建留言没有意义）
    def is_accessible(self):
        if current_user.is_authenticated and current_user.role.name == 'Admin':
            return True
        return False
    can_create = False

    column_labels = dict(
        time_now=u'时间',
        title=u'标题',
        content=u'内容',
        user=u'用户名')


class FilterView(ModelView):  # 关键字管理 可创建 times创建初始值应为0
    def is_accessible(self):
        if current_user.is_authenticated and current_user.role.name == 'Admin':
            return True
        return False
    column_labels = dict(key=u'关键字', times=u'出现次数', alert=u'是否告警（1：是 0：否）')


class TopKeyView(BaseView):  # 关键字top3 只是显示 无操作
    def is_accessible(self):
        if current_user.is_authenticated and current_user.role.name == 'Admin':
            return True
        return False

    @expose('/')
    def top_key(self):
        top_3 = top_keys()
        return self.render('top_key.html', top_3=top_3)


class AlertMailView(ModelView):  # 告警邮箱 不能创建不能删除 （一个告警邮箱, 仅限编辑）
    def is_accessible(self):
        if current_user.is_authenticated and current_user.role.name == 'Admin':
            return True
        return False
    can_create = False
    can_delete = False
    column_labels = dict(mail=u'告警邮箱')


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.role.name == 'Admin':
            return True
        return False


admin = Admin(app, name=u'后台管理系统', index_view=MyAdminIndexView())
admin.add_view(MyView1(User, db.session, name=u'管理账号'))
admin.add_view(MyView2(Word, db.session, name=u'管理留言'))
admin.add_view(FilterView(FilterWord, db.session, name=u'过滤关键字'))
admin.add_view(TopKeyView(name=u'关键字top3'))
admin.add_view(AlertMailView(AlertMailBox, db.session, name=u'告警邮箱配置'))
