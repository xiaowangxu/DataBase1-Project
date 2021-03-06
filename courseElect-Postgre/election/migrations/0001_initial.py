# Generated by Django 3.1.7 on 2021-05-20 02:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='course.course', verbose_name='fk_Election_cid')),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='student.student', verbose_name='fk_Election_sid')),
            ],
        ),
    ]
