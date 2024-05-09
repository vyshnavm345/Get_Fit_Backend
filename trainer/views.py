from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import TrainerProfileSerializer, TrainerSerializer
from .models import Trainer_profile
from user.serializers import FollowedProgramSerializer
from django.shortcuts import get_object_or_404
from user.models import FollowedPrograms
from rest_framework import filters
from fitness_program.models import FitnessProgram
from user.serializers import UserSerializer
from user.models import UserAccount

class TrainerProfileView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            serializer = TrainerProfileSerializer(data=request.data)
            if serializer.is_valid():
                profile = Trainer_profile.objects.create(**serializer.validated_data)
                if profile:
                    user = request.user
                    user.is_trainer = True
                    user.save()
                    profile.user = user
                    profile.save()
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
        if not user.is_trainer:
            return Response({'message':"user is not a trainer"}, status=status.HTTP_400_BAD_REQUEST)
        trainer = Trainer_profile.objects.get(user=user)
        serializer = TrainerSerializer(trainer)        
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
            # serializer = FollowedProgramSerializer(subscribers, many=True, context={'request': request, 'trainer_id': trainer.id})
            serializer = FollowedProgramSerializer(subscribers, many=True, context={'trainer_id': trainer.id})
            # print("The serializer is ",serializer)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("error", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RetrieveTrainer(APIView):
    def get(self, request, trainer_id):
        try:
            trainer = get_object_or_404(Trainer_profile, id=trainer_id)
            serializer = TrainerSerializer(trainer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Trainer_profile.DoesNotExist:
            return Response({'message': 'Trainer not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
# class GetUserTrainers(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self, request):
#         try:
#             user = request.user
#             trainers = Trainer_profile.objects.get(user=user)
#             print("The trainers are : ",trainers)
#             serializer = TrainerSerializer(trainers, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             print("error", str(e))
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# contact of all the users of a trainer
class GetTrainerContacts(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            user = request.user
            trainer = Trainer_profile.objects.get(user=user)
            programs = FitnessProgram.objects.filter(trainer=trainer)
            users = []
            for program in programs:
                user_ids = FollowedPrograms.objects.filter(program=program).values_list('user', flat=True)
                users.extend(UserAccount.objects.filter(pk__in=user_ids))
            users= set(users)
            users = list(users)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("error", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
        

# class GetUserContacts(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self, request):
#         try:
#             user = request.user
#             trainer = Trainer_profile.objects.get(user=user)
#             programs = FitnessProgram.objects.filter(trainer=trainer)
#             users = []
#             for program in programs:
#                 user_ids = FollowedPrograms.objects.filter(program=program).values_list('user', flat=True)
#                 users.extend(UserAccount.objects.filter(pk__in=user_ids))
#             print("subscribers are : ", users)
#             serializer = UserSerializer(users, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             print("error", str(e))
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)