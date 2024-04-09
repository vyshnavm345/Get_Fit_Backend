from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

from .models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password", "profile_picture")

    # validates the password using django inbuilt validators
    def validate(self, data):
        user = User(**data)
        password = data.get("password", user)
        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            # Convert the validation error into serializer errors
            serializer_errors = serializers.as_serializer_error(e)
            raise exceptions.ValidationError(
                {"password": serializer_errors["non_field_errors"]}
            )
        return data

    def create(self, validated_data):
        profile_picture = validated_data.pop("profile_picture", None)
        user = User.objects.create_user(**validated_data)

        if profile_picture:
            user.profile_picture = profile_picture
            user.save()
        print("user created in serializer")
        return user


class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False
    )

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "profile_picture",
            "is_staff",
        )


# class ProfileCreateSerializer(serializers.ModelSerializer):
#     profile_picture = serializers.ImageField(allow_null=True, required=False)
#     class Meta:
#         model = Profile
#         fields = ("height", "weight", "age", "body_fat","phone", "profile_picture")


#     def create(self, validated_data):
#         profile_picture = validated_data.pop('profile_picture', None)
#         user = User.objects.create_user(**validated_data)

#         if profile_picture:
#             user.profile_picture = profile_picture
#             user.save()

#         return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["height", "weight", "body_fat", "age", "phone"]


class UserWithProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "profile_picture",
            "profile",
        ]
