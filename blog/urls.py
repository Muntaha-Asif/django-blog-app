from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView,
    PostUpdateView, PostDeleteView, CategoryPostsView, UserPostsView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/like/', views.like_post, name='like-post'),
    path('post/<int:pk>/comment/', views.add_comment, name='add-comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete-comment'),
    path('category/<slug:slug>/', CategoryPostsView.as_view(), name='category-posts'),
    path('user/<str:username>/', UserPostsView.as_view(), name='user-posts'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
]