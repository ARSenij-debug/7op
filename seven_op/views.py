from django.shortcuts import render
from .models import Category, UploadedPhoto, UploadedFile, Post, Blog, BlogAuthor, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm, RegistrationForm, SearchForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from itertools import chain
import datetime
import django


# Create your views here.


def common_search(request):
    ret = dict()
    ret['url'] = False
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            ret['url'] = reverse('my_search_result', args=(str(query),))
    else:
        proposed_data = ''
        ret['form'] = SearchForm(initial={'data': proposed_data})
    return ret


def search_results(request, pk):
    """
    отображает результаты поиска
    :param request:
    :return:
    """
    search_result = common_search(request)
    if search_result['url']:
        return HttpResponseRedirect(search_result['url'])
    categories = Category.objects.all()
    active = 0
    recent_blogs = Blog.objects.all()
    recent_blogs = recent_blogs[0:min(len(recent_blogs), 5)]
    needed_blogs = Blog.objects.filter(title__contains=pk)
    needed_posts = Post.objects.filter(title__contains=pk)
    search_list = sorted(chain(needed_posts, needed_blogs), key=lambda instance: instance.date, reverse=True)
    title = "7Мнений - Поиск"
    paginator = Paginator(search_list, 21, allow_empty_first_page=True)
    page = request.GET.get('page')
    try:
        needed_search_list = paginator.page(page)
    except PageNotAnInteger:
        needed_search_list = paginator.page(1)
    except EmptyPage:
        needed_search_list = paginator.page(paginator.num_pages)

    count = len(search_list)
    count10 = count % 10
    if count10 == 0:
        count10 = 10

    return render(request,
                  'show_search_result.html',
                  context={'categories': categories,
                           'active': active,
                           'recent_blogs': recent_blogs,
                           'page_title': title,
                           'search_list': needed_search_list,
                           'count': count,
                           'count10': count10,
                           'search_form': search_result['form']})


def main(request):
    """
    отображает главную страницу
    :param request:
    :return:
    """
    search_result = common_search(request)
    if search_result['url']:
        return HttpResponseRedirect(search_result['url'])
    posts = Post.objects.all()
    paginator = Paginator(posts, 21, allow_empty_first_page=True)
    page = request.GET.get('page')
    try:
        needed_posts = paginator.page(page)
    except PageNotAnInteger:
        needed_posts = paginator.page(1)
    except EmptyPage:
        needed_posts = paginator.page(paginator.num_pages)
    categories = Category.objects.all()
    active = 0
    recent_blogs = Blog.objects.all()
    recent_blogs = recent_blogs[0:min(len(recent_blogs), 5)]

    return render(request,
                  'main_page_template.html',
                  context={'posts': needed_posts,
                           'categories': categories,
                           'active': active,
                           'recent_blogs': recent_blogs,
                           'page_title': '7Мнений - Главная',
                           'search_form': search_result['form']})


def show_category(request, pk):
    """
    отображает посты в выбранной категории
    :param request:
    :param pk: name_url категории для отображения
    :return:
    """
    search_result = common_search(request)
    if search_result['url']:
        return HttpResponseRedirect(search_result['url'])
    categories = Category.objects.all()
    needed_category = Category.objects.get(name_url__exact=pk)
    posts = Post.objects.filter(category__name_url__exact=pk)
    paginator = Paginator(posts, 21, allow_empty_first_page=True)
    page = request.GET.get('page')
    try:
        needed_posts = paginator.page(page)
    except PageNotAnInteger:
        needed_posts = paginator.page(1)
    except EmptyPage:
        needed_posts = paginator.page(paginator.num_pages)
    title = "7Мнений - " + str(needed_category.name_plur)
    active = needed_category.id
    recent_blogs = Blog.objects.all()
    recent_blogs = recent_blogs[:min(len(recent_blogs), 5)]

    return render(request,
                  'show_category_template.html',
                  context={'posts': needed_posts,
                           'categories': categories,
                           'needed_category': needed_category,
                           'active': active,
                           'recent_blogs': recent_blogs,
                           'page_title': title,
                           'search_form': search_result['form']})


