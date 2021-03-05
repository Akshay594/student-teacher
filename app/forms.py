from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User,Student,Teacher, Profile


class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        student = Student.objects.create(user=user)
        student.save()
        return user

class TeacherSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        teacher = Teacher.objects.create(user=user)
        teacher.save()
        return user





class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']