# Generated by Django 4.1.7 on 2023-06-20 01:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moduloApp', '0008_categoria_mercancia_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mercancia',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='moduloApp.categoria'),
        ),
    ]