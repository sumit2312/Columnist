# Generated by Django 2.1.15 on 2020-05-05 17:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20200505_1226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='author_email',
        ),
        migrations.AddField(
            model_name='tweet',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
