from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.main, name='main'),
    url(r'^show_category/(?P<pk>[-\w]+)$', views.show_category, name='show_category'),
    url(r'^show_post/(?P<pk>\d+)$', views.show_post, name='show_post'),
    url(r'^show_blog/(?P<pk>\d+)$', views.show_blog, name='show_blog'),
    url(r'^show_blog_authors/$', views.show_blog_authors, name='show_blog_authors'),
    url(r'^show_blogs_for_author/(?P<pk>\d+)$', views.show_blogs_for_author, name='show_blogs_for_author'),
    url(r'^registration', views.user_registration, name='registration'),
    url(r'^contacts', views.show_contacts, name='contacts'),
    url(r'search_result/(?P<pk>[-\w]+)$', views.search_results, name='my_search_result')
]
