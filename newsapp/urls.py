from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.loginuser, name='login'),
    path('adminarea', views.adminuser, name='adminarea'),
    path('recentsearch', views.recentsearch, name='recentsearch'),
    path("logout/", views.logoutuser, name="logout"),
]