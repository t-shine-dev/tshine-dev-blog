"""
Management command: python manage.py seed_posts
Creates real dev blog posts for TShine Dev Blog ⭐
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag
from django.utils.text import slugify
import random


POSTS = [
    {
        "title": "Getting Started with Django 5: Build Your First Web App",
        "category": "Django",
        "tags": ["django", "python", "web-dev", "beginner"],
        "excerpt": "A step-by-step guide to setting up Django 5, understanding the MTV architecture, and shipping your first working web application in under an hour.",
        "content": """Django is a high-level Python web framework that lets you build secure, scalable web applications fast. In this guide, we'll go from zero to a running app.

## What is Django?

Django follows the MTV (Model-Template-View) pattern. The framework handles the boring stuff — user auth, admin panels, database migrations — so you can focus on what makes your app unique.

## Setting Up

First, create a virtual environment and install Django:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install django
```

Then create your project:

```bash
django-admin startproject mysite
cd mysite
python manage.py startapp blog
```

## Your First Model

Open `blog/models.py` and define a Post model:

```python
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
```

Run migrations to create the database table:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Creating a View

In `blog/views.py`:

```python
from django.shortcuts import render
from .models import Post

def post_list(request):
    posts = Post.objects.filter(published=True).order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})
```

## Next Steps

From here, add URL routing in `urls.py`, create your templates, and use Django's built-in admin to manage content. Django's documentation is excellent — when in doubt, check the docs!

The key insight with Django: it's not magic, it's convention. Once you understand the flow (URL → View → Template), everything clicks.
""",
    },
    {
        "title": "Python Decorators Explained: From Basics to Real-World Use",
        "category": "Python",
        "tags": ["python", "decorators", "advanced", "functions"],
        "excerpt": "Decorators are one of Python's most elegant features. Learn how they work under the hood, write your own, and see patterns used in production codebases.",
        "content": """Decorators often feel like magic the first time you see them. They're not. Once you understand what's really happening, you'll use them everywhere.

## What is a Decorator?

A decorator is simply a function that takes another function as input and returns a modified version of it. That's it.

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before the function runs")
        result = func(*args, **kwargs)
        print("After the function runs")
        return result
    return wrapper

@my_decorator
def say_hello(name):
    print(f"Hello, {name}!")

say_hello("TShine")
# Before the function runs
# Hello, TShine!
# After the function runs
```

The `@my_decorator` syntax is just shorthand for `say_hello = my_decorator(say_hello)`.

## Preserving Metadata with functools.wraps

Always use `functools.wraps` — it preserves the original function's name and docstring:

```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

## A Practical Example: Timing Functions

```python
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

@timer
def slow_query():
    time.sleep(0.5)
    return "done"

slow_query()  # slow_query took 0.5001s
```

## Decorators with Arguments

To pass arguments to a decorator, add another layer:

```python
def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def greet():
    print("Hello!")

greet()  # Prints Hello! three times
```

## Real-World Uses

Django uses decorators extensively: `@login_required`, `@permission_required`, `@cache_page`. Flask uses `@app.route`. Next time you see `@something` above a function, you'll know exactly what's happening.
""",
    },
    {
        "title": "REST API Design: 10 Principles Every Developer Should Follow",
        "category": "APIs",
        "tags": ["api", "rest", "backend", "best-practices"],
        "excerpt": "Good API design separates maintainable systems from chaotic ones. These 10 practical principles will make your APIs intuitive, consistent, and a pleasure to consume.",
        "content": """Building a REST API is easy. Building a *good* REST API is an art. Here are 10 principles that separate professional API design from amateur work.

## 1. Use Nouns for Resources, Not Verbs

Bad: `GET /getUsers`, `POST /createUser`
Good: `GET /users`, `POST /users`

The HTTP method already expresses the action. Your URL should name the resource.

## 2. Use Plural Resource Names Consistently

Stick to plurals: `/users`, `/posts`, `/comments` — not a mix of `/user` and `/posts`.

## 3. Use HTTP Methods Correctly

```
GET    /posts          → list all posts
POST   /posts          → create a post
GET    /posts/{id}     → get one post
PUT    /posts/{id}     → replace a post
PATCH  /posts/{id}     → update fields
DELETE /posts/{id}     → delete a post
```

## 4. Return Proper HTTP Status Codes

```
200 OK          → success
201 Created     → resource created
204 No Content  → deleted successfully
400 Bad Request → validation error
401 Unauthorized → not authenticated
403 Forbidden   → not authorized
404 Not Found   → resource missing
422 Unprocessable → business logic error
500 Server Error → you broke something
```

## 5. Version Your API from Day One

Always prefix: `/api/v1/users` — never `/api/users`. Breaking changes become manageable.

## 6. Use Consistent JSON Structure

Every response should follow the same shape:

```json
{
  "data": { ... },
  "meta": { "page": 1, "total": 42 },
  "errors": null
}
```

## 7. Validate Input and Return Clear Errors

```json
{
  "errors": [
    { "field": "email", "message": "Invalid email format" }
  ]
}
```

## 8. Support Filtering, Sorting and Pagination

```
GET /posts?category=django&sort=-created_at&page=2&limit=20
```

## 9. Use HTTPS Always

No exceptions. Even in development, get used to secure connections.

## 10. Document Everything

No documentation = the API doesn't exist for your consumers. Use OpenAPI/Swagger. Write examples. Show error cases.

A well-designed API is a product. Treat it like one.
""",
    },
    {
        "title": "Git Workflows That Actually Work for Solo Developers and Teams",
        "category": "Git & DevOps",
        "tags": ["git", "workflow", "devops", "collaboration"],
        "excerpt": "Most developers know the basics of Git, but few use it strategically. Here are battle-tested workflows for keeping your history clean and your deployments safe.",
        "content": """Git is not just version control — it's the source of truth for your project's entire history. Used well, it saves you. Used carelessly, it becomes a liability.

## The Three Workflows

### 1. GitHub Flow (Simple, Great for Solo/Small Teams)

```
main
  └── feature/add-auth
  └── fix/login-bug
  └── feature/dark-mode
