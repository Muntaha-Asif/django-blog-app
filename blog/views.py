from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q, Count
from django.http import JsonResponse
from .models import Post, Category, Like, Comment, Profile
from .forms import CommentForm, ProfileUpdateForm


class PostListView(ListView):
    """Display list of published posts"""
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.filter(status='published')
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__username__icontains=query)
            )

        if category:
            queryset = queryset.filter(category__slug=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['popular_posts'] = Post.objects.filter(status='published').order_by('-views')[:5]
        return context


class PostDetailView(DetailView):
    """Display single blog post"""
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        # Increment views
        post.views += 1
        post.save()

        # Check if user liked the post
        if self.request.user.is_authenticated:
            context['user_liked'] = Like.objects.filter(user=self.request.user, post=post).exists()
        else:
            context['user_liked'] = False

        # Get comments
        context['comments'] = post.comments.filter(parent=None)
        context['comment_form'] = CommentForm()

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create new blog post"""
    model = Post
    fields = ['title', 'content', 'image', 'category', 'status']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request,
                         f'Post {"published" if form.instance.status == "published" else "saved as draft"}!')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update existing blog post"""
    model = Post
    fields = ['title', 'content', 'image', 'category', 'status']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete blog post"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)


class CategoryPostsView(ListView):
    """Display posts by category"""
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return Post.objects.filter(category=self.category, status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class UserPostsView(ListView):
    """Display posts by specific user"""
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user, status='published').order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_author'] = get_object_or_404(User, username=self.kwargs.get('username'))
        return context


@login_required
def like_post(request, pk):
    """Like/Unlike a post"""
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'liked': liked,
        'total_likes': post.total_likes()
    })


@login_required
def add_comment(request, pk):
    """Add comment to post"""
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user

            # Check for parent comment (replies)
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)

            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Error adding comment.')

    return redirect('post-detail', pk=pk)


@login_required
def delete_comment(request, pk):
    """Delete a comment"""
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk

    if request.user == comment.author:
        comment.delete()
        messages.success(request, 'Comment deleted!')
    else:
        messages.error(request, 'You can only delete your own comments.')

    return redirect('post-detail', pk=post_pk)


@login_required
def profile(request):
    """User profile view"""
    # Get or create profile for user
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)

    context = {
        'form': form,
        'posts': Post.objects.filter(author=request.user),
        'total_posts': Post.objects.filter(author=request.user).count(),
        'total_likes': Like.objects.filter(post__author=request.user).count(),
        'total_comments': Comment.objects.filter(post__author=request.user).count(),
    }

    return render(request, 'blog/profile.html', context)

@login_required
def dashboard(request):
    """User dashboard"""
    posts = Post.objects.filter(author=request.user)

    context = {
        'total_posts': posts.count(),
        'published_posts': posts.filter(status='published').count(),
        'draft_posts': posts.filter(status='draft').count(),
        'total_views': sum(post.views for post in posts),
        'total_likes': Like.objects.filter(post__author=request.user).count(),
        'total_comments': Comment.objects.filter(post__author=request.user).count(),
        'recent_posts': posts[:5],
        'popular_posts': posts.order_by('-views')[:5],
    }

    return render(request, 'blog/dashboard.html', context)