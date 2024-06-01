# project/urls.py
from blog.sitemaps import PostSitemap, WebHandlerSitemap
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

sitemaps = {
    'posts': PostSitemap,
    'web_handler': WebHandlerSitemap,
}

# url's проекта
urlpatterns = [
    path('admin/', admin.site.urls),  # admin site
    path('logout/', LogoutView.as_view(next_page='web_handler:home'), name='logout'),
    path('clients/', include('clients.urls')),
    path('account/', include('account.urls')),
    path('blog/', include('blog.urls', namespace='blog')),
    path("unicorn/", include("django_unicorn.urls")),
    path('', include('web_handler.urls')),
    # django-health patch
    path('health/', include('health_check.urls')),
    # API's pathes
    path('api/', include('clients.AI.urls')),

    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', include('robots.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
                   path("ckeditor5/", include('django_ckeditor_5.urls')),
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
