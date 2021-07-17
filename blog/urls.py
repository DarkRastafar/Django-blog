from django.urls import path
from . import views


app_name = 'blog' #определение пространства имен

urlpatterns = [
	
	path('', views.post_list, name='post_list'), # не принимает аргументов - только сопоставляется с обработчиком post_list
	path('<int:year>/<int:month>/<int:day>/<slug:post>/', 
		  views.post_detail, 
		  name='post_detail'),
	#вызывает post_detail и принимает параметры. "<>" - используется для извлечения значений из URLа.
]