from rest_framework import serializers
from django.contrib.auth import get_user_model
from taggit.models import Tag
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

from account.serializers import UserReaderializer

from .models import Article
from denounce.models import Denounce
from comment.models import Comment

class ArticleReadSerializer(serializers.ModelSerializer):
    author = UserReaderializer()
    tag_list = TagListSerializerField(source='tags', required=False)
    denounce = serializers.SerializerMethodField()
    comment_counts = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'author', 'title', 'content', 'created', 'updated', 'expired', 'tag_list', 'views', 'denounce', 'comment_counts')
        read_only_fields = ('id', 'author', 'created', 'updated', 'views', 'denounce', 'comment_counts')

    def get_denounce(self, obj):
        return Denounce.objects.filter(article=obj, denounce_status=1).exists()
    
    def get_comment_counts(self, obj):
        return Comment.objects.filter(article=obj).count()


class ArticleWriteSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()
    class Meta:
        model = Article
        fields = ('title', 'content', 'expired', 'tags')


    def create(self, validated_data):
        tags = validated_data.pop('tags')
        user=self.context['request'].user
        if not user.times and user.coins < 2:
            raise serializers.ValidationError("没有金币发表提问")
        article = Article(
            author=user,
            **validated_data
        )
        article.save()
        if user.times:
            user.times = user.times - 1
        else:
            user.coins = user.coins - 2
        user.save()
        article.tags.add(*tags)
        return article
    
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        
        instance.tags.clear()
        instance.tags.add(*tags)
        
        return instance
    

class TagSerializer(serializers.Serializer):
    tags = serializers.ListField(
        child=serializers.CharField()
    )