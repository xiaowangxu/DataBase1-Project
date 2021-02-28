# Generated by Django 3.1.5 on 2021-02-02 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('tid', models.CharField(max_length=50, unique=True)),
                ('isadmin', models.BooleanField(default=False)),
                ('password', models.CharField(max_length=50)),
                ('depart', models.CharField(max_length=50)),
            ],
        ),
    ]
