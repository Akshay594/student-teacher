from django.urls import path
from . import views



app_name='app'
urlpatterns = [
    path('student/', views.StudentHomeListView.as_view(), name='student_home'),
    path('teacher/', views.TeacherHomeListView.as_view(), name='teacher_home'),
    path('student/register/', views.StudentRegisterView.as_view(), name='student_signup'),
    path('teacher/register/', views.TeacherRegisterView.as_view(), name='teacher_signup'),



]