from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.
class PublishedManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(status='published') # возвращает QuerySet с фильтром


class Post(models.Model):
	STATUS_CHOICES = {
		('draft', 'Draft'),
		('published', 'Published'),
	}
	title = models.CharField(max_length=250) #заголовок статьи (VARCHAR тип)
	slug = models.SlugField(max_length=250, unique_for_date='publish') # поле для формирования семантических URLов статей
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post') # собсна автор, отношение "Один ко многим" автор может иметь много статей
	body = models.TextField() # содержание статьи
	publish = models.DateTimeField(default=timezone.now) # сохраняет дату публикации статьи
	created = models.DateTimeField(auto_now_add=True) # собсна указывает на дату создания статьи (auto_now_add=True - сохраняет автоматически при сохранении объекта)
	update  = models.DateTimeField(auto_now=True) # дата и время редактирования статьи (auto_now=True - сохраняет автоматически при сохранении объекта)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft') # статус статьи. Choices - для выбора статуса.
	objects = models.Manager() # описание менеджера
	published = PublishedManager() # добавление нового менеджера в модель
	tags = TaggableManager() # <---'''чтобы подружить эту херь с django 3+ - пришлось создавать 
	#в django.utils - "six.py" (исходники отрыл в аналах документации по древнему djando)
	#а так же патчить django.utils.encoding.py ибо данная библиотека наотрез отказалась 
	#работать без python_2_unicode_compatible, писать импорт "six" в managers.py в корне taggit, а так же - 
	#97 строка C:\Program Files (x86)\Python38-32\Lib\site-packages\django\forms - закоментил renderer'''

	class Meta:
		ordering = ('-publish',) # метаданные для порядка сортировки (по убыванию) (разумеется по убыванию даты публикации)

	def __str__(self):
		return self.title # это чтобы выводил текст, а не цифровую ссылку на объект


	def get_absolute_url(self):
		return reverse('blog:post_detail',
						args=[self.publish.year,
								self.publish.month,
								self.publish.day,
								self.slug])


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') #related_names - доступ к комментам конкретной статьи
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	update = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True) # чтобы была возможность скрывать матерные комменты.

	class Meta:
		ordering = ('created',)

	def __str__(self):
		return 'Comment by {} on {}'.format(self.name, self.post)


