from django.db import models

# Create your models here.


class Student(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True,
                          serialize=False, verbose_name='ID')
    name = models.CharField(max_length=50)
    sid = models.CharField(max_length=50, unique=True)
    sex = models.CharField(max_length=2)
    birth = models.DateField()
    password = models.CharField(max_length=50, default='1234567890')
    depart = models.CharField(max_length=50)