def show_post(request, pk):
    """
    отображает выбранный пост
    :param request:
    :param pk: id выбранного поста
    :return:
    """
    search_result = common_search(request)
    if search_result['url']:
        return HttpResponseRedirect(search_result['url'])
    categories = Category.objects.all()
    recent_blogs = Blog.objects.all()
    recent_blogs = recent_blogs[:min(len(recent_blogs), 5)]
    needed_post = Post.objects.get(id__exact=pk)
    active = needed_post.category.id
    comments = needed_post.comments.all()
    paginator = Paginator(comments, 5, allow_empty_first_page=True)
    page = request.GET.get('page')
    try:
        needed_comments = paginator.page(page)
    except PageNotAnInteger:
        needed_comments = paginator.page(1)
    except EmptyPage:
        needed_comments = paginator.page(paginator.num_pages)
    photos = needed_post.photos_for_spin.order_by('index').all()
    files = needed_post.attached_files.all()
    title = "7Мнений - Публикация"

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            user_comment = Comment()
            user_comment.data = form.cleaned_data['data']
            user_comment.author = request.user.get_username()
            user_comment.save()
            user_comment.data = datetime.datetime.now()
            needed_post.comments.add(user_comment)
            needed_post.save()
            return HttpResponseRedirect(needed_post.get_url_for_show())
    else:
        proposed_data = ''
        form = CommentForm(initial={'data': proposed_data})

    return render(request, 'show_post_template.html',
                  context={'post': needed_post,
                           'categories': categories,
                           'active': active,
                           'recent_blogs': recent_blogs,
                           'comments': needed_comments,
                           'page_title': title,
                           'photos_for_spin': photos,
                           'files': files,
                           'form': form,
                           'search_form': search_result['form']})


def show_blog(request, pk):
    """
    отображает выбранный блог
    :param request:
    :param pk:
    :return:
    """
    search_result = common_search(request)
    if search_result['url']:
        return HttpResponseRedirect(search_result['url'])
    categories = Category.objects.all()
    recent_blogs = Blog.objects.all()
    recent_blogs = recent_blogs[:min(len(recent_blogs), 5)]
    needed_blog = Blog.objects.get(id__exact=pk)
    active = "blog"
    comments = needed_blog.comments.all()
    paginator = Paginator(comments, 5, allow_empty_first_page=True)
    page = request.GET.get('page')
    try:
        needed_comments = paginator.page(page)
    except PageNotAnInteger:
        needed_comments = paginator.page(1)
    except EmptyPage:
        needed_comments = paginator.page(paginator.num_pages)
    photos = needed_blog.photos_for_spin.order_by('index').all()
    files = needed_blog.attached_files.all()
    title = "7Мнений - Блог"

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            user_comment = Comment()
            user_comment.data = form.cleaned_data['data']
            user_comment.author = request.user.get_username()
            user_comment.save()
            user_comment.data = datetime.datetime.now()
            needed_blog.comments.add(user_comment)
            needed_blog.save()
            return HttpResponseRedirect(needed_blog.get_url_for_show())
    else:
        proposed_data = ''
        form = CommentForm(initial={'data': proposed_data})

    return render(request,
                  'show_blog_template.html',
                  context={'blog': needed_blog,
                           'categories': categories,
                           'active': active,
                           'recent_blogs': recent_blogs,
                           'comments': needed_comments,
                           'page_title': title,
                           'photos_for_spin': photos,
                           'files': files,
                           'form': form,
                           'search_form': search_result['form']})


