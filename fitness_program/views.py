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
        id =request.data.get('id')
        # lesson = Lesson.objects.get(id=id)
        if id:
            print("The form is for updation ", request.data)
            try:
                message = self.updateLesson(request, id)
                print("back in the get method")
                return Response(message, status=status.HTTP_200_OK)
            except:
                return Response({"message":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ProgrammeLessonSerializer(data=request.data)
            if serializer.is_valid():
                print("data is valid")
                serializer.save(program=program)
                print("serializer is saved")
                return Response({'message':"Lesson Added"}, status=status.HTTP_201_CREATED)
            print("serializer error is", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def updateLesson(self, request, id):
        print("updating the lesson")
        lesson = Lesson.objects.get(id=id)
        data = request.data.copy() 
        if isinstance(request.data.get('image'), str):
            print("image is a string")
            del data['image']
        serializer = ProgrammeLessonSerializer(instance=lesson, data=data, partial=True)
        print("the data has been updated")
        if serializer.is_valid():
            print("Serializer is valid : data ")
            serializer.save()
            message = {'message': "Lesson updated successfully"}
            return message
        #     return Response({'message': "Lesson updated successfully"}, status=status.HTTP_200_OK)
        # print("error: ",serializer.errors)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        
        
    
# get the list of lessons of particular program
class GetLessonList(APIView):
    def get(self, request, pk):
        try:
            lessons = Lesson.objects.filter(program_id=pk)
            serializer = ProgrammeLessonSerializer(lessons, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"message":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
        
