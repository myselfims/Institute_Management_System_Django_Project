# Generated by Django 4.1 on 2022-10-04 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_alter_staffmember_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentsdetails',
            name='start_date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
