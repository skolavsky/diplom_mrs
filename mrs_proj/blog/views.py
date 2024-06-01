import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django_ratelimit.decorators import ratelimit

from .forms import SearchForm
from .models import Post


class PostListView(LoginRequiredMixin, View):
    @method_decorator(ratelimit(key='ip', rate='30/m', method='GET', block=True))
    def get(self, request, tag_slug=None):
        posts_only = request.GET.get('posts_only')

        if tag_slug:
            url = f'http://127.0.0.1:8001/posts/by_tag/{tag_slug}/'
        else:
            url = 'http://127.0.0.1:8001/posts/'

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            return HttpResponse(f"Error fetching posts: {e}", status=500)

        data = response.json()
        post_list = data.get('results', [])
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

        context = {'posts': posts, 'tag': tag_slug, 'total_posts': data.get('count', 0)}
        if posts_only:
            return render(request, 'blog/posts.html', context)
        return render(request, 'blog/post/list.html', context)


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
    def get(self, request, identifier):
        url = f'http://127.0.0.1:8001/posts/{identifier}/'

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            return HttpResponse(f"Error fetching post: {e}", status=500)

        data = response.json()
        post = data.get('post')
        similar_posts = data.get('similar_posts', [])

        return render(request,
                      'blog/post/detail.html',
                      {'post': post,
                       'similar_posts': similar_posts})
