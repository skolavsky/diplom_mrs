from rest_framework import serializers
from taggit.serializers import (TagListSerializerField, TaggitSerializer)

from .models import Post


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = '__all__'
