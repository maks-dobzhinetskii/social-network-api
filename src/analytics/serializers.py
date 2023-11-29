from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'last_login', 'last_request')
