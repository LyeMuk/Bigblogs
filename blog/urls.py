from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.loggin, name='login'),
    path('signup', views.signup, name="signup"),
    path('home', views.home, name="home"),
    path('forgot', views.forgot, name="forgot")
]