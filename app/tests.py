from django.shortcuts import reverse
from django.urls import resolve
from django.test import TestCase
from . import views
from django.contrib.auth import get_user_model
from .models import Student, Teacher

class StudentHomeTests(TestCase):

    """
        For student's home page test
    """
    def test_student_home_view_status_code(self):
        url = reverse('app:student_home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_student_home_url_resolves_home_view(self):
        view = resolve('/student/')
        self.assertEquals(view.func.__name__, views.StudentHomeListView.as_view().__name__)


class TeacherHomeTests(TestCase):
    def test_teacher_home_view_status_code(self):
        url = reverse('app:teacher_home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_teacher_home_url_resolves_home_view(self):
        view = resolve('/teacher/')
        self.assertEquals(view.func.__name__, views.TeacherHomeListView.as_view().__name__)

    

class StudentSignUpTests(TestCase):
    def setUp(self):
        url = reverse('app:student_signup')
        self.response = self.client.get(url)

    def test_student_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_csrf_student(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_student_signup_url_resolves_signup_view(self):
        view = resolve('/student/register/')
        self.assertEquals(view.func.__name__, views.StudentRegisterView.as_view().__name__)
    

    
class TeacherSignUpTests(TestCase):

    def setUp(self):
        url = reverse('app:teacher_signup')
        self.response = self.client.get(url)

    def test_teacher_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_csrf_teacher(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')


    def test_teacher_signup_url_resolves_signup_view(self):
        view = resolve('/teacher/register/')
        self.assertEquals(view.func.__name__, views.TeacherRegisterView.as_view().__name__)


class StudentSuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('app:student_signup')
        data = {
            'username': 'gopal',
            'first_name':'Gopal',
            'last_name':'Singh',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('app:student_signup')


    def test_user_creation(self):
        self.assertTrue(Student.objects.exists())

    def test_user_authentication(self):
        '''
        Create a new request to an arbitrary page.
        The resulting response should now have a `user` to its context,
        after a successful sign up.
        '''
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

    
class TeacherSuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('app:student_signup')
        data = {
            'username': 'teacher',
            'first_name':'Akshay',
            'last_name':'Panwar',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('app:teacher_signup')


    def test_user_teacher_creation(self):
        self.assertTrue(Student.objects.exists())

    def test_user_teacher_authentication(self):
        '''
        Create a new request to an arbitrary page.
        The resulting response should now have a `user` to its context,
        after a successful sign up.
        '''
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)



class StudentInvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('app:student_signup')
        self.response = self.client.post(url, {})  # submit an empty dictionary

    def test_signup_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(Student.objects.exists())


class TeacherInvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('app:teacher_signup')
        self.response = self.client.post(url, {})  # submit an empty dictionary

    def test_signup_teacher_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_teacher_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_teacher_create_user(self):
        self.assertFalse(Teacher.objects.exists())