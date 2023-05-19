from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Post, Comment
from chat.models import Room
from django.db.models import Count
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse

class PostView(View):
    def get(self, request, post_id):
        # get post by id
        post = Post.objects.get(id=post_id)
        # get all comments for this post
        comments = Comment.objects.filter(post=post).annotate(like_count=Count('likes')).order_by('-like_count', '-date_posted')
        comment_likes = [comment.likes.count() for comment in comments]
        comment_isLiked = [request.user in comment.likes.all() for comment in comments]
        comments_count = comments.count()
        post_likes = post.likes.count()
        isLiked = post.likes.filter(id=request.user.id).exists()
        context = {'post': post, 'post_likes': post_likes, 'isLiked': isLiked, 'comments': zip(comments, comment_likes, comment_isLiked), 'comments_count': comments_count}
        return render(request, 'forum/post.html', context)
    

class CreatePostView(View):
    def get(self, request):
        return render(request, 'forum/create.html')
    def post(self, request):
        # create a new post
        post = Post.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
            author=request.user
        )
        return redirect('post', post_id=post.id)
    

class EditPostView(View):
    def get(self, request, post_id):
        # get post by id
        post = Post.objects.get(id=post_id)
        context = {'post': post}
        return render(request, 'forum/edit.html', context)
    def post(self, request, post_id):
        # get post by id
        post = Post.objects.get(id=post_id)
        # update post
        post.content = request.POST['content']
        post.save()
        return redirect('post', post_id=post.id)


class DeletePostView(View):
    def get(self, request, post_id):
        # get post by id
        post = Post.objects.get(id=post_id)
        # delete post
        post.delete()
        return redirect('home')


class CreateCommentView(View):
    def post(self, request, post_id):
        # get post by id
        post = Post.objects.get(id=post_id)
        # create a new comment
        comment = Comment.objects.create(
            content=request.POST['content'],
            author=request.user,
            post=post
        )
        # return JSON response with the new comment's data
        return JsonResponse({
            'id': comment.id,
            'author': comment.author.username,
            'content': comment.content,
            'date_posted': comment.date_posted.strftime('%Y-%m-%d %H:%M:%S'),
            'post_id': post_id,
        })

class LikePostView(View):
    def post(self, request, post_id):
        # get post by id
        post = Post.objects.get(id=post_id)
        # check if user already liked the post
        if request.user in post.likes.all():
            # remove like
            post.likes.remove(request.user)
            liked = False
        else:
            # add like
            post.likes.add(request.user)
            liked = True
        # return JSON response with updated like count and whether user liked the post or not
        return JsonResponse({'likes': post.likes.count(), 'liked': liked, 'post_id': post_id})

class LikeCommentView(View):
    def post(self, request, post_id, comment_id):
        # get comment by id
        comment = Comment.objects.get(id=comment_id)
        # check if user already liked the comment
        if request.user in comment.likes.all():
            # remove like
            comment.likes.remove(request.user)
            liked = False
        else:
            # add like
            comment.likes.add(request.user)
            liked = True
        # return JSON response with updated like count and whether user liked the comment or not
        return JsonResponse({'likes': comment.likes.count(), 'liked': liked, 'comment_id': comment_id})
    

class SearchView(View):
    def get(self, request):
        query = request.GET['query']
        try:
            room = Room.objects.filter(Q(requester=request.user) | Q(responder=request.user)).first()
        except Room.DoesNotExist:
            room = None
        try:
            allposts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-date_posted')
            paginator = Paginator(allposts, 10)
            page_number = request.GET.get('page')
            posts = paginator.get_page(page_number)
            posts_likes = [post.likes.count() for post in posts]
            posts_isLiked = [request.user in post.likes.all() for post in posts]
            post_comments = [post.comments.count() for post in posts]
        except Post.DoesNotExist:
            posts = None
        context = {'room': room, 'posts': zip(posts, posts_likes, posts_isLiked, post_comments), 'page_obj': posts, 'query': query}
        return render(request, 'forum/search.html', context)
