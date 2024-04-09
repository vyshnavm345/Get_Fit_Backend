from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import TrainerProfileSerializer
from .models import Trainer_profile

class TrainerProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        print("request received")
        try:
            serializer = TrainerProfileSerializer(data=request.data)
            if serializer.is_valid():
                print("data is valid")
                profile = Trainer_profile.objects.create(**serializer.validated_data)
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
