from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FitnessProgram
from .serializers import FitnessProgramSerializer
# Create your views here.


class FitnessProgramCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        print("The request is :", request.data)
        serializer = FitnessProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FitnessProgramListAPIView(APIView):
    def get(self, request):
        programs = FitnessProgram.objects.all()
        serializer = FitnessProgramSerializer(programs, many=True)
        return Response(serializer.data)