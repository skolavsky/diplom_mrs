from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from taggit.models import Tag

from .models import Post
from .serializers import PostSerializer


class PostPagination(PageNumberPagination):
    page_size = 5


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED).annotate(comment_count=Count('comments'))
    serializer_class = PostSerializer
    pagination_class = PostPagination

    @action(detail=False, methods=['get'])
    def by_tag(self, request, tag_slug=None):
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = self.queryset.filter(tags__in=[tag])
        else:
            queryset = self.queryset

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
