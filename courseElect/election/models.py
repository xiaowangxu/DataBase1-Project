from django.db import models
from student.models import Student
from course.models import Course

# Create your models here.


class Election(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True,
                          serialize=False, verbose_name='ID')
    sid = models.ForeignKey(
        Student, verbose_name='fk_Election_sid', on_delete=models.PROTECT)
    cid = models.ForeignKey(
        Course, verbose_name='fk_Election_cid', on_delete=models.PROTECT)
    grade = models.DecimalField(decimal_places=2, max_digits=5, null=True)
