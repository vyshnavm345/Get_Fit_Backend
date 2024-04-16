from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FitnessProgram
from .serializers import FitnessProgramSerializer, ProgrammeLessonSerializer
from trainer.models import Trainer_profile


# create new programme
class FitnessProgramCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        print("The request is :", request.data)
        serializer = FitnessProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"Programme created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# retrive all the available programms
class FitnessProgramListAPIView(APIView):
    def get(self, request):
        programs = FitnessProgram.objects.all()
        serializer = FitnessProgramSerializer(programs, many=True)
        print("programme list : ", serializer.data[0])
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# retrive individual programme
class Get_fitness_program(APIView):
    def get(self, request, pk):
        program = FitnessProgram.objects.get(id=pk)
        serializer = FitnessProgramSerializer(program)
        print("serialized programme data : ", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# retrive programms of individual trainers
class Get_trainer_programme(APIView):
    def get(self, request, pk):
        trainer = Trainer_profile.objects.get(id=pk)
        print("The trainer is : ", trainer)
        programs = FitnessProgram.objects.filter(trainer=trainer)
        print("The programmes are : ", programs)
        serializer = FitnessProgramSerializer(programs ,many=True)
        print("serialized programme data : ", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# create new lesson for a programme
class CreateLesson(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        program = FitnessProgram.objects.get(id=pk)
        serializer = ProgrammeLessonSerializer(data=request.data)
        if serializer.is_valid():
            print("data is valid")
            serializer.save(program=program)
            return Response({'message':"Lesson Added"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        