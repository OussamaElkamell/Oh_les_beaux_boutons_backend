from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model, authenticate
from .models import UserProfile

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['total_games_played', 'best_nird_score', 'total_points_earned']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'school_name', 'school_type', 'profile']
        read_only_fields = ['id']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'school_name', 'school_type']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create profile
        UserProfile.objects.create(user=user)
        
        return user
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # tell DRF to use email instead of username

    def validate(self, attrs):
        # `authenticate` expects `username` by default, so we pass email as username
        credentials = {
            'username': attrs.get('email'),  # here username is actually email
            'password': attrs.get('password')
        }

        user = authenticate(**credentials)

        if not user:
            raise serializers.ValidationError(
                "Aucun compte actif n'a été trouvé avec les identifiants fournis"
            )

        return super().validate(attrs)