# Generated by Django 3.1.7 on 2021-05-25 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='capacity',
            field=models.IntegerField(default=50),
        ),
    ]
