# chat/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.db.models import Q
from django.http import Http404
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
    if request.user not in [room.requester, room.responder]:
        raise Http404("You are not allowed to view this room")
    return render(request, "room.html", {"room": room }) 

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
            form = CustomUserCreationForm(request.POST)
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
        room = None
        rooms = Room.objects.all()
        for r in rooms:
            requester_age = r.requester.age
            requester_gender = r.requester.gender
            requester_age_pref = r.requester.age_pref
            requester_gender_pref = r.requester.gender_pref
            responder_age = request.user.age
            responder_gender = request.user.gender
            responder_age_pref = request.user.age_pref
            responder_gender_pref = request.user.gender_pref
            if responder_gender_pref:
                if requester_gender != responder_gender_pref:
                    continue
            if requester_gender_pref:
                if responder_gender != requester_gender_pref:
                    continue
            if responder_age_pref:
                if responder_age_pref == 0:
                    if requester_age != responder_age:
                        continue
                elif responder_age_pref == 1:
                    if requester_age >= responder_age:
                        continue
                elif responder_age_pref == 2:
                    if requester_age <= responder_age:
                        continue
                elif responder_age_pref == 3:
                    if requester_age > responder_age:
                        continue
                elif responder_age_pref == 4:
                    if requester_age < responder_age:
                        continue
                elif responder_age_pref == 5:
                    if requester_age == responder_age:
                        continue
            if requester_age_pref:
                if requester_age_pref == 0:
                    if responder_age != requester_age:
                        continue
                elif requester_age_pref == 1:
                    if responder_age >= requester_age:
                        continue
                elif requester_age_pref == 2:
                    if responder_age <= requester_age:
                        continue
                elif requester_age_pref == 3:
                    if responder_age > requester_age:
                        continue
                elif requester_age_pref == 4:
                    if responder_age < requester_age:
                        continue
                elif requester_age_pref == 5:
                    if responder_age == requester_age:
                        continue
            room = r
            break
        if room:
            room.responder = request.user
            room.save()
            return redirect(reverse('room', kwargs={'room_name': room.name}))
        else:
            return redirect('index')
            

@login_required
def settings(request):
    if (request.method == 'POST'):
        age = request.POST['age']
        if age == '':
            age = None
        try:
            gender = request.POST['gender']
        except:
            gender = None
        
        try:
            age_pref_list = request.POST.getlist('agePref')
        except:
            age_pref_list = None
        
        if age_pref_list == ["same"]:
            age_pref = 0
        elif age_pref_list == ["younger"]:
            age_pref = 1
        elif age_pref_list == ["older"]:
            age_pref = 2
        elif age_pref_list == ["same", "younger"]:
            age_pref = 3
        elif age_pref_list == ["same", "older"]:
            age_pref = 4
        elif age_pref_list == ["older", "younger"]:
            age_pref = 5
        else:
            age_pref = None
        
        gender_pref = request.POST['genderPref']
        if gender_pref == 'A':
            gender_pref = None
        request.user.age = age
        request.user.gender = gender
        request.user.age_pref = age_pref
        request.user.gender_pref = gender_pref
        request.user.save()
        return render(request, 'settings.html')
    return render(request, 'settings.html')
