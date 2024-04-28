from django.urls import path

from .views import PostListView, PostDetailView, PostSearchView

app_name = 'blog'

# Post views
urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>/', PostListView.as_view(), name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', PostDetailView.as_view(), name='post_detail'),
    path('search/', PostSearchView.as_view(), name='post_search'),
]
