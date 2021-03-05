from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from PIL import Image

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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def get_absolute_url(self):
        return f'/profile/{self.user.username}/{self.user.id}/'


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


    def __str__(self):
        return f'Profile for user {self.user.username}'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()