def show_blog_authors(request):
    """
    отображает страницу со всеми авторами блогов
    :param request:
    :return:
    """
    search_result = common_search(request)
    if search_result['url']:
        return HttpResponseRedirect(search_result['url'])
    categories = Category.objects.all()
    recent_blogs = Blog.objects.all()
    recent_blogs = recent_blogs[:min(len(recent_blogs), 5)]
    authors = BlogAuthor.objects.all()
    paginator = Paginator(authors, 10, allow_empty_first_page=True)
    page = request.GET.get('page')
    try:
        needed_authors = paginator.page(page)
    except PageNotAnInteger:
        needed_authors = paginator.page(1)
    except EmptyPage:
        needed_authors = paginator.page(paginator.num_pages)
    title = "7Мнений - Авторы блогов"
    active = "blog"

    return render(request,
                  'show_blog_authors_template.html',
                  context={'authors': needed_authors,
                           'categories': categories,
                           'active': active,
                           'recent_blogs': recent_blogs,
                           'page_title': title,
                           'search_form': search_result['form']})


def show_blogs_for_author(request, pk):
    """
    отображает все блоги автора
    :param request:
    :param pk:
    :return:
    """
    search_result = common_search(request)
    if search_result['url']:
        return HttpResponseRedirect(search_result['url'])
    categories = Category.objects.all()
    recent_blogs = Blog.objects.all()
    recent_blogs = recent_blogs[:min(len(recent_blogs), 5)]
    author = BlogAuthor.objects.get(id__exact=pk)
    blogs = Blog.objects.filter(author__id__exact=pk)
    paginator = Paginator(blogs, 10, allow_empty_first_page=True)
    page = request.GET.get('page')
    try:
        needed_blogs = paginator.page(page)
    except PageNotAnInteger:
        needed_blogs = paginator.page(1)
    except EmptyPage:
        needed_blogs = paginator.page(paginator.num_pages)
    active = "blog"
    title = "7Мнений - страница автора"

    return render(request,
                  'show_blogs_for_author.html',
                  context={'author': author,
                           'blogs': needed_blogs,
                           'categories': categories,
                           'active': active,
                           'recent_blogs': recent_blogs,
                           'page_title': title,
                           'search_form': search_result['form']})


def user_registration(request):
    """
    отрисовывает страничку регистрации
    :param request:
    :return:
    """
    search_result = common_search(request)
    if search_result['url']:
        return HttpResponseRedirect(search_result['url'])
    categories = Category.objects.all()
    recent_blogs = Blog.objects.all()
    recent_blogs = recent_blogs[:min(len(recent_blogs), 5)]
    active = "registration"
    page_title = "7Мнений - Регистрация"
    error_massage = ""

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                new_user = User.objects.create_user(username=form.cleaned_data['user_name'],
                                                password=form.cleaned_data['user_password'])
                new_user.save()
            except django.db.utils.IntegrityError:
                error_massage = "это имя уже занято, придумайте другое"
                return render(request,
                              'registration_template.html',
                              context={'recent_blogs': recent_blogs,
                                       'active': active,
                                       'page_title': page_title,
                                       'categories': categories,
                                       'form': form,
                                       'error_massage': error_massage})

            return HttpResponseRedirect(reverse('login'))
    else:
        form = RegistrationForm()

    return render(request,
                  'registration_template.html',
                  context={'recent_blogs': recent_blogs,
                           'active': active,
                           'page_title': page_title,
                           'categories': categories,
                           'form': form,
                           'error_massage': error_massage,
                           'search_form': search_result['form']})


def show_contacts(request):
    """
    отрисовывает страницу контактов
    :param request:
    :return:
    """
    search_result = common_search(request)
    if search_result['url']:
        return HttpResponseRedirect(search_result['url'])
    categories = Category.objects.all()
    recent_blogs = Blog.objects.all()
    recent_blogs = recent_blogs[:min(len(recent_blogs), 5)]
    active = "contacts"
    page_title = "7Мнений - Контакты"

    return render(request,
                  'show_contacts_template.html',
                  context={'recent_blogs': recent_blogs,
                           'active': active,
                           'categories': categories,
                           'page_title': page_title,
                           'search_form': search_result['form']})
