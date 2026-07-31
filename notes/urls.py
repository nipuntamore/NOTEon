from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("Archive/",views.Archive,name='archive'),
    path('Archive/done/<int:note_id>/', views.toggle_done, name='toggle_done'),
    path('Archive/undone/<int:note_id>/', views.toggle_undone, name='toggle_undone'),
    path("New/",views.New_Task,name='newtask'),
]