```

Rules:
- `main` is always deployable
- Branch off `main` for every feature
- Open a PR, review, merge
- Deploy immediately after merge

### 2. Git Flow (Structured, for Versioned Releases)

```
main
develop
  └── feature/...
  └── release/v1.2
  └── hotfix/critical-bug
```

Use this when you have scheduled releases or need to maintain multiple versions simultaneously.

### 3. Trunk-Based Development (Fast, for CI/CD teams)

Everyone commits directly to `main` (or very short-lived branches). Requires strong CI and feature flags.

## Commit Message Convention

Use Conventional Commits:

```
feat: add bookmark toggle endpoint
fix: resolve duplicate slug on post save
docs: update API documentation
refactor: extract read_time calculation to model
test: add coverage for comment approval
chore: upgrade Django to 5.2
```

This format enables automatic changelog generation and semantic versioning.

## Essential Git Commands You Should Know

```bash
# Undo last commit but keep changes staged
git reset --soft HEAD~1

# Stash work in progress
git stash push -m "WIP: auth refactor"
git stash pop

# Clean up merged branches
git branch --merged | grep -v main | xargs git branch -d

# See what changed in the last 5 commits
git log --oneline -5

# Interactive rebase to clean history before PR
git rebase -i HEAD~4
```

## The Golden Rule

Never rewrite history on shared branches. `git rebase`, `git push --force` and `git reset` on `main` or `develop` are career-limiting moves when working with a team.

On your own branches: rebase freely, keep history clean, squash noise before merging.
""",
    },
    {
        "title": "CSS Grid vs Flexbox: When to Use Each (With Real Examples)",
        "category": "Frontend",
        "tags": ["css", "frontend", "flexbox", "grid", "layout"],
        "excerpt": "The \"Grid vs Flexbox\" debate has a simple answer: they solve different problems. Learn exactly when to reach for each one with practical, copy-paste examples.",
        "content": """I see developers use Flexbox for everything, or Grid for everything, when the right answer is usually: use both. They're complementary tools, not competitors.

## The Core Difference

**Flexbox** = one-dimensional layout (a row OR a column)
**Grid** = two-dimensional layout (rows AND columns simultaneously)

That single insight solves 90% of the confusion.

## When to Use Flexbox

Use Flexbox when you're arranging items along a single axis:

```css
/* Navigation bar */
.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

/* Button group */
.btn-group {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

/* Card footer with space-between */
.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
```

## When to Use Grid

Use Grid when you have a two-dimensional layout — rows AND columns matter:

```css
/* Page layout */
.page {
  display: grid;
  grid-template-columns: 260px 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

/* Responsive card grid */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

/* Dashboard stats */
.stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}
```

## Use Both Together

The real power comes from nesting:

```css
/* Grid for the overall layout */
.dashboard {
  display: grid;
  grid-template-columns: 240px 1fr;
}

/* Flexbox for the sidebar nav items */
.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

/* Flexbox for each nav item internals */
.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
}
```

## The Quick Decision Guide

| Scenario | Use |
|---|---|
| Nav bar | Flexbox |
| Page layout | Grid |
| Card internals | Flexbox |
| Card grid | Grid |
| Button groups | Flexbox |
| Dashboard | Grid (outer), Flexbox (inner) |

Stop picking sides. Use both.
""",
    },
    {
        "title": "Django ORM: Advanced Queries You Need to Know",
        "category": "Django",
        "tags": ["django", "orm", "database", "python", "performance"],
        "excerpt": "The Django ORM is incredibly powerful, but most developers only scratch the surface. These advanced query techniques will make your database interactions faster and cleaner.",
        "content": """The Django ORM lets you do things that would take 50 lines of SQL in just one readable Python expression. Here are the techniques that separate Django beginners from experts.

## select_related and prefetch_related

The #1 performance mistake in Django: N+1 queries.

```python
# BAD: 1 query for posts + 1 query per post for author = N+1 queries
posts = Post.objects.all()
for post in posts:
    print(post.author.username)  # hits DB every iteration

