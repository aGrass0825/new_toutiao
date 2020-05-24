from flask import g, current_app
from functools import wraps
from sqlalchemy.orm import load_only
from sqlalchemy.exc import SQLAlchemyError


from models import db


def set_db_to_read(func):
    """
    设置使用读数据库
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        db.session().set_to_read()
        return func(*args, **kwargs)
    return wrapper


def set_db_to_write(func):
    """
    设置使用写数据库
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        db.session().set_to_write()
        return func(*args, **kwargs)
    return wrapper


def login_required(func):
    """
    验证是否为登录用户，只有登录用户才能访问视图函数
    :param func: 视图函数
    :return:
    """
    def wrapper(*args, **kwargs):
        if g.user_id is not None and g.use_refresh_token is False:  # g.use_refresh_token is False保证是普通token，而不是刷新token
            return func(*args, **kwargs)
        else:
            return {'message': 'Invalid token'}  # 无效的token

    return wrapper