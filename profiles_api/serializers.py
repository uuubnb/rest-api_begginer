from rest_framework import serializers

from profiles_api import models


class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type':'password'}
            }
        }
    
    def create(self, validated_data):   # without this method passwords will be stored as a raw text
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user( # 'create_user' perfoms 'user.set_password' and 'user.save'
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
 
        return user
    
    """
    # SECOND OPTION FOR USER CREATION
    def create(self, validated_data):
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    """

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        
        return super().update(instance, validated_data)

