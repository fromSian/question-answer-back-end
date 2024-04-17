from rest_framework import serializers
from django.contrib.auth import get_user_model
from taggit.models import Tag
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)

from account.serializers import UserReaderializer

from .models import Article


class ArticleReadSerializer(serializers.ModelSerializer):
    author = UserReaderializer()
    tag_list = TagListSerializerField(source='tags', required=False)

    class Meta:
        model = Article
        fields = ('id', 'author', 'title', 'content', 'created', 'updated', 'expired', 'tag_list', 'views')
        read_only_fields = ('id', 'author', 'created', 'updated', 'views')


class ArticleWriteSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()
    class Meta:
        model = Article
        fields = ('title', 'content', 'expired', 'tags')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        article = Article(
            author=self.context['request'].user,
            **validated_data
        )
        article.save()
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
    