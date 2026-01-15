from django.contrib import admin
from .models import Post, Profile, Category, Like, Comment


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'website')
    search_fields = ('user__username', 'bio')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'date_posted', 'views', 'total_likes', 'total_comments')
    list_filter = ('status', 'category', 'date_posted', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'title': ('title',)}
    date_hierarchy = 'date_posted'

    def total_likes(self, obj):
        return obj.total_likes()

    total_likes.short_description = 'Likes'

    def total_comments(self, obj):
        return obj.total_comments()

    total_comments.short_description = 'Comments'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'date_posted', 'parent')
    list_filter = ('date_posted',)
    search_fields = ('content', 'author__username')