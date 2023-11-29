from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password

from .models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'phone',
                  'is_active', 'is_staff', 'is_superuser')


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Password fields do not match.'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            phone=validated_data.get('phone')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
