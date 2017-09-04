from models.user import User

from flask import (
    Blueprint,
    request,
    render_template,
    url_for,
    session,
    redirect,
)
from utils import log

main = Blueprint('api_user', __name__)


@main.route('/login', methods=['POST'])
def login():
    """
    登录页面的路由函数
    """
    form = request.form
    u = User.new(form)
    u = u.validateLogin_user()
    if u is not None:
        session['user_id'] = u.id
        session.permanent = True
        resp = redirect(url_for('home.index'))

        # 登录后定向到 /
        return resp
    else:
        return redirect(url_for('user.login'))


@main.route('/register', methods=['POST'])
def register():
    """
    注册页面的路由函数
    """
    form = request.form
    u = User.new(form)
    if u.validate_register():
        # 注册成功再保存
        u.save()
        # 注册成功后 定向到登录页面
        return redirect(url_for('user.login'))
    else:
        # 注册失败 定向到注册页面
        return redirect(url_for('user.register'))
