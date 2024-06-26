from rest_framework import serializers
from django.contrib.auth import get_user_model

from account.serializers import UserReaderializer
from article.serializers import ArticleReadSerializer
from .models import Article, Comment
from datetime import datetime

import pytz


"""
查询回答列表序列化器
"""


class CommentReadSerializer(serializers.ModelSerializer):
    author = UserReaderializer()

    class Meta:
        model = Comment
        fields = ("id", "author", "content", "is_great", "created", "updated")
        read_only_fields = ("id", "author", "created", "updated", "is_great")


"""
查询单条回答详细信息
"""


class CommentReadWithArticleSerializer(serializers.ModelSerializer):
    author = UserReaderializer()
    article = ArticleReadSerializer()

    class Meta:
        model = Comment
        fields = (
            "id",
            "article",
            "author",
            "content",
            "is_great",
            "created",
            "updated",
        )
        read_only_fields = ("id", "author", "created", "updated", "is_great")


class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content", "article")

    def create(self, validated_data):
        article = validated_data.get("article")
        if article.expired and article.expired < datetime.now():
            raise serializers.ValidationError("不在文章评论有效期内")
        comment = Comment(author=self.context["request"].user, **validated_data)
        comment.save()
        return comment
