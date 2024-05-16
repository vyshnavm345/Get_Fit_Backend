from django.urls import path
from .views import FitnessProgramCreateView, FitnessProgramListAPIView, Get_fitness_program, Get_trainer_programme, CreateLesson, GetLessonList, DeleteLesson,  GetProgramCount, GetPopularProgram

urlpatterns = [
    path("create/", FitnessProgramCreateView.as_view()),
    path("retrive_all/", FitnessProgramListAPIView.as_view()),
    path("get_programme/<int:pk>/", Get_fitness_program.as_view()),
    path("get_trainer_programme/<int:pk>/", Get_trainer_programme.as_view()),
    path("createLesson/<int:pk>/", CreateLesson.as_view()),
    path("getLessons/<int:pk>/", GetLessonList.as_view()),
    path("DeleteLesson/<int:pk>/", DeleteLesson.as_view()),
    path("getProgramCount/", GetProgramCount.as_view()),
    path("getPopularProgram/", GetPopularProgram.as_view()),
   
]