# GOOD: 2 queries total (JOIN)
posts = Post.objects.select_related('author', 'category').all()

# GOOD for M2M: 2 queries (prefetch)
posts = Post.objects.prefetch_related('tags', 'comments').all()
```

## annotate() — Add Computed Fields

```python
from django.db.models import Count, Avg, Sum

# Add comment count to each post (one query!)
posts = Post.objects.annotate(
    comment_count=Count('comments'),
    total_views=Sum('views'),
)

# Use in template: {{ post.comment_count }}
```

## F() Expressions — Reference Field Values

```python
from django.db.models import F

# Increment view counter without fetching the object
Post.objects.filter(pk=post_id).update(views=F('views') + 1)

# Find posts where comments > views
from django.db.models import F
popular = Post.objects.filter(comments__count__gt=F('views'))
```

## Q() Objects — Complex Filters

```python
from django.db.models import Q

# OR condition
results = Post.objects.filter(
    Q(title__icontains=query) | Q(content__icontains=query)
)

# NOT condition
published = Post.objects.filter(~Q(status='draft'))

# Combined AND/OR/NOT
complex_filter = Post.objects.filter(
    Q(category__name='Django') & (
        Q(title__icontains='orm') | Q(tags__name='database')
    )
)
```

## values() and values_list() — Lightweight Queries

```python
# Only fetch what you need
titles = Post.objects.values_list('title', flat=True)
# Returns: <QuerySet ['Post 1', 'Post 2', ...]>

# Dictionary output
post_data = Post.objects.values('id', 'title', 'author__username')
```

## Aggregation

```python
from django.db.models import Count, Max, Min, Avg

stats = Post.objects.aggregate(
    total=Count('id'),
    max_views=Max('views'),
    avg_comments=Avg('comments__count'),
)
```

## exists() vs count() vs first()

```python
# Cheap existence check (don't use count() for this)
if Post.objects.filter(author=user).exists():
    print("User has posts")

# Get one or None without exception
post = Post.objects.filter(slug=slug).first()
```

The Django ORM is a joy to use when you know these patterns. Always check the generated SQL with `queryset.query` during development.
""",
    },
    {
        "title": "JavaScript Async/Await: Mastering Asynchronous Code",
        "category": "JavaScript",
        "tags": ["javascript", "async", "promises", "frontend"],
        "excerpt": "Callbacks are history. Promises are the past. Async/await is how modern JavaScript should be written. Master it completely with this practical guide.",
        "content": """Asynchronous JavaScript went through three eras: callbacks, Promises, and async/await. You should write async/await. Here's everything you need.

## The Problem: Asynchronous Operations

JavaScript is single-threaded. Fetching data, reading files, and timers can't block execution. We need a way to say "do this later, when it's ready."

## From Callbacks to Promises to Async/Await

```javascript
// Callbacks (the old way — callback hell)
getUser(id, function(user) {
  getPosts(user.id, function(posts) {
    getComments(posts[0].id, function(comments) {
      // deeply nested nightmare
    });
  });
});

// Promises (better, but chaining can still get messy)
getUser(id)
  .then(user => getPosts(user.id))
  .then(posts => getComments(posts[0].id))
  .then(comments => console.log(comments))
  .catch(err => console.error(err));

// Async/Await (clean, readable, maintainable)
async function loadData(id) {
  try {
    const user     = await getUser(id);
    const posts    = await getPosts(user.id);
    const comments = await getComments(posts[0].id);
    return comments;
  } catch (err) {
    console.error('Failed to load:', err);
  }
}
```

## Parallel Execution with Promise.all

Don't await things sequentially if they're independent:

```javascript
// SLOW: sequential (waits for each before starting next)
const user     = await getUser(id);
const settings = await getSettings(id);
const stats    = await getStats(id);

