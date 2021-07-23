from django.urls import path
from . import views


app_name = 'blog' #определение пространства имен

urlpatterns = [
	
	path('', views.PostListView.as_view(), name='post_list'), # не принимает аргументов - только сопоставляется с обработчиком post_list
	path('<int:year>/<int:month>/<int:day>/<slug:post>/', 
		  views.post_detail, 
		  name='post_detail'),
	path('<int:post_id>/share/', views.post_share, name='post_share'),
	#вызывает post_detail и принимает параметры. "<>" - используется для извлечения значений из URLа.
]