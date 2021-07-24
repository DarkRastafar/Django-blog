tags = TaggableManager() # <---Чтобы подружить эту херь с django 3+ - пришлось создавать 
	#в django.utils - "six.py" (исходники отрыл в аналах документации по древнему djando)
	#а так же патчить django.utils.encoding.py ибо данная библиотека наотрез отказалась 
	#работать без python_2_unicode_compatible, писать импорт "six" в managers.py в корне taggit, а так же - 
	#97 строка C:\Program Files (x86)\Python38-32\Lib\site-packages\django\forms - закоментил renderer, ибо -
	renderer=None - нагло игнорилось, т.к. там renderer принимает значение из экземпляра 
	(class BoundField, def as_widget).