from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from .forms import EmailPostForm
from .models import Post

# Create your views here.
def post_list(request):
	object_list = Post.published.all()
	paginator = Paginator(object_list, 5) #Добавлю ка по 10 статей на страницу, вродь норм
	page = request.GET.get('page') #текущая страница
	try:
		posts = paginator.page(page) # список объектов на странице "метод page(), класса Paginator"
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	return render(request, 
				 'blog/post/list.html', 
				 {'page': page, 
				  'posts': posts})
	'''принимает на вход все статьи блога и с помощью функции render (принимает на вход: объект request,
	путь к шаблону и переменные контекста для этого шаблона) - формируем шаблон для списка статей  '''


def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
	return render(request,
                  'blog/post/detail.html',
                  {'post': post})
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
