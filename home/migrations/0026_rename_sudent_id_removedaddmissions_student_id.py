# Generated by Django 4.1 on 2022-10-04 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_removedaddmissions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='removedaddmissions',
            old_name='sudent_id',
            new_name='student_id',
        ),
    ]
