from rest_framework import serializers 
from .models import User 


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user
        
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == 'password':
                instance.set_password(value)
            else:
                setattr(instance, key, value)
        instance.save()
        return instance   
    

class UserReaderializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'coins')