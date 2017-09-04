from flask import (
    jsonify,
    Blueprint,
    request,
)

from utils import log
from models.weibo import Weibo
from models.comment import Comment
from routes import (
    current_user,
    login_required,
    same_user_required,
)

main = Blueprint('weibo_api', __name__)


@main.route('/all', methods=['GET'])
def all():
    weibos = Weibo.all_json()
    return jsonify(weibos)


@main.route('/add', methods=['POST'])
@login_required
def add():
    # 得到浏览器发送的表单, 浏览器用 ajax 发送 json 格式的数据过来
    # 用 json 函数来获取格式化后的 json 数据
    form = request.get_json()
    u = current_user()
    # 创建一个 weibo
    form['user_id'] = u.id
    form['username'] = u.username
    t = Weibo.new(form)
    # 把创建好的 weibo 返回给浏览器
    return jsonify(t.json())


@main.route('/delete', methods=['GET'])
def delete():
    weibo_id = int(request.args.get('id'))
    item = Weibo.find(weibo_id)
    if same_user_required(item):
        t = Weibo.delete(weibo_id)
        comments = Comment.find_all(weibo_id=str(weibo_id))
        for c in comments:
            Comment.delete(c.id)
        return jsonify(t.json())
    else:
        pass
