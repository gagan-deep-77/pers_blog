from django import template
from blog.models import Post
from django.contrib.auth.models import User
register = template.Library()


@register.simple_tag
def is_liked(post_id,liked_by):
    if liked_by.username == "":
        return "anon"
    post = Post.objects.get(id=post_id)
    
    if liked_by.blog_posts.filter(id=post_id).exists():
        return True
    return False