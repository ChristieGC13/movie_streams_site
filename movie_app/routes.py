from django.urls import path
from . import views

urlpatterns = [
    path('', views.root),
    path('register', views.register),
    path('register_account', views.register_account),
    path('login', views.login),
    path('home', views.home),
    path('search', views.search),
    path('results', views.results),
    path('title_details', views.title_details),
    path('logout', views.logout),
]