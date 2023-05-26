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
    path('logout/', logoutuser, name='logout'),
    # path('login/', loginuser, name='login'),
]
