# Generated by Django 3.1.7 on 2021-04-27 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_course_accept'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='accept',
            field=models.BooleanField(default='', verbose_name='Accepted'),
        ),
    ]
