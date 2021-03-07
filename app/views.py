from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Teacher, Student,User, Profile
from django.views.generic.list import ListView
from django.utils import timezone
from .forms import StudentSignUpForm, TeacherSignUpForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import CreateView, DetailView, DeleteView
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from  django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect


class StudentHomeListView(ListView):
    model = Teacher
    context_object_name = 'teachers'
    template_name = 'app/student_home.html'
              


class TeacherFilteredDetailView(ListView):
    model = Teacher
    template_name = 'app/data.html'

    def get_context_data(self,*args,  **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = Teacher.objects.get(user=self.request.user)
        students = teacher.students.all()
        if students is not None:
            context['students'] = students
            return context
        else:
            context['no_data'] = "No data available"
            return context
 

class StudentFilteredDetailView(ListView):
    model = Student
    template_name = 'app/data.html'

    def get_context_data(self,*args,  **kwargs):
        context = super().get_context_data(**kwargs)
        student = Student.objects.get(user=self.request.user)
        teachers = student.teachers.all()
        if teachers is not None:
            context['teachers'] = teachers
            return context
        else:
            context['no_data'] = "No data available"
            return context
 

    


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


class StudentProfileDetailView(DetailView):
    model = Profile
    template_name = 'app/student_profile_detail.html'
    


class TeacherProfileDetailView(DetailView):
    model = Profile
    template_name = 'app/teacher_profile_detail.html'

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)
        p_teacher = get_object_or_404(Profile, id=self.kwargs['pk'])
        student = Student.objects.get(user=self.request.user)
        is_liked = False
        if student.teachers.filter(id=p_teacher.user.teacher.id).exists():
            is_liked = True
        data['is_liked'] = is_liked
        return data



def delete_confirm(request):
    return render(request, 'app/confirm_delete.html')

def del_user(request, username):    
    u = User.objects.get(username = username)
    u.delete()
    return redirect('/') 


def add_teacher(request, pk):
    teacher = get_object_or_404(Teacher, id=request.POST.get('id'))
    student = Student.objects.get(user=request.user)
    if student.teachers.filter(id=teacher.id).exists():
        student.teachers.remove(teacher)
    else:
        student.teachers.add(teacher)
    return redirect(f'/profile/teacher/{pk}')


def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            if request.user.is_teacher:
                return redirect('app:teacher_home')
            else:
                return redirect('app:student_home')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'app/profile.html', context)