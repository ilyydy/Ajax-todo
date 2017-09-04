from routes import (
    current_user,
    same_user_required,
)
from flask import (
    jsonify,
    Blueprint,
    request,
)

from utils import log
from models.comment import Comment

main = Blueprint('comment_api', __name__)


@main.route('/all')
def all():
    comments = Comment.all_json()
    return jsonify(comments)


@main.route('/add', methods=['POST'])
def add():
    # 得到浏览器发送的表单, 浏览器用 ajax 发送 json 格式的数据过来
    # 用 json 函数来获取格式化后的 json 数据
    form = request.get_json()
    u = current_user()
    # 创建一个 comment
    form['user_id'] = u.id
    form['username'] = u.username
    t = Comment.new(form)
    # 把创建好的 comment 返回给浏览器
    return jsonify(t.json())


@main.route('/delete')
def delete():
    comment_id = int(request.args.get('id'))
    item = Comment.find(comment_id)
    if same_user_required(item):
        t = Comment.delete(comment_id)
        return jsonify(t.json())
    else:
        pass
