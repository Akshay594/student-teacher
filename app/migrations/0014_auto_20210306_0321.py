# Generated by Django 3.1.7 on 2021-03-06 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20210305_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='like',
            field=models.ManyToManyField(related_name='liked_teachers', to='app.Student'),
        ),
    ]
