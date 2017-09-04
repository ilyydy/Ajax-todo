from flask import (
    render_template,
    Blueprint,
)
from routes import (
    current_user,
    login_required,
    same_user_required,
)
# 创建一个蓝图对象
# 路由都定义在蓝图对象中
# 然后再 flask 主代码中 注册蓝图 来使用
main = Blueprint('blog', __name__)


@main.route('/index')
def index():
    """
    主页的处理函数, 返回主页的响应
    """
    return render_template('blog_index.html')


@main.route('/detail')
def detail():
    """
    主页的处理函数, 返回主页的响应
    """
    return render_template('blog_detail.html')


@main.route('/new')
@login_required
def new():
    """
    主页的处理函数, 返回主页的响应
    """
    return render_template('blog_new.html')
