# Generated by Django 4.1.5 on 2023-01-16 05:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='make',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='make', to='cars.make', to_field='brand'),
        ),
        migrations.AlterField(
            model_name='make',
            name='brand',
            field=models.CharField(max_length=200, unique=True, verbose_name='Brand Name'),
        ),
    ]
