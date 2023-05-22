from django.shortcuts import render, redirect
from chat.models import Room
from forum.models import Post
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .forms import CustomUserCreationForm
from django.views import View
from django.db.models import Count
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator


class IndexView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, "main/landing.html")
        try:
            room = Room.objects.filter(
                Q(requester=request.user) | Q(responder=request.user)
            ).first()
        except Room.DoesNotExist:
            room = None
        try:
            allposts = Post.objects.all().order_by('-date_posted')
            paginator = Paginator(allposts, 10)
            page_number = request.GET.get('page')
            posts = paginator.get_page(page_number)
            posts_likes = [post.likes.count() for post in posts]
            posts_isLiked = [
                request.user in post.likes.all() for post in posts
            ]
            post_comments = [post.comments.count() for post in posts]
        except Post.DoesNotExist:
            posts = None
        context = {
            'room': room,
            'posts': zip(posts, posts_likes, posts_isLiked, post_comments),
            'page_obj': posts
        }
        return render(request, "main/index.html", context)


class TopPostsView(View):
    def get(self, request):
        try:
            room = Room.objects.filter(
                Q(requester=request.user) | Q(responder=request.user)
            ).first()
        except Room.DoesNotExist:
            room = None
        try:
            # get posts with most likes count and sort by new
            posts = Post.objects.all().annotate(like_count=Count('likes')).\
                order_by('-like_count', '-date_posted')
            posts_likes = [post.likes.count() for post in posts]
            posts_isLiked = [
                request.user in post.likes.all() for post in posts
            ]
            post_comments = [post.comments.count() for post in posts]
        except Post.DoesNotExist:
            posts = None
        context = {
            'room': room,
            'posts': zip(posts, posts_likes, posts_isLiked, post_comments)}
        return render(request, "main/index.html", context)


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, 'main/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            context = {'message': 'Invalid username or password.'}
            return render(request, 'main/login.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'main/register.html')

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            message = ''
            for error in form.errors.values():
                message += error[0] + ' '
            context = {'message': message}
            return render(request, 'main/register.html', context)


class SettingsView(View):
    def get(self, request):
        param = request.GET.get('success')
        context = None
        if param == 'chat':
            message = 'Chat preferences updated successfully.'
            context = {'message': message}
        elif param == 'profile':
            message = 'Profile updated successfully.'
            context = {'message': message}
        if context:
            return render(request, 'main/settings.html', context)
        return render(request, 'main/settings.html')

    def post(self, request):
        if request.POST['type'] == "account":
            request.user.email = request.POST['email']
            request.user.phone = request.POST['phone']
            request.user.save()
            if request.POST['old_password'] != '':
                form = PasswordChangeForm(request.user, request.POST)
                if form.is_valid():
                    form.save()
                    message = 'Password changed successfully.'
                    context = {'message': message}
                    login(request, request.user)
                    return render(request, 'main/settings.html', context)
                else:
                    message = ''
                    for error in form.errors.values():
                        message += error[0] + ' '
                    context = {'message': message}
                    return render(request, 'main/settings.html', context)
        elif request.POST['type'] == "profile":
            request.user.name = request.POST['name']
            request.user.country = request.POST['country']
            if request.POST['dob'] != '':
                request.user.dob = request.POST['dob']
            request.user.gender = request.POST['gender']
            request.user.instagram = request.POST['instagram']
            request.user.twitter = request.POST['twitter']
            try:
                request.user.picture = request.FILES['image']
            except:
                pass
            request.user.save()
            return redirect('/settings?success=profile#profile-tab-pane')
        elif request.POST['type'] == "chat":
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
                gender_pref = ""
            request.user.age_pref = age_pref
            request.user.gender_pref = gender_pref
            request.user.save()
            return redirect('/settings?success=chat#chat-tab-pane')
        return render(request, 'main/settings.html')


class ProfileView(View):
    def get(self, request):
        try:
            room = Room.objects.filter(
                Q(requester=request.user) | Q(responder=request.user)
            ).first()
        except Room.DoesNotExist:
            room = None
        try:
            allposts = Post.objects.filter(
                Q(author=request.user)
            ).annotate(like_count=Count('likes')).order_by('-date_posted')
            posts_count = allposts.count()
            posts_likes_count = sum([post.likes.count() for post in allposts])
            paginator = Paginator(allposts, 10)
            page_number = request.GET.get('page')
            posts = paginator.get_page(page_number)
            post_likes = [post.likes.count() for post in posts]
            post_isLiked = [request.user in post.likes.all() for post in posts]
            post_comments = [post.comments.count() for post in posts]
        except Post.DoesNotExist:
            posts = None
        context = {
            'room': room,
            'posts': zip(posts, post_likes, post_isLiked, post_comments),
            'posts_count': posts_count,
            'posts_likes_count': posts_likes_count,
            'page_obj': posts,
        }
        return render(request, "main/profile.html", context)


class ProfileLikeView(View):
    def get(self, request):
        try:
            room = Room.objects.filter(
                Q(requester=request.user) | Q(responder=request.user)
            ).first()
        except Room.DoesNotExist:
            room = None
        try:
            allposts = Post.objects.filter(
                Q(author=request.user)
            ).annotate(like_count=Count('likes')).order_by('-date_posted')
            posts_count = allposts.count()
            posts_likes_count = sum([post.likes.count() for post in allposts])
            allposts = Post.objects.filter(likes=request.user).\
                annotate(like_count=Count('likes')).order_by('-date_posted')
            paginator = Paginator(allposts, 10)
            page_number = request.GET.get('page')
            posts = paginator.get_page(page_number)
            post_likes = [post.likes.count() for post in posts]
            post_isLiked = [request.user in post.likes.all() for post in posts]
            post_comments = [post.comments.count() for post in posts]
        except Post.DoesNotExist:
            posts = None
        context = {
            'room': room,
            'posts': zip(posts, post_likes, post_isLiked, post_comments),
            'posts_count': posts_count,
            'posts_likes_count': posts_likes_count,
            'page_obj': posts,
        }
        return render(request, "main/profile.html", context)
