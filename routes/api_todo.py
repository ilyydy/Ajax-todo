from flask import (
    jsonify,
    Blueprint,
    request,
)

from utils import log
from models.todo import Todo
from html import escape

main = Blueprint('todo_api', __name__)


@main.route('/all')
def all():
    todos = Todo.all_json()
    return jsonify(todos)


@main.route('/add', methods=['POST'])
def add():
    # 得到浏览器发送的表单, 浏览器用 ajax 发送 json 格式的数据过来
    # 用 json 函数来获取格式化后的 json 数据
    form = request.get_json()
    # 创建一个 todo
    form['task'] = escape(form['task'])
    t = Todo.new(form)
    # 把创建好的 todo 返回给浏览器
    return jsonify(t.json())


@main.route('/delete', methods=['GET'])
def delete():
    todo_id = int(request.args.get('id'))
    t = Todo.delete(todo_id)
    return jsonify(t.json())


@main.route('/update', methods=['POST'])
def update():
    form = request.get_json()
    todo_id = int(form.get('id'))
    t = Todo.update(todo_id, form)
    return jsonify(t.json())
