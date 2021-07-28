from django.conf.urls import url
from app1 import views

urlpatterns = [
    # url('hello',views.greetings),
    url('logout',views.userLogout),
    url('login',views.login_page),
    url('sign-up',views.sign_up_page),
    url('home',views.home),
    url('confirmation',views.confirm),
    url('addpost',views.addpost),
    url('mypost',views.mypost,name='mypost'),
    url('add',views.add),
    url('upload',views.upload),
    url('likepost',views.like_post),
    url('search',views.search,name='search'),
    url('insertcomment/(?P<post_id>\w+)/$',views.newcomment),
    url('comment_new/(?P<post_id>\w+)/$',views.comment1),
]
