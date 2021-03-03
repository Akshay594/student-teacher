from django.shortcuts import reverse
from django.urls import resolve
from django.test import TestCase
from . import views

class StudentHomeTests(TestCase):
    def test_student_home_view_status_code(self):
        url = reverse('app:student_home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_student_home_url_resolves_home_view(self):
        view = resolve('/student/')
        self.assertEquals(view.func, views.student_home)


class TeacherHomeTests(TestCase):
    def test_teacher_home_view_status_code(self):
        url = reverse('app:teacher_home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_teacher_home_url_resolves_home_view(self):
        view = resolve('/teacher/')
        self.assertEquals(view.func, views.teacher_home)