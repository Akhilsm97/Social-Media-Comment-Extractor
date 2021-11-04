from django.conf.urls import url
from app1 import views
from django.urls import path
from .views import CreateThread, ListThreads, ThreadView, CreateMessage


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
    url('comment_new/(?P<post_id>\w+)/$',views.commentview),
    url('follow',views.follow,name='follow'),
    url('accept',views.accept,name='accept'),
    url('decline',views.decline,name='decline'),
    url('view_click/(?P<username>\w+)/$',views.admin_view),
    url('post_view/(?P<post_id>\w+)/$',views.post_view),
    url('block/(?P<username>\w+)/$',views.block),
    url('profilepic',views.profile_pic),
    url('prof_pic',views.prof_pic),
    url('landingPage',views.landingPage),
    url('findfriend',views.findfriend),
    url('addFriendclick/(?P<username>\w+)/$',views.addFriendclick),
    url('viewCluster/(?P<post_id>\w+)/$',views.viewCluster),
    url('adminHome',views.adminHome),
    url('inbox/', ListThreads.as_view(), name='inbox'),
    url('inbox/create-thread/', CreateThread.as_view(), name='create-thread'),
    url('inbox/<int:pk>/', ThreadView.as_view(), name='thread'),
    url('inbox/<int:pk>/create-message/', CreateMessage.as_view(), name='create-message'),
]
 