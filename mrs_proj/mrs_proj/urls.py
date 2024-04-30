# project/urls.py
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap

sitemaps = {
    'posts': PostSitemap,
}

# url's проекта
urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', LogoutView.as_view(next_page='web_handler:home'), name='logout'),
    path('clients/', include('clients.urls')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('', include('web_handler.urls')),

    # API's pathes
    path('api/', include('clients.AI.urls')),

    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]
