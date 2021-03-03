from django.urls import path
from . import views



app_name='app'
urlpatterns = [
    path('student/', views.student_home, name='student_home'),
    path('teacher/', views.teacher_home, name='teacher_home'),

]