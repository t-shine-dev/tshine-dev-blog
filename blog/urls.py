from django.urls import path
from . import views

urlpatterns = [
    path('post/new/', views.create_post, name='create_post'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('post/<slug:slug>/delete/', views.delete_post, name='delete_post'),
    path('post/<slug:slug>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('category/<slug:slug>/', views.category_posts, name='category'),
    path('tag/<slug:slug>/', views.tag_posts, name='tag'),
    path('tags/', views.tags_page, name='tags_page'),
    path('author/<str:username>/', views.author_posts, name='author_posts'),
    path('bookmarks/', views.bookmarked_posts, name='bookmarks'),
]
