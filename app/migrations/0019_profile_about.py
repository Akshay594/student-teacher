# Generated by Django 3.1.7 on 2021-03-07 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20210307_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='about',
            field=models.TextField(max_length=2000, null=True),
        ),
    ]
