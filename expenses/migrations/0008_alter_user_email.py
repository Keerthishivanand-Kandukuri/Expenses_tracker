# Generated by Django 5.1.7 on 2025-03-26 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0007_alter_user_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default='Update_your_email@gmail.com', max_length=50),
        ),
    ]
