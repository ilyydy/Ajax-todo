import time

from models import Model
from utils import log


class Blog(Model):

    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            'title',
            'content',
            'author',
            'user_id'
        ]
        return names

    @classmethod
    def new(cls, form):
        m = super().new(form)
        t = int(time.time())
        m.created_time = t
        m.updated_time = t
        m.save()
        return m

    @classmethod
    def update(cls, id, form):
        m = super().update(id, form)
        log('blog update', m)
        m.updated_time = int(time.time())
        m.save()
        return m
