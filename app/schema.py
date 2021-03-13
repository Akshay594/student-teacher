import graphene
from graphene_django import DjangoObjectType
from .models import User, Teacher, Student



class UserType(DjangoObjectType):
    class Meta:
        model = User
        
class StudentType(DjangoObjectType):
    class Meta:
        model = Student

class TeacherType(DjangoObjectType):
    class Meta:
        model = Teacher

# For quering the database
class Query(graphene.ObjectType):
    """
        This class helps in performing the operations for querying the
        database for teachers and students.
    """
    teachers = graphene.List(UserType)
    students = graphene.List(UserType)
    star_students = graphene.List(StudentType, username=graphene.String(required=True))

    def resolve_teachers(self, info):
        # Returns the list of all teachers we have.
        return User.objects.all().filter(is_teacher=True)
    
    def resolve_students(self, info):
        # Returns the list of all students we have
        return User.objects.all().filter(is_student=True)
    
    def resolve_star_students(self, info, username):
        # Returns the list of all star students marked by a teacher
        user = User.objects.get(username=username)
        teacher = Teacher.objects.get(user=user)
        return teacher.star_students.all()

class CreateUser(graphene.Mutation):
    # Creates teacher and student account
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        is_student = graphene.Boolean(required=True)
        is_teacher = graphene.Boolean(required=True)
    
    def mutate(self, info, **kwargs):
        user = User(
            username=kwargs.get('username'),
            is_student=kwargs.get('is_student'),
            is_teacher=kwargs.get('is_teacher')
        )
        user.set_password(kwargs.get('password'))
        user.save()
        return CreateUser(user=user)

class CreateStarStudent(graphene.Mutation):
    """
        This class helps in adding the star with a teacher account.
    """
    student = graphene.Field(StudentType)
    teacher = graphene.Field(TeacherType)

    class Arguments:
        teacher_username = graphene.String(required=True)
        student_username = graphene.String(required=True)
    
    def mutate(self, info, **kwargs):
        teacher_user = User.objects.get(username=kwargs.get('teacher_username'))
        student_user = User.objects.get(username=kwargs.get('student_username'))

        teacher = Teacher.objects.get(user=teacher_user)
        student = Student.objects.get(user=student_user)

        teacher.star_students.add(student)
        return CreateStarStudent(student=student, teacher=teacher)

    
class RemoveStarStudent(graphene.Mutation):
    """
        This class removes the star from a student account.
    """
    student = graphene.Field(StudentType)
    teacher = graphene.Field(TeacherType)

    class Arguments:
        teacher_username = graphene.String(required=True)
        student_username = graphene.String(required=True)
    
    def mutate(self, info, **kwargs):
        teacher_user = User.objects.get(username=kwargs.get('teacher_username'))
        student_user = User.objects.get(username=kwargs.get('student_username'))

        teacher = Teacher.objects.get(user=teacher_user)
        student = Student.objects.get(user=student_user)

        teacher.star_students.remove(student)
        return RemoveStarStudent(student=student, teacher=teacher)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_star_student = CreateStarStudent.Field()
    remove_star_student = RemoveStarStudent.Field()
