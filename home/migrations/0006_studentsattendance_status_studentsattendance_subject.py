# Generated by Django 4.1 on 2022-09-21 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_syllabus_studentsdetails_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentsattendance',
            name='status',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='studentsattendance',
            name='subject',
            field=models.CharField(default='', max_length=100),
        ),
    ]