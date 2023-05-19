from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('<int:post_id>/', login_required(views.PostView.as_view()), name='post'),
    path('create/', login_required(views.CreatePostView.as_view()), name='create_post'),
    path('<int:post_id>/edit/', login_required(views.EditPostView.as_view()), name='edit_post'),
    path('<int:post_id>/delete/', login_required(views.DeletePostView.as_view()), name='delete_post'),
    path('<int:post_id>/create_comment/', login_required(views.CreateCommentView.as_view()), name='create_comment'),
    path('<int:post_id>/like/', login_required(views.LikePostView.as_view()), name='like_post'),
    path('<int:post_id>/comment/<int:comment_id>/like/', login_required(views.LikeCommentView.as_view()), name='like_comment'),
    path('<int:post_id>/comment/<int:comment_id>/edit/', login_required(views.EditCommentView.as_view()), name='edit_comment'),
    path('<int:post_id>/comment/<int:comment_id>/delete/', login_required(views.DeleteCommentView.as_view()), name='delete_comment'),
    path('search/', views.SearchView.as_view(), name='search'),
]