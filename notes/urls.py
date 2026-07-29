from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name='index'),
    path("New",views.New_Task,name='newtask'),
    path("Archive",views.Archive,name='archive')
]