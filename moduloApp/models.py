from typing import Any, Dict, Tuple
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Proveedor(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre #+ ' ' + self.user.username

    
class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    responsable = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)

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
    
    def agregar_stock(self, cantidad):
        cantidad_actual = self.cantidad
        self.cantidad = cantidad_actual + int(cantidad)  # Sumar la cantidad ingresada al valor actual
        self.save()
        HistorialEntrada.objects.create(mercancia=self, cantidad=cantidad)

    def sustraer_stock(self, cantidad):
        if self.cantidad >= cantidad:
            self.cantidad -= cantidad
            self.save()
            RegistroSalida.objects.create(mercancia=self, cantidad=cantidad)
            
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

class RegistroSalida(models.Model):
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



class Devolucion(models.Model):
    mercancia = models.ForeignKey(Mercancia, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()    
    fecha = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.mercancia.nombre