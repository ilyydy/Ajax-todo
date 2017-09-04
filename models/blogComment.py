from models import Model
from models.user import User
import time


class Blogcomment(Model):
    """
    评论类
    """

    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            'content',
            'blog_id',
            'user_id',
            'username',
        ]
        return names

    @classmethod
    def new(cls, form):
        m = super().new(form)
        m.created_time = int(time.time())
        m.save()
        return m

    def user(self):
        u = User.find_by(id=self.user_id)
        return u
