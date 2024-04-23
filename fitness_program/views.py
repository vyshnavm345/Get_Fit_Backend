from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FitnessProgram, Lesson
from .serializers import FitnessProgramSerializer, ProgrammeLessonSerializer
from trainer.models import Trainer_profile


# create new programme
class FitnessProgramCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        # print("The request is :", request.data)
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
        # print("programme list : ", serializer.data[0])
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# retrive individual programme
class Get_fitness_program(APIView):
    def get(self, request, pk):
        program = FitnessProgram.objects.get(id=pk)
        serializer = FitnessProgramSerializer(program)
        # print("serialized programme data : ", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# retrive programms of individual trainers
class Get_trainer_programme(APIView):
    def get(self, request, pk):
        try:
            trainer = Trainer_profile.objects.get(id=pk)
            # print("The trainer is : ", trainer)
            programs = FitnessProgram.objects.filter(trainer=trainer)
            # print("The programmes are : ", programs)
            serializer = FitnessProgramSerializer(programs ,many=True)
            # print("serialized programme data : ", serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"message": "sorry cannot retrive the trainer programmes"}, status=status.HTTP_400_BAD_REQUEST)
    
# create new lesson for a programme
class CreateLesson(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        program = FitnessProgram.objects.get(id=pk)
        print("this is the programme")
        serializer = ProgrammeLessonSerializer(data=request.data)
        print("the serializer is ", serializer)
        if serializer.is_valid():
            print("data is valid")
            serializer.save(program=program)
            print("serializer is saved")
            print()
            return Response({'message':"Lesson Added"}, status=status.HTTP_201_CREATED)
        print("serializer error is", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class GetLessonList(APIView):
    def get(self, request, pk):
        try:
            lessons = Lesson.objects.filter(program_id=pk)
            print("THese are the lessons", lessons)
            serializer = ProgrammeLessonSerializer(lessons, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"message":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST)