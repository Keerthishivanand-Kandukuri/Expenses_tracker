# Generated by Django 5.1.7 on 2025-03-26 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0004_user_user_alter_expenses_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default='Update your email', max_length=50),
        ),
    ]
