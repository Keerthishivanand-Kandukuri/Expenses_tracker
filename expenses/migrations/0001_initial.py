# Generated by Django 5.1.7 on 2025-03-25 07:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('full_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('total_budget', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('budget_remaining', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('category', models.CharField(choices=[('Food', 'Food'), ('Transport', 'Transport'), ('Shopping', 'Shopping'), ('Others', 'Others')], max_length=20)),
                ('description', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='expenses.user')),
            ],
        ),
    ]
