from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import Post, Category, Tag, Comment, Bookmark
from .forms import RegisterForm, PostForm, CommentForm, GuestCommentForm, UserCommentForm

CATEGORY_COLORS = [
    'cat-blue', 'cat-green', 'cat-purple',
    'cat-amber', 'cat-red', 'cat-cyan', 'cat-pink'
]


def home(request):
    posts = Post.objects.filter(status=Post.STATUS_PUBLISHED).select_related('author', 'category')
    categories = list(Category.objects.all())
    categories_with_colors = [
        (cat, CATEGORY_COLORS[i % len(CATEGORY_COLORS)])
        for i, cat in enumerate(categories)
    ]
    featured = posts.first()
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    user_bookmarks = set()
    if request.user.is_authenticated:
        user_bookmarks = set(
            Bookmark.objects.filter(user=request.user).values_list('post_id', flat=True)
        )

    return render(request, 'blog/home.html', {
        'page_obj': page_obj,
        'categories_with_colors': categories_with_colors,
        'featured': featured,
        'user_bookmarks': user_bookmarks,
    })


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.STATUS_PUBLISHED)
    post.views += 1
    post.save(update_fields=['views'])

    comments = post.comments.filter(is_approved=True)

    comment_form = UserCommentForm()

    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, post=post).exists()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'You must be logged in to post a comment.')
            return redirect(f"/login/?next={request.path}")
        comment_form = UserCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post  = post
            comment.user  = request.user
            comment.name  = request.user.get_full_name() or request.user.username
            comment.email = request.user.email or f'{request.user.username}@tshinedev.blog'
            comment.save()
            messages.success(request, 'Your comment has been posted!')
            return redirect('post_detail', slug=post.slug)

    related_posts = Post.objects.filter(
        status=Post.STATUS_PUBLISHED,
        category=post.category
    ).exclude(pk=post.pk)[:3]

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'related_posts': related_posts,
        'is_bookmarked': is_bookmarked,
    })


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            form.save()
            messages.success(request, 'Post created successfully.')
            if post.status == Post.STATUS_PUBLISHED:
                return redirect('post_detail', slug=post.slug)
            return redirect('dashboard')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Create'})


@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            if post.status == Post.STATUS_PUBLISHED:
                return redirect('post_detail', slug=post.slug)
            return redirect('dashboard')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'post': post, 'action': 'Edit'})


@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('dashboard')
    return render(request, 'blog/post_delete.html', {'post': post})


@login_required
def dashboard(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    published = posts.filter(status=Post.STATUS_PUBLISHED)
    drafts = posts.filter(status=Post.STATUS_DRAFT)
    total_views = sum(p.views for p in published)
    total_comments = Comment.objects.filter(post__author=request.user, is_approved=True).count()
    bookmark_count = Bookmark.objects.filter(user=request.user).count()
    recent_comments = Comment.objects.filter(
        post__author=request.user, is_approved=True
    ).select_related('post').order_by('-created_at')[:5]
    return render(request, 'blog/dashboard.html', {
        'posts': posts[:10],
        'published_count': published.count(),
        'draft_count': drafts.count(),
        'total_views': total_views,
        'total_comments': total_comments,
        'bookmark_count': bookmark_count,
        'recent_comments': recent_comments,
    })


@login_required
def toggle_bookmark(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.STATUS_PUBLISHED)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)
    if not created:
        bookmark.delete()
        bookmarked = False
    else:
        bookmarked = True
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'bookmarked': bookmarked})
    return redirect('post_detail', slug=slug)


@login_required
def bookmarked_posts(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('post', 'post__author', 'post__category')
    posts = [b.post for b in bookmarks]
    return render(request, 'blog/bookmarks.html', {'posts': posts})


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(status=Post.STATUS_PUBLISHED, category=category)
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/category.html', {'category': category, 'page_obj': page_obj})


def tag_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(status=Post.STATUS_PUBLISHED, tags=tag)
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/tag.html', {'tag': tag, 'page_obj': page_obj})


def author_posts(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(status=Post.STATUS_PUBLISHED, author=author)
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/author_posts.html', {'author': author, 'page_obj': page_obj})


def search(request):
    query = request.GET.get('q', '').strip()
    posts = Post.objects.none()
    if query:
        posts = Post.objects.filter(
            status=Post.STATUS_PUBLISHED
        ).filter(
            Q(title__icontains=query) | Q(content__icontains=query) |
            Q(excerpt__icontains=query) | Q(tags__name__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/search.html', {'page_obj': page_obj, 'query': query})


def about(request):
    return render(request, 'blog/about.html')


def tags_page(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_page.html', {'tags': tags})
