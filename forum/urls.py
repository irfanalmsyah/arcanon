from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('<int:post_id>/', login_required(views.PostView.as_view()), name='post'),
    path('create/', login_required(views.CreatePostView.as_view()), name='create_post'),
    path('<int:post_id>/create_comment/', login_required(views.CreateCommentView.as_view()), name='create_comment'),
    path('<int:post_id>/like/', login_required(views.LikePostView.as_view()), name='like_post'),
    path('<int:post_id>/comment/<int:comment_id>/like/', login_required(views.LikeCommentView.as_view()), name='like_comment'),
    path('search/', views.SearchView.as_view(), name='search'),
]