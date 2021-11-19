from django.core.exceptions import ValidationError

from rest_framework import serializers

from authenication.models import User


class RegistrationSerializer(serializers.ModelSerializer):

    username = serializers.RegexField(r"^\+375([0-9]{1,9})$")
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def validate(self, attrs):
        try:
            if User.objects.get(username=attrs["username"]):
                raise ValidationError("User already exist", 401)

        except User.DoesNotExist:
            return attrs

    def create(self, validated_data):

        return User.objects.create_user(**validated_data)

      