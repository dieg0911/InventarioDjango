"""inventario URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # Importamos include
from moduloApp.views import * # Importamos todas las vistas de moduloApp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', loginuser, name='login'),
    path('home/', home, name='home'),
    path('registro/', registro, name='registro'),
    #proveedores
    path('proveedores/', proveedores, name='proveedores'),
    path('proveedores/crear/', crear_proveedor, name='crear_proveedor'),
    path('proveedores/<int:proveedor_id>/', detalle_proveedor, name='detalle_proveedor'),
    path('proveedores/eliminar/<int:proveedor_id>', eliminar_proveedor, name='eliminar_proveedor'),
    path('proveedores/inactivos/', proveedores_inactivos, name='proveedores_inactivos'),
    path('proveedores/reingresar/<int:proveedor_id>/', reingresar_proveedor, name='reingresar_proveedor'),
    path('proveedores/desactivar/<int:proveedor_id>/', desactivar_proveedor, name='desactivar_proveedor'),


    path('logout/', logoutuser, name='logout'),
    # path('login/', loginuser, name='login'),
    #sucursales
    path('sucursales/', sucursales, name='sucursales'),
    path('sucursales/crear/', crear_sucursal, name='crear_sucursal'),
    path('sucursales/<int:sucursal_id>/', detalle_sucursal, name='detalle_sucursal'),
    path('sucursales/eliminar/<int:sucursal_id>', eliminar_sucursal, name='eliminar_sucursal'),
    path('sucursales/inactivos/', sucursales_inactivas, name='sucursales_inactivas'),
    path('sucursales/reingresar/<int:sucursal_id>/', reingresar_sucursal, name='reingresar_sucursal'),
    path('sucursales/desactivar/<int:sucursal_id>/', desactivar_sucursal, name='desactivar_sucursal'),

    #mercancias
    path('mercancias/', mercancias, name='mercancias'),
    path('mercancias/crear/', crear_mercancia, name='crear_mercancia'),
    path('mercancias/<int:mercancia_id>/', detalle_mercancia, name='detalle_mercancia'),
    path('mercancias/eliminar/<int:mercancia_id>', eliminar_mercancia, name='eliminar_mercancia'),
    path('mercancias/inactivos/', mercancias_inactivas, name='mercancias_inactivas'),
    path('mercancias/reingresar/<int:mercancia_id>/', reingresar_mercancia, name='reingresar_mercancia'),
    path('mercancias/desactivar/<int:mercancia_id>/', desactivar_mercancia, name='desactivar_mercancia'),

    #categorias
    path('categorias/', categorias, name='categorias'),
    path('categorias/crear/', crear_categoria, name='crear_categoria'),
    path('categorias/<int:categoria_id>/', detalle_categoria, name='detalle_categoria'),
    path('categorias/eliminar/<int:categoria_id>', eliminar_categoria, name='eliminar_categoria'),
    path('categorias/inactivos/', categorias_inactivas, name='categorias_inactivas'),
    path('categorias/reingresar/<int:categoria_id>/', reingresar_categoria, name='reingresar_categoria'),
    path('categorias/desactivar/<int:categoria_id>/', desactivar_categoria, name='desactivar_categoria'),

    #entradas
    path('entradas/', entradas, name='entradas'),
    path('entradas/crear/', crear_entrada, name='crear_entrada'),
    # path('entradas/<int:entrada_id>/', detalle_entrada, name='detalle_entrada'),
    path('entradas/eliminar/<int:entrada_id>', eliminar_entrada, name='eliminar_entrada'),
    # path('entradas/inactivos/', entradas_inactivas, name='entradas_inactivas'),
    # path('entradas/reingresar/<int:entrada_id>/', reingresar_entrada, name='reingresar_entrada'),
    # path('entradas/desactivar/<int:entrada_id>/', desactivar_entrada, name='desactivar_entrada'),
    
    #historial de entradas
    path('historial_entradas/', historial_entradas, name='historial_entradas'),
    # path('historial_entradas/crear/', crear_historial_entrada, name='crear_historial_entrada'),
    # path('historial_entradas/<int:historial_entrada_id>/', detalle_historial_entrada, name='detalle_historial_entrada'),
    path('historial_entradas/eliminar/<int:historial_entrada_id>', eliminar_historial_entrada, name='eliminar_historial_entrada'),
    #salidas
    path('salidas/', salidas, name='salidas'),
    path('salidas/crear/', crear_salida, name='crear_salida'),
    # path('salidas/<int:salida_id>/', detalle_salida, name='detalle_salida'),
    path('salidas/eliminar/<int:salida_id>', eliminar_salida, name='eliminar_salida'),
    #path('salidas/', salidas, name='salidas'),

 

]