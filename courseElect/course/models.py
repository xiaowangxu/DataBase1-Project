from django.db import models
from teacher.models import Teacher
# Create your models here.


class Course(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True,
                          serialize=False, verbose_name='ID')
    name = models.CharField(max_length=50)
    cid = models.CharField(max_length=50, unique=True)
    # tid = models.CharField(max_length=50, unique=True)
    credit = models.IntegerField()
    term = models.CharField(max_length=50)
    depart = models.CharField(max_length=50)
    accept = models.BooleanField(
        verbose_name="Accepted", default="", null=True)
    description = models.CharField(max_length=1000, default="无介绍")
    keys_tid = models.ForeignKey(
        Teacher, verbose_name="fk_Course_id", on_delete=models.PROTECT)
