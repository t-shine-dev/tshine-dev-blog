from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from blog import views as blog_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', blog_views.home, name='home'),
    path('register/', blog_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', blog_views.dashboard, name='dashboard'),
    path('search/', blog_views.search, name='search'),
    path('about/', blog_views.about, name='about'),
    path('blog/', include('blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
