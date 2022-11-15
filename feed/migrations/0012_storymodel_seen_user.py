# Generated by Django 4.1 on 2022-10-13 17:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0011_favoriteposts'),
    ]

    operations = [
        migrations.AddField(
            model_name='storymodel',
            name='seen_user',
            field=models.ManyToManyField(blank=True, null=True, related_name='seen_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
