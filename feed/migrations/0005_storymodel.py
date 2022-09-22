# Generated by Django 4.1 on 2022-09-11 18:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0004_postmodel_like_alter_postmodel_post_creator'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('story_image', models.ImageField(upload_to='story_image/')),
                ('create_by', models.DateTimeField(auto_now_add=True)),
                ('story_creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='story_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
