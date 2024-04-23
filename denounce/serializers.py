from rest_framework import serializers
from django.contrib.auth import get_user_model

from account.serializers import UserReaderializer
from article.serializers import ArticleReadSerializer
from .models import Denounce


class DenounceReadWithArticleSerializer(serializers.ModelSerializer):
    user = UserReaderializer()
    article = ArticleReadSerializer()
    

    class Meta:
        model = Denounce
        fields = ('id', 'article', 'user', 'denounce_status', 'created', 'updated')


class DenounceWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Denounce
        fields = ('article', 'user')
    