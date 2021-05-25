from django.db import models

# Create your models here.


class Teacher(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True,
                          serialize=False, verbose_name='ID')
    name = models.CharField(max_length=50)
    tid = models.CharField(max_length=50, unique=True)
    isadmin = models.BooleanField(default=False, null=False)
    password = models.CharField(max_length=50, default='1234567890')
    depart = models.CharField(max_length=50)
