from django import template
from bboard.models import *


register = template.Library()


@register.inclusion_tag('bboard/list_replies.html')
def show_replies(sort=None, throught_slug=False, post_id=None):
    """Tag for show replies on view read post"""
    if throught_slug:
        post_id = Post.objects.get(slug=post_id).pk
    if post_id is not None:
        if not sort:
            replies = Reply.objects.filter(post=post_id, is_approved=True)
        else:
            replies = Reply.objects.filter(post=post_id, is_approved=True).order_by(sort)
        return {"replies": replies}
    else:
        return {"replies": {}}


@register.inclusion_tag('bboard/show_post.html')
def show_post(slug_post=None):
    """Tag for show post on view add reply"""
    if slug_post is not None:
        posts = Post.objects.filter(slug=slug_post, is_published=True)
        return {"posts": posts}
    else:
        return {"posts": {}}
