from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('users/<str:username>/logout/', views.logout, name='logout'),
    path('users/<str:username>/', views.user, name='user'),
]
