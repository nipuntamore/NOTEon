from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("Archive/",views.Archive,name='archive'),
    path("New/",views.New_Task,name='newtask'),
]