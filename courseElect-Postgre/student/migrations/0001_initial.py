# Generated by Django 3.1.7 on 2021-05-20 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('sid', models.CharField(max_length=50, unique=True)),
                ('sex', models.CharField(max_length=2)),
                ('birth', models.DateField()),
                ('password', models.CharField(default='1234567890', max_length=50)),
                ('depart', models.CharField(max_length=50)),
            ],
        ),
    ]