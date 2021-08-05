from django.urls import path, include
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.contrib import admin


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('about',views.about,name='about' ),
    path('my_profile',views.my_profile,name='my-profile' ),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),
    
    path('profile/<int:pk>/', views.profile, name='profile'),
    
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('accounts/signup/', views.register, name='signup'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('follows/', views.follow_list, name='follow_list'),
    path('api/v1/',include('social_django.urls', namespace='social')),
   # url('', views.index),
    #path('users/friend-request/send/<int:id>/', views.send_friend_request, name='send_friend_request'),
    #path('users/friend-request/cancel/<int:id>/', views.cancel_friend_request, name='cancel_friend_request'),
    #path('users/friend-request/accept/<int:id>/', views.accept_friend_request, name='accept_friend_request'),
    #path('users/friend-request/delete/<int:id>/', views.delete_friend_request, name='delete_friend_request'),
    #path('users/friend/delete/<int:id>/', views.delete_friend, name='delete_friend'),
    path('follow/<int:user>',views.follow , name='follow'),
    path('unfollow/<int:user>',views.unfollow, name='unfollow'),
    path('feed', views.feed, name='feed')
]
