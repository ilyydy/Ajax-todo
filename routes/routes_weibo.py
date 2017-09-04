from flask import (
    render_template,
    Blueprint,
)
from routes import login_required

# 创建一个蓝图对象
# 路由都定义在蓝图对象中
# 然后再 flask 主代码中 注册蓝图 来使用
main = Blueprint('weibo', __name__)


@main.route('/index')
@login_required
def index():
    """
    主页的处理函数, 返回主页的响应
    """
    return render_template('weibo_index.html')
