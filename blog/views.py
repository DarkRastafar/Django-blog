from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.db.models import Count
from .forms import EmailPostForm, CommentForm
from .models import Post, Comment
from taggit.models import Tag


def post_list(request, tag_slug=None):
	object_list = Post.published.all()
	tag = None

	if tag_slug:
		tag = get_object_or_404(Tag, slug=tag_slug)
		object_list = object_list.filter(tags__in=[tag])

	paginator = Paginator(object_list, 3)
	page = request.GET.get('page') #текущая страница
	try:
		posts = paginator.page(page) # список объектов на странице
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	return render(request, 
				 'blog/post/list.html', 
				 {'page': page, 
				  'posts': posts,
				  'tag' : tag})
	'''принимает на вход все статьи блога и с помощью функции render (принимает на вход: объект request,
	путь к шаблону и переменные контекста для этого шаблона) - формируем шаблон для списка статей  '''


def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

	
	comments = post.comments.filter(active=True) #список активных комментариев для статьи через QuerySet
	new_comment = None
	if request.method == 'POST':
		comment_form = CommentForm(data=request.POST) # юзер отправил коммент
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False) #даем создать комент, но не записываем в базу
			new_comment.post = post # завязываем коммент на статью
			new_comment.save() # собсна - сохраняем в бд.
	else:
		comment_form = CommentForm() #возвращаем форму, если GET запрос

	post_tags_ids = post.tags.values_list('id', flat=True) #values_list получает через QuerySet все id тегов статей
														   #flat=True - для вывода плоского списка из id-шников
	similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id) #все статьи с тегом, кроме текущей
	similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4] #агрегация до 4 значений

	return render(request,
                  'blog/post/detail.html',
                  {'post' : post, 'comments' : comments,
                   'new_comment' : new_comment, 'comment_form' : comment_form,
                   'similar_posts' : similar_posts,})
	'''обработчик страницы статьи. принимает на вход арг для получения статьи по слагу и дате.
	render - возвращает HTML - шаблон'''


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
	#Получение статьи по идентификатору
	post = get_object_or_404(Post, id=post_id, status='published')
	sent = False

	if request.method == 'POST':
		#форма была отправлена на сохранение
		form = EmailPostForm(request.POST)
		if form.is_valid():
			#Все прошло валидацию
			cd = form.cleaned_data
			#Отправка емейл почты
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'],post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
			send_mail(subject, message, 'admin@myblog.com', [cd['to']])
			sent = True
	else:
		form = EmailPostForm()
	return render(request, 'blog/post/share.html', {'post' : post, 'form' : form, 'sent' : sent})