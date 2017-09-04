from routes import current_user
from flask import (
    Blueprint,
    render_template,
    request,
)
from utils import (
    log,
    get_location,
)

main = Blueprint('home', __name__)


@main.route('/')
def index():
    """
    主页的处理函数, 返回主页的响应
    """
    u = current_user()
    # request_ip = request.remote_addr
    # log('request location', get_location(request_ip))
    if u is None:
        username = 'Stranger'
    else:
        username = u.username
    return render_template('index.html', username=username)
