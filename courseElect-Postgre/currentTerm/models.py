from django.db import models

# Create your models here.


class CurrentTerm(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True,
                          serialize=False, verbose_name='ID')
    current = models.CharField(max_length=50)
