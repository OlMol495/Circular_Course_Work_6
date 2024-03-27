from django.core.cache import cache
from django.conf import settings

from blog.models import Post

def get_cached_post():
    if settings.CACHE_ENABLED:
        key = 'post_list'
        post_list = cache.get(key)
        if post_list is None:
            post_list = Post.objects.all()
            cache.set(key, post_list)
    else:
        post_list = Post.objects.all()
    return post_list
