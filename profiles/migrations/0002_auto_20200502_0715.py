# Generated by Django 2.1.15 on 2020-05-02 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='user_type',
            field=models.CharField(choices=[('STUDENT', 'student'), ('TEACHER', 'teacher'), ('SECRETARY', 'secretary'), ('SUPERVISOR', 'supervisor'), ('ADMIN', 'admin')], default='student', max_length=64),
        ),
    ]
