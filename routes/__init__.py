from models.user import User
from functools import wraps
from flask import (
    request,
    session,
    redirect,
)

from utils import log


def current_user():
    user_id = session.get('user_id', -1)
    log('user_id session', user_id)
    u = User.find(user_id)
    return u


def login_required(route_function):
    @wraps(route_function)
    def f(*args, **kwargs):
        u = current_user()
        if u is None:
            log('非登录用户')
            return redirect('/login')
        else:
            return route_function(*args, **kwargs)

    return f


def same_user_required(item):
    u = current_user()
    if u is None or u.id != item.user_id:
        log('没有权限', item)
        return False
    else:
        return True
