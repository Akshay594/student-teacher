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
from django.contrib.auth.decorators import login_required
from .decorators import student_required, teacher_required
from django.utils.decorators import method_decorator



def index(request):
    """
        This function handles the redirection of requests 
        according to the input requests by user.
    """
    if request.user.is_authenticated and request.user.is_teacher:
        return redirect('app:teahcer_home')
    elif request.user.is_authenticated and request.user.is_student:
        return redirect('app:student_home')
    else:
        return redirect('app:login')

class StudentHomeListView(ListView):
    """
        This class brings all teachers on student's homepage.
    """
    model = Teacher
    context_object_name = 'teachers'
    template_name = 'app/student_home.html'
              

@method_decorator([login_required(login_url='app:login'), teacher_required], name='dispatch')
class TeacherFilteredListView(ListView):
    """
        This class brings the selected students by teachers. 
    """
    model = Teacher
    template_name = 'app/data.html'

    def get_context_data(self,*args,  **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = Teacher.objects.get(user=self.request.user)
        # selecting all students with current teacher account.
        students = teacher.students.all()
        if students is not None:
            context['students'] = students
            return context
        else:
            context['no_data'] = "No data available"
            return context
 
@method_decorator([login_required(login_url='app:login'), student_required], name='dispatch')
class StudentFilteredListView(ListView):

    """
        This class brings the selected teachers by students.
    """
    model = Student
    template_name = 'app/data.html'

    def get_context_data(self,*args,  **kwargs):
        context = super().get_context_data(**kwargs)
        student = Student.objects.get(user=self.request.user)
        # selecting all teachers with the current student account.
        teachers = student.teachers.all()
        if teachers is not None:
            context['teachers'] = teachers
            return context
        else:
            context['no_data'] = "No data available"
            return context
 
class StarStudentListView(ListView):
    """
        Class for listing the exceptional students,starred by teachers.
    """
    model = Teacher
    template_name = 'app/star_students.html'

    def get_context_data(self,*args,  **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = Teacher.objects.get(user=self.request.user)
        students = teacher.star_students.all()
        if students is not None:
            context['students'] = students
            return context
        else:
            context['no_data'] = "No data available"
            return context


    


class TeacherHomeListView(ListView):
    """
        Class for listing the all students on teacher's home page.
    """
    model = Student
    paginate_by = 10
    context_object_name = 'students'
    template_name = 'app/teacher_home.html'




# Registration forms for student and teacher
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
    """
        Customized login view for students and
        teachers for logging in.
    """
    template_name = 'registration/login.html'
    def get_success_url(self):
        if self.request.user.is_teacher:
           return reverse('app:teacher_home')
        else:
            return reverse('app:student_home')

@method_decorator([login_required(login_url='app:login'), teacher_required], name='dispatch')
class StudentProfileDetailView(DetailView):
    """
        Profile view for students.
    """
    model = Profile
    template_name = 'app/student_profile_detail.html'

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)
        p_student = get_object_or_404(Profile, id=self.kwargs['pk'])
        teacher = Teacher.objects.get(user=self.request.user)
        is_liked = False
        if teacher.star_students.filter(id=p_student.user.student.id).exists():
            is_liked = True
        data['is_liked'] = is_liked
        return data
    

@method_decorator([login_required(login_url='app:login'), student_required], name='dispatch')
class TeacherProfileDetailView(DetailView):
    """
        Profile view for teachers.
    """
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



@login_required
def delete_confirm(request):
    return render(request, 'app/confirm_delete.html')

def del_user(request, username):   
    """
        Function for deleting the user.
    """ 
    u = User.objects.get(username = username)
    u.delete()
    return redirect('/') 

@login_required
def add_favourite(request, pk):
    """
        Function for adding the favourite teacher.
    """
    teacher = get_object_or_404(Teacher, id=request.POST.get('id'))
    student = Student.objects.get(user=request.user)
    if student.teachers.filter(id=teacher.id).exists():
        student.teachers.remove(teacher)
    else:
        student.teachers.add(teacher)
    return redirect(f'/profile/teacher/{pk}')

@login_required
def add_star(request, pk):
    """
        Function for marking a student exceptional.
    """
    student = get_object_or_404(Student, id=request.POST.get('id'))
    teacher = Teacher.objects.get(user=request.user)
    if teacher.star_students.filter(id=student.id).exists():
        teacher.star_students.remove(student)
    else:
        teacher.star_students.add(student)
    return redirect(f'/profile/student/{pk}')

 

    
@login_required
def profile(request):
    # Function for editing the user profile.
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