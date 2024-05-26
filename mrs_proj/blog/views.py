from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django_ratelimit.decorators import ratelimit
from taggit.models import Tag

from .forms import SearchForm
from .models import Post


class PostListView(LoginRequiredMixin, View):
    @method_decorator(ratelimit(key='ip', rate='30/m', method='GET', block=True))
    def get(self, request, tag_slug=None):
        post_list = Post.published.annotate(comment_count=Count('comments'))
        posts_only = request.GET.get('posts_only')

        tag = None
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            post_list = post_list.filter(tags__in=[tag])
        paginator = Paginator(post_list, 5)
        page_number = request.GET.get('page', 1)
        try:
            posts = paginator.page(page_number)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            if posts_only:
                return HttpResponse('')
            posts = paginator.page(paginator.num_pages)
        if posts_only:
            return render(request,
                          'blog/posts.html', {'posts': posts, 'tag': tag})
        return render(request,
                      'blog/post/list.html',
                      {'posts': posts, 'tag': tag})


class PostSearchView(LoginRequiredMixin, View):
    @method_decorator(ratelimit(key='ip', rate='30/m', method='GET', block=True))
    def get(self, request):
        form = SearchForm()
        query = None
        results = []

        if 'query' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']
                results = Post.published.annotate(
                    similarity=TrigramSimilarity('title', query),
                ).filter(similarity__gt=0.1).order_by('-similarity')

        return render(request,
                      'blog/post/search.html',
                      {'form': form,
                       'query': query,
                       'results': results})


class PostDetailView(LoginRequiredMixin, View):
    @method_decorator(ratelimit(key='ip', rate='30/m', method='GET', block=True))
    def get(self, request, year, month, day, post):
        post = get_object_or_404(Post,
                                 status=Post.Status.PUBLISHED,
                                 slug=post,
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day)

        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

        return render(request,
                      'blog/post/detail.html',
                      {'post': post,
                       'similar_posts': similar_posts})
