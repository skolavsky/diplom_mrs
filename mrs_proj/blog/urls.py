from django.urls import path

from .feeds import LatestPostsFeed
from .views import PostListView, PostDetailView, PostSearchView

app_name = 'blog'

# Post views
urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>/', PostListView.as_view(), name='post_list_by_tag'),
    path('post_detail/<str:identifier>/', PostDetailView.as_view(), name='post_detail'),
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('feed/', LatestPostsFeed(), name='post_feed'),

]
