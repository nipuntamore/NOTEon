from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from .forms import create_todo
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import User, notes
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
# Replace the old import line with this:
from .utils import generate_ai_cover_image


# Create your views here.


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "notes/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "notes/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "notes/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "notes/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "notes/register.html")
def index(request):
    notes_list = notes.objects.none()
    if request.user.is_authenticated:
        notes_list = notes.objects.filter(user_1=request.user, isarchived = False)

    current_time = timezone.now()
    context = {
        'notes': notes_list,
        'time': current_time,
    }
    return render(request, "notes/index.html", context)


def Archive(request):
    if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to create a task!")
            return redirect("login")
    notes_list = notes.objects.none()
    if request.user.is_authenticated:
        notes_list = notes.objects.filter(user_1=request.user, isarchived = True)      
    context ={
        'notes': notes_list       
    }
    return render(request,"notes/archive.html",context) 

def New_Task(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to create a task!")
        return redirect("login")
    
    if request.method == 'POST':
        form = create_todo(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user_1 = request.user
            task.cover_image_url = generate_ai_cover_image(
                note_title=task.title, 
                note_text=task.content
            )
            task.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = create_todo()
    return render(request, "notes/newtodo.html",{'form':form})

def toggle_done(request, note_id):
    note = notes.objects.none()
    if request.method == "POST" and request.user.is_authenticated:
        note = notes.objects.get(id=note_id, user_1=request.user)
        note.isarchived = True
        note.save()
    return HttpResponseRedirect(reverse("index"))
def toggle_undone(request, note_id):
    note = notes.objects.none()
    if request.method == "POST" and request.user.is_authenticated:
        note = notes.objects.get(id=note_id, user_1=request.user)
        note.isarchived = False
        note.save()
    return HttpResponseRedirect(reverse("index"))
def delete_note(request, note_id):
    if request.method == "POST" and request.user.is_authenticated:
        note = get_object_or_404(notes, id=note_id, user_1=request.user)
        note.delete()
    # Redirect back to whichever page sent the request (Dashboard or Archive)
    return redirect(request.META.get('HTTP_REFERER', 'index'))