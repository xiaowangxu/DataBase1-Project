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
    depart = models.CharField(max_length=50)
    keys_tid = models.ForeignKey(
        Teacher, verbose_name="fk_Course_id", on_delete=models.PROTECT)
