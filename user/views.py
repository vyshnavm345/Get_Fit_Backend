from rest_framework.views import APIView
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view 

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserCreateSerializer,
    UserSerializer,
    UserWithProfileSerializer,
    ProfileSerializer,
)
from .models import Profile, UserAccount
import time
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth import get_user_model
import jwt
from django.conf import settings
import json

User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserCreateSerializer(data=data)
        if not serializer.is_valid():
            error_messages = ""
            for field, messages in serializer.errors.items():
                for message in messages:
                    error_messages += f"{message}. \n"
            return Response(
                {"error_message": error_messages.strip()},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.create(serializer.validated_data)
        user_data = UserSerializer(user)

        user = UserAccount.objects.get(email=user.email)
        token = RefreshToken.for_user(user).access_token

        # current_site = get_current_site(request).domain
        # relative_link = reverse("email_verification")
        # absurl = "http://" + current_site + relative_link + "?token=" + str(token)
        absurl = "http://127.0.0.1:3000/verify/" + str(token)
        
        email_body = (
            "Hi "
            + user.first_name
            + "Use the link below to verify your email \n"
            + absurl
        )
        data = {
            "email_body": email_body,
            "to_email": user.email,
            "email_subject": "Veryfy your email",
        }
        print("the data is : ", data)
        frontend_domain = request.headers.get('Origin')
        print("This is the frontend domain : ", frontend_domain)
        
        
        Util.send_email(data)
        print("mail send")

        return Response(
            {"message": "Verification link sent to your email"},
            status=status.HTTP_201_CREATED
        )
        


class Verify_email(generics.GenericAPIView):
    def post(self, request):
        data = json.loads(request.body)
        token = data.get("token")
        print("This is the recieved Token:",token)
        print("This is the secret key : ",settings.SECRET_KEY)
        
        try:
            payload =jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = UserAccount.objects.get(id=payload['user_id'])
            # print("the user is :", user)
            if not user.is_verified:
                print("inside verified")
                user.is_verified = True
                user.save()
            else:
                return Response({"Message":"Account already active"}, status=status.HTTP_208_ALREADY_REPORTED)
            # user = UserSerializer(user)
            # return Response(user.data, status=status.HTTP_201_CREATED)
            print("sending message")
            return Response({"Message":"Account Activated \n Now Log in using your credentials"}, status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError as e:
            return Response({"error" : "Activation Link Expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            print("Error decoding token:", e)
            return Response({"error" : "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)


class RetriveUserView(APIView):
    print("retriving user data")
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_verified:
            user = UserSerializer(user)

            return Response(user.data, status=status.HTTP_200_OK)
        return Response({"message":"Email not Verified"}, status=status.HTTP_401_UNAUTHORIZED)

# add a decorater here to let only the once in the verified group to access
class Retrive_full_user_data(APIView):
    print("getting permission")
    permission_classes = [permissions.IsAuthenticated]
    print("got permission")
    def get(self, request):
        try:
            user = request.user
            if user.is_verified:
                user = UserWithProfileSerializer(user)

                return Response(user.data, status=status.HTTP_200_OK)
            print(Response.error)
            return Response({"message":"Email not Verified"}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            return Response({"message": "An error occurred while retrieving user data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT"])
def update_user_profile(request):
    data = request.data.copy()
    profile_data = {
        "height": data.get("height"),
        "weight": data.get("weight"),
        "body_fat": data.get("body_fat"),
        "age": data.get("age"),
        "phone": data.get("phone"),
    }
    user_data = {
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "email": data.get("email"),
    }
    print("this is the user data", user_data)
    print("this is the profile data", profile_data)
    profile_picture = request.data.get("profile_picture")
    if profile_picture != "null":
        user_data["profile_picture"] = profile_picture

    user_id = request.data.get("id")
    user = UserAccount.objects.get(id=user_id)
    user_serializer = UserSerializer(user, data=user_data, partial=True)

    if user_serializer.is_valid():
        print("serializer is valid")
        user_instance = user_serializer.save()
        profile_instance, created = Profile.objects.get_or_create(user=user_instance)
        
        cleaned_profile_data = {}
        for key, value in profile_data.items():
            if value != 'null':  # Skip null values
                cleaned_profile_data[key] = value
        print("this is the cleaned profile data", cleaned_profile_data)
        
        profile_serializer = ProfileSerializer(
            profile_instance, data=cleaned_profile_data, partial=True
        )
        if profile_serializer.is_valid():
            print("valid profile serializer")
            profile_serializer.save()
            return Response(
                {"message": "User profile updated successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            print("profile serializer error : ", profile_serializer.errors)
    print("This is the reason ", user_serializer.errors)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
