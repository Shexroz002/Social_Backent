# Generated by Django 4.1 on 2022-09-07 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmodel',
            name='update_by',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='postmodel',
            name='create_by',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
