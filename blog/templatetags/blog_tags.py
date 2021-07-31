from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import Post


register = template.Library()

@register.simple_tag
def total_posts():
	return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
	'''выводит пять последних постов, отсортированных по убыванию'''
	latest_posts = Post.published.order_by('-publish')[:count]
	return {'latest_posts' : latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
	'''выводит пять самых залайканных постов, отсортированных по убыванию'''
	return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
	return mark_safe(markdown.markdown(text)) #mark_safe - помечает return как разрешенный HTML-код