from django.shortcuts import render
from .forms import create_todo
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request,"notes/index.html")

def New_Task(request):
    if request.method == 'POST':
        form = create_todo(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = create_todo()
    return render(request, "notes/newtodo.html",{'form':form})

    