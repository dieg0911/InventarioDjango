# Generated by Django 4.1.7 on 2023-06-20 01:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moduloApp', '0007_sucursal_activo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='mercancia',
            name='categoria',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='moduloApp.categoria'),
        ),
    ]
