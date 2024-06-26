# Generated by Django 5.0.1 on 2024-04-22 17:03

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_age_remove_user_birth_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthenticationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=13, region=None, verbose_name='Номер телефона')),
                ('code', models.CharField(max_length=4, verbose_name='Код')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('is_activated', models.BooleanField(default=False, verbose_name='Активирован')),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_authorized',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='verification_code',
        ),
    ]
