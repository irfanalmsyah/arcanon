# chat/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.db.models import Q
from django.http import Http404
from django.utils.datastructures import MultiValueDictKeyError
from .models import Room, Message
from .random_string import generate_random_string


@login_required
def index(request):
    try:
        room = Room.objects.filter(Q(requester=request.user) | Q(responder=request.user)).first()
    except Room.DoesNotExist:
        room = None
    return render(request, "index.html", {"room": room})

@login_required
def room(request, room_name):
    try:
        room = Room.objects.get(name=room_name)
    except Room.DoesNotExist:
        raise Http404("Room does not exist")
    if not room.responder or request.user not in [room.requester, room.responder]:
        raise Http404("You are not allowed to view this room")
    return render(request, "room.html", {"room_name": room_name}) 

def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            context = {'message': 'Invalid username or password.'}
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                # Create and save a new user
                user = form.save()
                # Authenticate and log in the user
                login(request, user)
                return redirect('index')
            else:
                # Extract any error messages from the form and pass them to the template
                message = ''
                for error in form.errors.values():
                    message += error[0] + ' '
                context = {'message': message}
                return render(request, 'register.html', context)
        else:
            return render(request, 'register.html')


@login_required
def requester(request):
    if request.method == 'POST':
        room_name = generate_random_string()
        try:
            room = Room.objects.get(requester=request.user)
        except Room.DoesNotExist:
            room = Room(name=room_name, requester=request.user)
            room.save()
        return redirect(reverse('room', kwargs={'room_name': room.name}))


@login_required
def responder(request):
    if request.method == 'POST':
        room = Room.objects.first()
        room.responder = request.user
        room.save()
        return redirect(reverse('room', kwargs={'room_name': room.name}))
