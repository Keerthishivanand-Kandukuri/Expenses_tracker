# Generated by Django 5.1.7 on 2025-03-25 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_registerd_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registerd_user',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
