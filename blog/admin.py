from django.contrib import admin
from .models import Post, Category, Tag, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'views', 'published_at', 'created_at']
    list_filter = ['status', 'category', 'created_at', 'author']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = ['views', 'created_at', 'updated_at', 'published_at']
    date_hierarchy = 'created_at'
    list_editable = ['status']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'email', 'body']
    list_editable = ['is_approved']
    readonly_fields = ['created_at']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = 'Approve selected comments'
