from django.shortcuts import render
from .forms import create_todo
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import notes

# Create your views here.
def index(request):
    current_time = timezone.now()
    notes_list = notes.objects.all()
    context ={
        'notes': notes_list,
        'time':current_time        
    }
    return render(request,"notes/index.html",context)


def New_Task(request):
    if request.method == 'POST':
        form = create_todo(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = create_todo()
    return render(request, "notes/newtodo.html",{'form':form})

def Archive(request):
    notes_list = notes.objects.all()
    context ={
        'notes': notes_list       
    }
    return render(request,"notes/archive.html",context)