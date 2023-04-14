from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from chat.models import Room
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .forms import CustomUserCreationForm
from django.views import View

class IndexView(View):
    def get(self, request):
        try:
            room = Room.objects.filter(Q(requester=request.user) | Q(responder=request.user)).first()
        except Room.DoesNotExist:
            room = None
        return render(request, "index.html", {"room": room})

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("index")
        return render(request, 'login.html')
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            context = {'message': 'Invalid username or password.'}
            return render(request, 'login.html', context)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, 'register.html')
    def post(self, request):
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

class SettingsView(View):
    def get(self, request):
        return render(request, 'settings.html')
    
    def post(self, request):
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