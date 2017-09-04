from flask import Flask
from flask_bootstrap import Bootstrap
from datetime import timedelta
from routes.routes_static import main as home_view
from routes.routes_user import main as user_view
from routes.routes_todo import main as todo_view
from routes.routes_weibo import main as weibo_view
from routes.routes_blog import main as blog_view
from routes.api_user import main as user_api
from routes.api_todo import main as todo_api
from routes.api_weibo import main as weibo_api
from routes.api_comment import main as comment_api
from routes.api_blog import main as blog_api
from routes.api_blogComment import main as blogComment_api
from conf import secret_key


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = secret_key
app.permanent_session_lifetime = timedelta(minutes=5)
# 注册路由
app.register_blueprint(home_view)
app.register_blueprint(user_view)
app.register_blueprint(blog_view, url_prefix='/blog')
app.register_blueprint(todo_view, url_prefix='/todo')
app.register_blueprint(weibo_view, url_prefix='/weibo')
app.register_blueprint(user_api, url_prefix='/api/user')
app.register_blueprint(todo_api, url_prefix='/api/todo')
app.register_blueprint(weibo_api, url_prefix='/api/weibo')
app.register_blueprint(comment_api, url_prefix='/api/comment')
app.register_blueprint(blog_api, url_prefix='/api/blog')
app.register_blueprint(blogComment_api, url_prefix='/api/blogComment')


if __name__ == '__main__':
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2000,
    )

    app.run(**config)
