from typing import Any, Dict, Tuple
from django.db import models, transaction
from django.db.models import Sum
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MaxLengthValidator

# Create your models here.


class Proveedor(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100, unique=True)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+\d{1,11}$',
                message='El número de teléfono debe comenzar con "+" y tener un máximo de 11 dígitos.'
            )
        ]
    )
    activo = models.BooleanField(default=True)
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre


class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+\d{1,11}$',
                message='El número de teléfono debe comenzar con "+" y tener un máximo de 11 dígitos.'
            )
        ]
    )
    responsable = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre 


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Mercancia(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    valor_unitario = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def total_cantidad_salidas(self):
        return self.salidamercancia_set.aggregate(total=Sum('cantidad'))['total'] or 0

    def agregar_stock(self, cantidad):
        cantidad_actual = self.cantidad
        # Sumar la cantidad ingresada al valor actual
        self.cantidad = cantidad_actual + int(cantidad)
        self.save()
        HistorialEntrada.objects.create(mercancia=self, cantidad=cantidad)

    def sustraer_stock(self, cantidad):
        if self.cantidad >= cantidad:
            self.cantidad -= cantidad
            self.save()
            HistorialSalida.objects.create(mercancia=self, cantidad=cantidad)
            
            return True  # Agregar esta línea para indicar que la sustracción se realizó correctamente
        else:
            return False  # Agregar esta línea para indicar que no hay suficiente stock

        return False 


class HistorialEntrada(models.Model):
    mercancia = models.ForeignKey(Mercancia, on_delete=models.CASCADE)
    # Proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Historial de Entrada {self.id} - {self.mercancia.nombre}"


class EntradaMercancia(models.Model):
    mercancia = models.ForeignKey(Mercancia, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        is_new_entry = self.pk is None  # Verificar si es una entrada nueva o existente

        super().save(*args, **kwargs)

        if is_new_entry:
            self.mercancia.agregar_stock(self.cantidad)

    def delete(self, *args, **kwargs):
        self.mercancia.sustraer_stock(self.cantidad)
        super().delete(*args, **kwargs)


class HistorialSalida(models.Model):
    mercancia = models.ForeignKey(Mercancia, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Registro de Salida {self.id} - {self.mercancia.nombre}"


class SalidaMercancia(models.Model):
    mercancia = models.ForeignKey(Mercancia, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id)


class DevolucionMercancia(models.Model):
    salida_mercancia = models.ForeignKey(SalidaMercancia, on_delete=models.CASCADE)
    cantidad_devuelta = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id) + " - " + self.salida_mercancia.mercancia.nombre
    
