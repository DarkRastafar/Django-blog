from django.urls import path
from .feeds import LatestPostsFeed
from . import views


app_name = 'blog' #определение пространства имен

urlpatterns = [
	
	path('', views.post_list, name='post_list'),
	path('<int:year>/<int:month>/<int:day>/<slug:post>/', 
		  views.post_detail, name='post_detail'),
	path('<int:post_id>/share/', views.post_share, name='post_share'),
	path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),#вызывает post_detail и принимает параметры. "<>" - используется для извлечения значений из URLа.
	path('feed/', LatestPostsFeed(), name='post_feed'),
]