// FAST: parallel (all start at the same time)
const [user, settings, stats] = await Promise.all([
  getUser(id),
  getSettings(id),
  getStats(id),
]);
```

## Error Handling

```javascript
// Option 1: try/catch
async function fetchPost(slug) {
  try {
    const res = await fetch(`/api/posts/${slug}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error('Fetch failed:', err.message);
    return null;
  }
}

// Option 2: helper that never throws
async function safe(promise) {
  try {
    return [await promise, null];
  } catch (err) {
    return [null, err];
  }
}

const [data, error] = await safe(fetchPost('hello-world'));
if (error) { /* handle */ }
```

## Async in Loops

```javascript
const slugs = ['post-1', 'post-2', 'post-3'];

// WRONG: forEach doesn't handle async correctly
slugs.forEach(async (slug) => {
  await fetchPost(slug); // doesn't wait!
});

// CORRECT: sequential
for (const slug of slugs) {
  await fetchPost(slug);
}

// CORRECT: parallel
const posts = await Promise.all(slugs.map(fetchPost));
```

Async/await doesn't replace Promises — it's built on top of them. Understanding Promises makes you a better async/await user.
""",
    },
    {
        "title": "Building a Production-Ready Django REST API with DRF",
        "category": "APIs",
        "tags": ["django", "drf", "api", "rest", "python"],
        "excerpt": "Django REST Framework is the gold standard for building APIs in Python. This guide covers serializers, viewsets, authentication, permissions, and deployment.",
        "content": """Django REST Framework (DRF) turns Django into a powerhouse for building APIs. Here's how to build one that's actually production-ready.

## Setup

```bash
pip install djangorestframework
```

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

## Serializers

Serializers convert models to/from JSON:

```python
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    read_time   = serializers.IntegerField(read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'excerpt', 'author_name',
                  'read_time', 'comment_count', 'created_at']
        read_only_fields = ['slug', 'created_at']

    def get_comment_count(self, obj):
        return obj.comments.filter(is_approved=True).count()
```

## ViewSets — The DRF Superpower

```python
from rest_framework import viewsets, permissions, filters
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    filter_backends  = [filters.SearchFilter, filters.OrderingFilter]
    search_fields    = ['title', 'content', 'tags__name']
    ordering_fields  = ['created_at', 'views']
    ordering         = ['-created_at']

    def get_queryset(self):
        return Post.objects.filter(
            status='published'
        ).select_related('author', 'category').prefetch_related('tags')

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

## Router Registration

```python
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')

urlpatterns = [path('api/v1/', include(router.urls))]
```

This gives you: `GET /api/v1/posts/`, `POST /api/v1/posts/`, `GET /api/v1/posts/{id}/`, `PATCH`, `DELETE` — all for free.

## Custom Actions

```python
from rest_framework.decorators import action
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    ...
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def bookmark(self, request, pk=None):
        post = self.get_object()
        # toggle bookmark logic
        return Response({'bookmarked': True})
```

DRF is opinionated, but that's a feature. Follow the patterns and you'll have a consistent, well-documented API in no time.
""",
    },
]

CAT_COLORS = ['purple', 'amber', 'green', 'blue', 'red', 'pink', 'cyan', 'indigo']
CAT_ICONS = {
    'Django':        'bi-gear-wide-connected',
    'Python':        'bi-cpu',
    'APIs':          'bi-cloud-arrow-up',
    'Git & DevOps':  'bi-git',
    'Frontend':      'bi-palette',
    'JavaScript':    'bi-braces',
}


class Command(BaseCommand):
    help = 'Seed TShine Dev Blog with real developer posts'

    def handle(self, *args, **options):
        # Get or create a superuser to be the author
        user, created = User.objects.get_or_create(
            username='tshine',
            defaults={
                'email': 'tshine@example.com',
                'first_name': 'TShine',
                'last_name': 'Dev',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            user.set_password('tshine123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created author: tshine (password: tshine123)'))
        else:
            self.stdout.write(f'Using existing user: {user.username}')

        created_count = 0
        for i, post_data in enumerate(POSTS):
            # Get or create category
            cat, _ = Category.objects.get_or_create(
                name=post_data['category'],
                defaults={'slug': slugify(post_data['category'])}
            )

            # Skip if post already exists
            if Post.objects.filter(title=post_data['title']).exists():
                self.stdout.write(f'  Skipping (exists): {post_data["title"][:50]}')
                continue

            slug = slugify(post_data['title'])
            # Ensure unique slug
            base_slug = slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1

            post = Post.objects.create(
                title=post_data['title'],
                slug=slug,
                content=post_data['content'],
                excerpt=post_data['excerpt'],
                author=user,
                category=cat,
                status='published',
                views=random.randint(50, 800),
            )

            # Tags
            for tag_name in post_data['tags']:
                tag, _ = Tag.objects.get_or_create(
                    name=tag_name,
                    defaults={'slug': slugify(tag_name)}
                )
                post.tags.add(tag)

            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'  Created: {post.title[:60]}'))

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Done! Created {created_count} posts. '
            f'Visit http://localhost:8099/ to see them.'
        ))
