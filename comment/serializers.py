from rest_framework import serializers
from django.contrib.auth import get_user_model

from account.serializers import UserReaderializer
from article.serializers import ArticleReadSerializer
from .models import Article, Comment


class CommentReadSerializer(serializers.ModelSerializer):
    author = UserReaderializer()
    

    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'is_great', 'created', 'updated')
        read_only_fields = ('id', 'author', 'created', 'updated', 'is_great')


class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content', 'article')

    def create(self, validated_data):
        comment = Comment(
            author=self.context['request'].user,
            **validated_data
        )
        comment.save()
        return comment
    