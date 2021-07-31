from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
	'''частота обновления страниц статей и степень совпадения с тематикой сайта'''
	changefreq = 'weekly'
	priority = 0.9

	def items(self):
		'''выводит все посты'''
		return Post.published.all()

	def lastmod(self, obj):
		'''возвращает время оследней модификации статьи'''
		return obj.update