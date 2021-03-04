from django.shortcuts import render, redirect
from .models import Teacher, Student,User
from django.views.generic.list import ListView
from django.utils import timezone
from .forms import StudentSignUpForm, TeacherSignUpForm
from django.views.generic import CreateView
from django.contrib.auth import login, logout,authenticate




class StudentHomeListView(ListView):
    model = Teacher
    paginate_by = 10
    context_object_name = 'teachers'
    template_name = 'app/student_home.html'


class TeacherHomeListView(ListView):
    model = Student
    paginate_by = 10
    context_object_name = 'students'
    template_name = 'app/teacher_home.html'


class StudentRegisterView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/student_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('app:student_home')

class TeacherRegisterView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/teacher_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('app:teacher_home')
