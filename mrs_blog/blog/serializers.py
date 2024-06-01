from rest_framework import serializers
from taggit.serializers import (TagListSerializerField, TaggitSerializer)

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_comment_count(self, obj):
        return Comment.objects.filter(post=obj).count()
