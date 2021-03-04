from django.shortcuts import render, redirect, reverse
from .models import Teacher, Student,User
from django.views.generic.list import ListView
from django.utils import timezone
from .forms import StudentSignUpForm, TeacherSignUpForm
from django.views.generic import CreateView
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from  django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model


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


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    def get_success_url(self):
        if self.request.user.is_teacher:
           return reverse('app:teacher_home')
        else:
            return reverse('app:student_home')