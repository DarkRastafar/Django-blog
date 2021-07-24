from django.contrib import admin
from .models import Post, Comment


@admin.register(Post) # делает то же самое, что и admin.site.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'author', 'publish', 'status')
	list_filter = ('status', 'created', 'publish', 'author') # поля фильтра
	search_fields = ('title', 'body') # строка поиска
	prepopulated_fields = {'slug': ('title',)}
	raw_id_fields = ('author',)
	date_hierarchy = 'publish' #Добавление ссылок для навигации по датам в фильтре
	ordering = ('status', 'publish') # сортировка по умолчанию
	#count_likes = ('',)

# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'post', 'created', 'active')
	list_filter = ('active', 'created', 'update')
	search_fields = ('name', 'email', 'body')