# Generated by Django 4.1 on 2022-11-24 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0005_postmodel_post_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmodel',
            name='post_name',
            field=models.CharField(default='', max_length=300),
        ),
    ]
