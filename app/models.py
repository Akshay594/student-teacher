from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=200)
    grade = models.CharField(max_length=10)
    roll_no = models.IntegerField(blank=False)

    class Meta:
        ordering = ['roll_no']

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    students = models.ManyToManyField(Student, related_name='students')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name