# Generated by Django 4.1.7 on 2023-06-21 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moduloApp', '0013_mercancia_cantidad_registrocantidad_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrocantidad',
            name='cantidad',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='registrocantidad',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]