from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.loggin, name='login'),
    # path('', views.home, name='home'),
    path('signup', views.signup, name="signup"),
    path('home', views.home, name="home"),
    path('forgot', views.forgot, name="forgot"),
    path('open/<int:num>', views.open),
    path('nexxt', views.nexxt, name="nexxt"),
    path('prior', views.prior, name="prior"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('delit/<int:num>', views.delit, name="delit"),

    path('api', views.ApiOverview, name='homme'),
    path('api/create/', views.add_items, name='add-items'),
    path('api/all', views.view_items, name='view_items'),
    path('api/update/<int:pk>/', views.update_items, name='update-items'),
    path('api/blog/<int:pk>/delete/', views.delete_items, name='delete-items'),


]