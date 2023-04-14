from django.shortcuts import render
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
