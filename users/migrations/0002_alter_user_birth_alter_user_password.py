# Generated by Django 5.1.5 on 2025-02-20 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth',
            field=models.DateField(default='2000-01-01', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.TextField(max_length=20),
        ),
    ]
