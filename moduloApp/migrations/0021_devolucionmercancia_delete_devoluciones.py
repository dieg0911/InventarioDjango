# Generated by Django 4.1.7 on 2023-07-06 06:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('moduloApp', '0020_devoluciones_alter_proveedor_nombre_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DevolucionMercancia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_devuelta', models.PositiveIntegerField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('salida_mercancia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moduloApp.salidamercancia')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Devoluciones',
        ),
    ]