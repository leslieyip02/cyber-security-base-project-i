from django.urls import path
from .views import homePageView, loginView, signupView, logoutView

urlpatterns = [
    path('', homePageView, name='home'),
    path('login/', loginView, name='login'),
    path('signup/', signupView, name='signup'),
    path('logout/', logoutView, name='logout'),
]
