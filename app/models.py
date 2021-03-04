from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)




class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    is_star = models.BooleanField(default=False, null=True)
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.user}'

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    students = models.ManyToManyField(Student, related_name='teachers')

    class Meta:
        ordering = ['-id']
        
    def __str__(self):
        return f'{self.user}'