# Generated by Django 4.1.7 on 2023-06-20 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moduloApp', '0011_remove_mercancia_cantidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='RegistroCantidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('mercancia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moduloApp.mercancia')),
            ],
        ),
    ]
