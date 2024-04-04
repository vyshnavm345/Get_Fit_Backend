from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework_simplejwt import RefreshToken

from .serializers import UserCreateSerializer, UserSerializer, UserWithProfileSerializer, ProfileSerializer
from .models import Profile, UserAccount
import time

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        time.sleep(5)
        serializer = UserCreateSerializer(data = data)
        if not serializer.is_valid():
            error_messages = ""
            for field, messages in serializer.errors.items():
                for message in messages:
                    error_messages += f"{message}. \n"
            print("this is the register error", error_messages)
            return Response({"error_message": error_messages.strip()}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.create(serializer.validated_data)
        user = UserSerializer(user)
        
        return Response(user.data, status=status.HTTP_201_CREATED)
    
class RetriveUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        user = UserSerializer(user)

        return Response(user.data, status=status.HTTP_200_OK)

class Retrive_full_user_data(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        user = UserWithProfileSerializer(user)

        return Response(user.data, status=status.HTTP_200_OK)
    
    
@api_view(['PUT'])
def update_user_profile(request):

    data = request.data.copy()
    profile_data = {
        'height': data.get('height'),
        'weight': data.get('weight'),
        'body_fat': data.get('body_fat'),
        'age': data.get('age'),
        'phone': data.get('phone'),
    }
    user_data ={
        "first_name": data.get('first_name'),
        "last_name": data.get('last_name'),
        "email": data.get('email'),
        
    }
    print("this is the user data", user_data)
    print("this is the profile data", profile_data)
    profile_picture = request.data.get('profile_picture')
    if profile_picture != 'null':
        user_data['profile_picture'] = profile_picture

    user_id = request.data.get('id')
    user = UserAccount.objects.get(id=user_id)
    user_serializer = UserSerializer(user, data=user_data, partial=True)

    if user_serializer.is_valid():
        print("serializer is valid")
        user_instance = user_serializer.save()
        profile_instance, created = Profile.objects.get_or_create(user=user_instance)
        profile_serializer = ProfileSerializer(profile_instance, data=profile_data, partial=True)
        if profile_serializer.is_valid():
            print("valid profile serializer")
            profile_serializer.save()
            return Response({'message': 'User profile updated successfully'}, status=status.HTTP_200_OK)
    print("This is the reason ",user_serializer.errors)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)










# @api_view(['PUT'])
# def update_user_profile(request):
#     print("this is the initial request", request.data)
#     user_data = request.data.copy()
#     profile_data = {
#         'height': user_data.get('height'),
#         'weight': user_data.get('weight'),
#         'body_fat': user_data.get('body_fat'),
#         'age': user_data.get('age'),
#         'phone': user_data.get('phone'),
#     } 
#     user_data ={
#         "first_name": user_data.get('first_name'),
#         "last_name": user_data.get('last_name'),
#         "email": user_data.get('email'),
#         "profile_picture": user_data.get('profile_picture')
#     }
#     print("this is the user data", user_data)
#     print("this is the profile data", profile_data)

#     user = UserAccount.objects.get(email = user_data['email'])
#     print("current user : ", user)
#     user_serializer = UserSerializer(user, data=user_data, partial=True)
#     if user_serializer.is_valid():
#         print("validated")
#         user_instance = user_serializer.save()
#         print("successfully saved userinstance : ", user_instance)

#         profile_instance, created = Profile.objects.get_or_create(user=user_instance)
#         print("success", profile_instance)
#         profile_serializer = ProfileSerializer(profile_instance, data=profile_data, partial=True)
#         if profile_serializer.is_valid():
#             profile_serializer.save()
#             return Response({'message': 'User profile updated successfully'}, status=status.HTTP_200_OK)
#     print("This is the reason ",user_serializer.errors)
#     return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)