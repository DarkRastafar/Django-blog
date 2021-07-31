tags = TaggableManager() # <---Чтобы подружить эту херь с django 3+ - пришлось создавать 
	#в django.utils - "six.py" (исходники отрыл в аналах документации по древнему djando)
	#а так же патчить django.utils.encoding.py ибо данная библиотека наотрез отказалась 
	#работать без python_2_unicode_compatible, писать импорт "six" в managers.py в корне taggit, а так же - 
<<<<<<< HEAD
	#97 строка C:\Program Files (x86)\Python38-32\Lib\site-packages\django\forms - закоментил renderer, ибо -
	renderer=None - нагло игнорилось, т.к. там renderer принимает значение из экземпляра 
	(class BoundField, def as_widget).


=======
	#97 строка C:\Program Files (x86)\Python38-32\Lib\site-packages\django\forms\boundfield.py - закоментил renderer, ибо -
	renderer=None - нагло игнорилось, т.к. там renderer принимает значение из экземпляра жопы единорога...
	(class BoundField, def as_widget).
	
>>>>>>> b52c468ed2b2e40a5b7bb7b4718900ac132fa1fe
vievs.py	
post_list - рендерит статьи блога + пагинатор + теги.
post_detail - рендерит комменты + форму комментов + рекомендацию похожих статей по тегам.
post_share - собсна функция для того, чтобы отправлять на мыло ссылку на статью и меседж. рендерит форму отправки.

models.py
PublishedManager - Апдейтнутый QuerySet обработчик (фильтр по публикации).
Post - Таблица постов.
get_absolute_url - создание URL из данных статьи.
<<<<<<< HEAD
Comment - Таблица комментов.
=======
Comment - Таблица комментов.

>>>>>>> b52c468ed2b2e40a5b7bb7b4718900ac132fa1fe
