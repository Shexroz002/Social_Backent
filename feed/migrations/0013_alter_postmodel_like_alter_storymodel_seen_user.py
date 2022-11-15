# Generated by Django 4.1 on 2022-11-13 09:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0012_storymodel_seen_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='like',
            field=models.ManyToManyField(related_name='like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='storymodel',
            name='seen_user',
            field=models.ManyToManyField(related_name='seen_user', to=settings.AUTH_USER_MODEL),
        ),
    ]