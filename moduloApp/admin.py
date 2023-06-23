from django.contrib import admin
from moduloApp.models import *




# Register your models here.

admin.site.register(Proveedor)
admin.site.register(Sucursal)
admin.site.register(Mercancia)
admin.site.register(Categoria)
admin.site.register(EntradaMercancia)
admin.site.register(SalidaMercancia)
admin.site.register(HistorialEntrada)
admin.site.register(HistorialSalida)

