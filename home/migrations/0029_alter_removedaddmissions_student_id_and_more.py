# Generated by Django 4.1 on 2022-10-05 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_alter_removedaddmissions_student_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='removedaddmissions',
            name='student_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='studentprogress',
            name='student_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='studentsattendance',
            name='student_id',
            field=models.IntegerField(),
        ),
    ]
