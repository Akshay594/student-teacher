from django.shortcuts import render
from .models import Teacher, Student



def student_home(request):
    teachers = Teacher.objects.all()
    return render(request, 'app/student_home.html', context={
        'teachers':teachers
    })



def teacher_home(request):
    students = Student.objects.all()
    return render(request, 'app/teacher_home.html', context={
        'students':students
    })

