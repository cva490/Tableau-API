
from django.urls import path
from . import views


urlpatterns=[
    #path('',views.home, name='home'),
    path('',views.Login,name='Login'),
    path('home',views.home,name='Home'),
    path('logout',views.logout,name='logout'),
    path('publish',views.publish,name='publish'),
    path('published',views.submmitpublish,name='published'),
    path('users',views.submmitusers,name='users')
]

