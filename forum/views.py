from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Post, Comment
from django.db.models import Count

class PostView(View):
    def get(self, request, post_id):
        # get post by id
        post = Post.objects.get(id=post_id)
        # get all comments for this post
        comments = Comment.objects.filter(post=post).annotate(like_count=Count('likes')).order_by('-like_count', 'date_posted')
        comment_likes = [comment.likes.count() for comment in comments]
        comment_isLiked = [request.user in comment.likes.all() for comment in comments]
        post_likes = post.likes.count()
        isLiked = post.likes.filter(id=request.user.id).exists()
        context = {'post': post, 'post_likes': post_likes, 'isLiked': isLiked, 'comments': zip(comments, comment_likes, comment_isLiked)}
        return render(request, 'post.html', context)
    

class CreatePostView(View):
    def get(self, request):
        return render(request, 'create_post.html')
    def post(self, request):
        # create a new post
        post = Post.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
            author=request.user
        )
        return redirect('post', post_id=post.id)


from django.http import JsonResponse

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
            'date_posted': comment.date_posted.strftime('%Y-%m-%d %H:%M:%S')
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
        return JsonResponse({'likes': post.likes.count(), 'liked': liked})

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
