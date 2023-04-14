from django.shortcuts import render, redirect
from django.views import View
from .models import Post, Comment

class PostView(View):
    def get(self, request, post_id):
        # get post by id
        post = Post.objects.get(id=post_id)
        # get all comments for this post
        comments = Comment.objects.filter(post=post).order_by('-date_posted')
        context = {'post': post, 'comments': comments}
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
