# Generated by Django 4.1.5 on 2023-01-19 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_appuser_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
