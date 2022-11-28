# Generated by Django 4.1 on 2022-11-22 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_remove_postmodel_post_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmodel',
            name='post_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_type', to='feed.booktype'),
        ),
    ]
