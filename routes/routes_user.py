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

main = Blueprint('user', __name__)


@main.route('/login')
def login():
    """
    登录页面的路由函数
    """

    return render_template('login.html')


@main.route('/register')
def register():
    """
    注册页面的路由函数
    """

    return render_template('register.html')
