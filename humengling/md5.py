# coding:utf-8
import hashlib
def to_md5(something):  #用md5值存储用户密码
    md5_obj=hashlib.md5()
    md5_obj.update(something)
    something_md5=md5_obj.hexdigest()
    return something_md5