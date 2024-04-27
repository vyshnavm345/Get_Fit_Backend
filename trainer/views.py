from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import TrainerProfileSerializer, TrainerSerializer
from .models import Trainer_profile
from user.serializers import FollowedProgramSerializer


class TrainerProfileView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        print("request received", request.data)
        try:
            serializer = TrainerProfileSerializer(data=request.data)
            if serializer.is_valid():
                print("data is valid")
                profile = Trainer_profile.objects.create(**serializer.validated_data)
                print("the validated data is ", serializer.validated_data)
                print("trainer profile create")
                if profile:
                    print("trainer exists")
                    user = request.user
                    user.is_trainer = True
                    print("user is a trainer now")
                    user.save()
                    profile.user = user
                    profile.save()
                    print("trainer profile assigned to user")
                return Response({"message": "Trainer profile created"}, status=status.HTTP_201_CREATED)
            else:
                print("error : ", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("error", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class RetriveTrainerProfile(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        print("The user is user: ", user)
        if not user.is_trainer:
            return Response({'message':"user is not a trainer"}, status=status.HTTP_400_BAD_REQUEST)
        trainer = Trainer_profile.objects.get(user=user)
        serializer = TrainerSerializer(trainer)
        print("This is the serialized trainer data : ", serializer.data)
        
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)

class RetriveAllTrainers(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        trainers = Trainer_profile.objects.all()
        serializer = TrainerSerializer(trainers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# retrive all the subscribers and followed programs of a trainer
class GetSubscribers(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            user = request.user
            trainer = Trainer_profile.objects.get(user=user)
            subscribers = trainer.get_subscribed_users()
            print("subscribers are : ", subscribers)
            serializer = FollowedProgramSerializer(subscribers, many=True)
            print("The serializer is ",serializer)
            print("The validated data is ",serializer.data)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("error", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        