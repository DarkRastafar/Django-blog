from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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


