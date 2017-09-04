from flask import (
    jsonify,
    Blueprint,
    request,
    redirect,
    url_for,
    render_template,
)

from utils import log
from models.blog import Blog
from models.blogComment import Blogcomment
from routes import (
    current_user,
    login_required,
    same_user_required,
)

main = Blueprint('blog_api', __name__)


@main.route('/all')
def all():
    blogs = Blog.all_json()
    return jsonify(blogs)


@main.route('/add', methods=['POST'])
@login_required
def add():
    # 得到浏览器发送的表单, 浏览器用 ajax 发送 json 格式的数据过来
    # 用 json 函数来获取格式化后的 json 数据
    form = request.form
    log('form', form)
    u = current_user()
    f = form.to_dict()
    f['user_id'] = u.id
    # 创建一个 blog
    Blog.new(f)
    # 把创建好的 blog 返回给浏览器
    return redirect(url_for('blog.index'))


@main.route('/delete')
def delete():
    blog_id = int(request.args.get('id'))
    item = Blog.find(blog_id)
    if same_user_required(item):
        b = Blog.delete(blog_id)
        blogComments = Blogcomment.find_all(blog_id=str(blog_id))
        for bc in blogComments:
            Blogcomment.delete(bc.id)
        return jsonify(b.json())
    else:
        pass


@main.route('/update', methods=['POST'])
def update():
    form = request.form
    blog_id = int(request.args.get('id'))
    item = Blog.find(blog_id)
    if same_user_required(item):
        b = Blog.update(blog_id, form)
        return redirect(url_for('blog.detail', id=blog_id))
    else:
        pass


@main.route('/detail')
def detail():
    blog_id = int(request.args.get('id'))
    b = Blog.find(blog_id)
    log('load blog detail', b)
    if b is not None:
        return jsonify(b.json())
    # else：
    #     return redirect(url_for(''))


@main.route('/edit')
@login_required
def edit():
    """
    主页的处理函数, 返回主页的响应
    """
    blog_id = int(request.args.get('id'))
    item = Blog.find(blog_id)
    if same_user_required(item):
        return render_template('blog_edit.html', blog=item)
    else:
        pass
