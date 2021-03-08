from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


app_name='app'
urlpatterns = [
    path('', views.index, name='index'),
    path('data/teachers/', views.TeacherFilteredListView.as_view(), name='data-detail-teacher'),


    path('data/students/', views.StudentFilteredListView.as_view(), name='data-detail-student'),
    
    path('like/<int:pk>', views.add_favourite, name='add_favourite'),
    path('star/<int:pk>', views.add_star, name='add_star'),

    path('student/', views.StudentHomeListView.as_view(), name='student_home'),
    path('teacher/', views.TeacherHomeListView.as_view(), name='teacher_home'),
    path('stars/', views.StarStudentListView.as_view(), name='star_students'),
    path('student/register/', views.StudentRegisterView.as_view(), name='student_signup'),
    path('teacher/register/', views.TeacherRegisterView.as_view(), name='teacher_signup'),

    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', views.CustomLoginView.as_view(), name='login'),

    path('profile/student/<pk>/', views.StudentProfileDetailView.as_view(), name='profile_detail_student'),
    path('profile/teacher/<pk>/', views.TeacherProfileDetailView.as_view(), name='profile_detail_teacher'),
    path('profile/', views.profile, name='profile'),
    path('delete/confirm/', views.delete_confirm, name='delete_confirm'),
    path('delete/<username>/', views.del_user, name='delete'),



]