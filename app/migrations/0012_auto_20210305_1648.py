# Generated by Django 3.1.7 on 2021-03-05 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20210305_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='like',
            field=models.ManyToManyField(related_name='liked_student', to='app.Teacher'),
        ),
    ]