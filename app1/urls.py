from django.conf.urls import url
from app1 import views
from django.urls import path
from .views import CreateThread, ListThreads, ThreadView, CreateMessage, sending_msg, friendcreatethread

urlpatterns = [
    # url('hello',views.greetings),
    url('logout',views.userLogout),
    url('login',views.login_page),
    url('sign-up',views.sign_up_page),
    url('home',views.home),
    url('friendposts',views.friendposts),
    url('confirmation',views.confirm),
    url('addpost',views.addpost),
    url('mypost',views.mypost,name='mypost'),
    url('add',views.add),
    url('upload',views.upload),
    url('likepost/(?P<post_id>\w+)/(?P<username>\w+)/$',views.like_post),
    url('Mylikes_post/(?P<post_id>\w+)/(?P<username>\w+)/$',views.Mylikes_post),
    url('Unlikeposts/(?P<post_id>\w+)/(?P<username>\w+)/$',views.unlike_post),
    url('MyUnlikesposts/(?P<post_id>\w+)/(?P<username>\w+)/$',views.MyUnlikesposts),
    # url('likepost',views.like_post),
    url('search',views.search,name='search'),
    url('insertcomment/(?P<post_id>\w+)/$',views.newcomment),
    url('deletepost/(?P<post_id>\w+)/$',views.deletepost),
    # url('Myinsertescomment/(?P<post_id>\w+)/$',views.Myinsertescomment),
    url('comment_new/(?P<post_id>\w+)/$',views.commentview),
    url('follow',views.follow,name='follow'),
    url('accept',views.accept,name='accept'),
    url('decline',views.decline,name='decline'),
    url('deleted_friend',views.delete_friend,name='deleted_friend'),
    url('view_click/(?P<username>\w+)/$',views.admin_view),
    url('post_view/(?P<post_id>\w+)/$',views.post_view),
    url('block/(?P<username>\w+)/$',views.block),
    url('profilepic',views.profile_pic),
    url('prof_pic',views.prof_pic),
    url('landingPage',views.landingPage),
    url('findfriend',views.findfriend),
    url('addFriendclick/(?P<username>\w+)/$',views.addFriendclick),
    url('clickingfriends/(?P<username>\w+)/$',views.clickingfriends),
    url('viewCluster/(?P<post_id>\w+)/$',views.viewCluster),
    url('adminHome',views.adminHome),
    url('notifications',views.notifications),
    url('usernotification',views.usernotification),
    url('ViewFriends/(?P<username>\w+)/$', views.ViewFriends),
    url('inbox/', ListThreads.as_view(), name='inbox'),
    url('create-thread/', CreateThread.as_view(), name='create-thread'),
    url('friendsthread/', friendcreatethread.as_view(), name='friendsthread'),
    url('thread/(?P<pk>\d+)/', ThreadView.as_view(), name='thread'),
    url('create-message/(?P<pk>\d+)/', CreateMessage.as_view(), name='create-message'),
    url('Addnotification/', views.Addnotification),
    url('sending_msg/', sending_msg.as_view(), name='sending_msg'),

]
 