from rest_framework import serializers
from .models import User
from django.contrib.auth.models import Group

"""
用户注册序列化器
"""


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        normal = Group.objects.filter(name="普通用户").first()
        if not normal:
            normal = Group.objects.create(name="普通用户")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        user.groups.add(normal)
        return user

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)
        instance.save()
        return instance


"""
 用户信息序列化器
"""


class UserReaderializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username", "coins", "times")
