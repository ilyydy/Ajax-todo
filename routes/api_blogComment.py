from routes import (
    current_user,
    login_required,
    same_user_required,
)
from flask import (
    jsonify,
    Blueprint,
    request,
)

from utils import log
from models.blogComment import Blogcomment

main = Blueprint('blogComment_api', __name__)


@main.route('/all')
def all():
    blogComments = Blogcomment.all_json()
    return jsonify(blogComments)


@main.route('/add', methods=['POST'])
@login_required
def add():
    # 得到浏览器发送的表单, 浏览器用 ajax 发送 json 格式的数据过来
    # 用 json 函数来获取格式化后的 json 数据
    form = request.get_json()
    log('blogComment form', form)
    u = current_user()
    # 创建一个 comment
    form['user_id'] = u.id
    form['username'] = u.username
    bt = Blogcomment.new(form)
    # 把创建好的 comment 返回给浏览器
    return jsonify(bt.json())


@main.route('/delete')
def delete():
    blogComment_id = int(request.args.get('id'))
    item = Blogcomment.find(blogComment_id)
    if same_user_required(item):
        bt = Blogcomment.delete(blogComment_id)
        return jsonify(bt.json())
    else:
        pass
