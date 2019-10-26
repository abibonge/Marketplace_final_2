from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.accountshome, name='accounts_home'),
    path('login', views.login, name='login_page'),
    path('register', views.register, name='register_page'),
    path('logout', views.logout, name='logout_page'), #send back to home
    
]
