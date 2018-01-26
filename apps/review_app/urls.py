from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
  url(r'^$', views.index, name = "index"),
  url(r'^login$', views.user_login, name = "user_login"),
  url(r'^user/(?P<user_id>\d+)$', views.user_review, name = "user_review"),
  url(r'^user_create$',views.user_create, name = "user_create"),
  url(r'^add_book_get$',views.add_book_get, name = "add_book_get"),
  url(r'^add_book_post$',views.add_book_post, name = "add_book_post"),
  url(r'^book_review/(?P<book_id>\d+)$', views.book_review, name = "book_review")
  
]