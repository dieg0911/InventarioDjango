from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
#modulos reportlab
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from django.views.generic import View
from datetime import datetime




# Create your views here.

def index(request):
    return render(request, 'sistema/index.html')

#home
def home(request):
    return render(request, 'sistema/basehome.html')
#login y logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomAuthenticationForm

def loginuser(request):
    if request.method == 'GET':
        form = CustomAuthenticationForm()
    else:
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Usuario y/o contraseña incorrectos')  # Agregar error personalizado al formulario

    return render(request, 'login.html', {'form': form})


def logoutuser(request):
        logout(request)
        return redirect('login')

#registro de usuarios
@login_required
def registro(request):
    if not request.user.is_superuser:
        # Si el usuario no es un superusuario, redirige a otra vista o muestra un mensaje de error.
        return HttpResponse('Acceso denegado')

    if request.method == 'GET':
        return render(request, 'registro.html', {
            'form': CustomUserCreationForm()
        })
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Crear el usuario pero no guardarlo todavía
            user = form.save(commit=False)
            
            # Personalizar cualquier campo adicional del usuario si es necesario
            user.custom_field = 'valor_personalizado'

            # Guardar el usuario en la base de datos
            user.save()

            return redirect('home')
        else:
            return render(request, 'registro.html', {
                'form': form
            })
    else:
        return HttpResponse('Método de solicitud no válido')

#proveedores, crear y editar proveedores
@login_required
def proveedores(request):
    proveedores = Proveedor.objects.filter(activo=True)
    return render(request, 'sistema/proveedores.html', {'proveedores': proveedores})
#crear proveedor
@login_required
def crear_proveedor(request):
    if request.method == 'GET':
        return render(request, 'sistema/crear_proveedor.html', {'form': ProveedorForm()})
    else:
        try:
            form_proveedor = ProveedorForm(request.POST)
            if form_proveedor.is_valid():
                new_proveedor = form_proveedor.save(commit=False)
                new_proveedor.user = request.user
                new_proveedor.save()
                return redirect('proveedores')
            else:
                return render(request, 'sistema/crear_proveedor.html', {
                    'form': form_proveedor,
                    'error': 'Los datos no son válidos'
                })
        except Exception as e:
            return render(request, 'sistema/crear_proveedor.html', {
                'form': ProveedorForm,
                'error': 'Se produjo un error al guardar el proveedor'
            })
#detalle proveedor
@login_required       
def detalle_proveedor(request, proveedor_id):
    if request.method == 'GET':
        # proveedor = get_object_or_404(Proveedor, pk=proveedor_id, user=request.user) muestra proveedor creado por el usuario
        proveedor = get_object_or_404(Proveedor, pk=proveedor_id)
        form_proovedor = ProveedorForm(instance=proveedor)
        return render(request, 'sistema/detalle_proveedor.html', {'proveedor': proveedor, 'form': form_proovedor})
    else:
        try:
            proveedor = get_object_or_404(Proveedor, pk=proveedor_id,)
            form = ProveedorForm(request.POST, instance=proveedor)
            form.save()
            return redirect('proveedores')
        except ValueError:
            return render(request, 'sistema/detalle_proveedor.html', {'proveedor': proveedor, 'form': form, 'error': 'Los datos no son validos', 'error': 'No se puede editar este proveedor'
            })
#eliminar proveedor
@login_required
def eliminar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id)
    proveedor.delete()
    return redirect('proveedores')
#desactivar proveedor
@login_required
def desactivar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id)
    proveedor.activo = False
    proveedor.save()
    return redirect('proveedores')
#proveedores inactivos
@login_required
def proveedores_inactivos(request):
    proveedores = Proveedor.objects.filter(activo=False)
    return render(request, 'sistema/proveedores_inactivos.html', {'proveedores': proveedores})
#reingresar proveedor
@login_required
def reingresar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    proveedor.activo = True
    proveedor.save()
    return redirect('proveedores')

#sucursales, crear y editar sucursales
@login_required
def sucursales(request):
    sucursales = Sucursal.objects.filter(activo = True)  # Obtener todas las sucursales, tanto activas como inactivas
    return render(request, 'sistema/sucursales.html', {'sucursales': sucursales})
#crear sucursal
@login_required
def crear_sucursal(request):    
    if request.method == 'GET':
        return render(request, 'sistema/crear_sucursal.html', {
            'form': SucursalForm()
        })
    else:
        try:
            form_sucursal = SucursalForm(request.POST)
            if form_sucursal.is_valid():
                new_sucursal = form_sucursal.save(commit=False)
                new_sucursal.user = request.user
                new_sucursal.save()
                return redirect('sucursales')
            else:
                return render(request, 'sistema/crear_sucursal.html', {
                    'form': form_sucursal,
                    'error': 'Los datos no son válidos'
                })
        except Exception as e:
            return render(request, 'sistema/crear_sucursal.html', {
                'form': SucursalForm,
                'error': 'Se produjo un error al guardar la sucursal'
            })
#detalle sucursal
@login_required
def detalle_sucursal(request, sucursal_id):
    if request.method == 'GET':
        sucursal = get_object_or_404(Sucursal, pk=sucursal_id)
        form_sucursal = SucursalForm(instance=sucursal)
        return render(request, 'sistema/detalle_sucursal.html', {'sucursal': sucursal, 'form': form_sucursal})
    else:
        try:
            sucursal = get_object_or_404(Sucursal, pk=sucursal_id,)
            form = SucursalForm(request.POST, instance=sucursal)
            form.save()
            return redirect('sucursales')
        except ValueError:
            return render(request, 'sistema/detalle_sucursal.html', {'sucursal': sucursal, 'form': form, 'error': 'Los datos no son validos', 'error': 'No se puede editar esta sucursal'
            })
#eliminar sucursal
@login_required
def eliminar_sucursal(request, sucursal_id):
    sucursal = get_object_or_404(Sucursal, pk=sucursal_id)
    sucursal.delete()
    return redirect('sucursales')
#desactivar sucursal
@login_required
def desactivar_sucursal(request, sucursal_id):
    sucursal = get_object_or_404(Sucursal, pk=sucursal_id)
    sucursal.activo = False
    sucursal.save()
    return redirect('sucursales')
#sucursales inactivas
@login_required
def sucursales_inactivas(request):
    sucursales = Sucursal.objects.filter(activo=False)
    return render(request, 'sistema/sucursales_inactivas.html', {'sucursales': sucursales})
#reingresar sucursal
@login_required
def reingresar_sucursal(request, sucursal_id):
    sucursal = get_object_or_404(Sucursal, id=sucursal_id)
    sucursal.activo = True
    sucursal.save()
    return redirect('sucursales')


#mercania crear y editar mercancia
@login_required
def mercancias(request):
    mercancias = Mercancia.objects.filter(activo = True)  # Obtener todas las mercancias, tanto activas como inactivas
    return render(request, 'sistema/mercancias.html', {'mercancias': mercancias})
#crear mercancia
@login_required
def crear_mercancia(request):
    if request.method == 'GET':
        return render(request, 'sistema/crear_mercancia.html', {
            'form': MercanciaForm()
        })
    else:
        try:
            form_mercancia = MercanciaForm(request.POST)
            new_mercancia = form_mercancia.save(commit=False)
            new_mercancia.user = request.user
            new_mercancia.save()
            print(new_mercancia)
            return redirect('mercancias')
        except ValueError:
           return render(request, 'sistema/crear_mercancia.html', {
            'form': MercanciaForm,
            "error": "Los datos no son validos" 
            })
#detalle mercancia
@login_required
def detalle_mercancia(request, mercancia_id):
    if request.method == 'GET':
        mercancia = get_object_or_404(Mercancia, pk=mercancia_id)
        form_mercancia = MercanciaForm(instance=mercancia)
        return render(request, 'sistema/detalle_mercancia.html', {'mercancia': mercancia, 'form': form_mercancia})
    else:
        try:
            mercancia = get_object_or_404(Mercancia, pk=mercancia_id,)
            form = MercanciaForm(request.POST, instance=mercancia)
            form.save()
            return redirect('mercancias')
        except ValueError:
            return render(request, 'sistema/detalle_mercancia.html', {'mercancia': mercancia, 'form': form, 'error': 'Los datos no son validos', 'error': 'No se puede editar esta mercancia'
            })
#eliminar mercancia
@login_required
def eliminar_mercancia(request, mercancia_id):
    mercancia = get_object_or_404(Mercancia, pk=mercancia_id)
    mercancia.delete()
    return redirect('mercancias')
#desactivar mercancia
@login_required
def desactivar_mercancia(request, mercancia_id):
    mercancia = get_object_or_404(Mercancia, pk=mercancia_id)
    mercancia.activo = False
    mercancia.save()
    return redirect('mercancias')
#mercancias inactivas
@login_required
def mercancias_inactivas(request):
    mercancias = Mercancia.objects.filter(activo=False)
    return render(request, 'sistema/mercancias_inactivas.html', {'mercancias': mercancias})
#reingresar mercancia
@login_required
def reingresar_mercancia(request, mercancia_id):
    mercancia = get_object_or_404(Mercancia, id=mercancia_id)
    mercancia.activo = True
    mercancia.save()
    return redirect('mercancias')

#categorias crear y editar categorias
@login_required
def categorias(request):
    categorias = Categoria.objects.filter(activo = True)  # Obtener todas las categorias, tanto activas como inactivas
    return render(request, 'sistema/categorias.html', {'categorias': categorias})
#crear categoria
@login_required
def crear_categoria(request):
    if request.method == 'GET':
        return render(request, 'sistema/crear_categoria.html', {
            'form': CategoriaForm()
        })
    else:
        try:
            form_categoria = CategoriaForm(request.POST)
            new_categoria = form_categoria.save(commit=False)
            new_categoria.user = request.user
            new_categoria.save()
            print(new_categoria)
            return redirect('categorias')
        except ValueError:
           return render(request, 'sistema/crear_categoria.html', {
            'form': CategoriaForm,
            "error": "Los datos no son validos" 
            })
#detalle categoria
@login_required
def detalle_categoria(request, categoria_id):
    if request.method == 'GET':
        categoria = get_object_or_404(Categoria, pk=categoria_id)
        form_categoria = CategoriaForm(instance=categoria)
        return render(request, 'sistema/detalle_categoria.html', {'categoria': categoria, 'form': form_categoria})
    else:
        try:
            categoria = get_object_or_404(Categoria, pk=categoria_id,)
            form = CategoriaForm(request.POST, instance=categoria)
            form.save()
            return redirect('categorias')
        except ValueError:
            return render(request, 'sistema/detalle_categoria.html', {'categoria': categoria, 'form': form, 'error': 'Los datos no son validos', 'error': 'No se puede editar esta categoria'
            })
#eliminar categoria
@login_required
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    categoria.delete()
    return redirect('categorias')
#desactivar categoria
@login_required
def desactivar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    categoria.activo = False
    categoria.save()
    return redirect('categorias')
#categorias inactivas
@login_required
def categorias_inactivas(request):
    categorias = Categoria.objects.filter(activo=False)
    return render(request, 'sistema/categorias_inactivas.html', {'categorias': categorias})
#reingresar categoria
@login_required
def reingresar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.activo = True
    categoria.save()
    return redirect('categorias')

#entradas
@login_required
def entradas(request):
    entradas = EntradaMercancia.objects.all()
    return render(request, 'sistema/entradas.html', {'entradas': entradas})
@login_required
def crear_entrada(request):
    if request.method == 'GET':
        return render(request, 'sistema/crear_entrada.html', {
            'form': EntradaMercanciaForm()
        })
    else:
        try:
            form_entrada = EntradaMercanciaForm(request.POST)
            new_entrada = form_entrada.save(commit=False)
            new_entrada.user = request.user
            new_entrada.save()
            print(new_entrada)
            return redirect('entradas')
        except ValueError:
           return render(request, 'sistema/crear_entrada.html', {
            'form': EntradaMercanciaForm,
            "error": "Los datos no son validos" 
            })
@login_required
def eliminar_entrada(request, entrada_id):
    entrada = get_object_or_404(EntradaMercancia, pk=entrada_id)
    entrada.delete()
    return redirect('entradas')


#salidas de mercancia
@login_required
def salidas(request):
    salidas = SalidaMercancia.objects.all()
    return render(request, 'sistema/salidas.html', {'salidas': salidas})
@login_required
def crear_salida(request):
    if request.method == 'GET':
        return render(request, 'sistema/crear_salida.html', {
            'form': SalidaMercanciaForm()
        })
    else:
        try:
            form_salida = SalidaMercanciaForm(request.POST)
            new_salida = form_salida.save(commit=False)

            # Verificar si hay suficiente stock antes de guardar la salida
            if new_salida.mercancia.sustraer_stock(new_salida.cantidad):
                new_salida.user = request.user
                new_salida.save()
                return redirect('salidas')
            else:
                return render(request, 'sistema/crear_salida.html', {
                    'form': SalidaMercanciaForm(),
                    "error": "No hay suficiente stock disponible"
                })
        except ValueError:
           return render(request, 'sistema/crear_salida.html', {
            'form': SalidaMercanciaForm(),
            "error": "Los datos no son válidos" 
           })

@login_required
def eliminar_salida(request, salida_id):
    salida = get_object_or_404(SalidaMercancia, pk=salida_id)

    # Restaurar la cantidad de mercancía al eliminar la salida
    cantidad_restaurar = salida.cantidad
    mercancia = salida.mercancia
    mercancia.cantidad += cantidad_restaurar
    mercancia.save()

    salida.delete()
    return redirect('salidas')

#historial de entradas
@login_required
def historial_entradas(request):
    entradas = HistorialEntrada.objects.all()
    return render(request, 'sistema/historial_entradas.html', {'entradas': entradas})
@login_required
def eliminar_historial_entrada(request, historial_entrada_id):
    entrada = get_object_or_404(HistorialEntrada, pk=historial_entrada_id)
    entrada.delete()
    return redirect('historial_entradas')

#historial de salidas
@login_required
def historial_salidas(request):
    salidas = HistorialSalida.objects.all()
    return render(request, 'sistema/historial_salidas.html', {'salidas': salidas})
@login_required
def eliminar_historial_salida(request, historial_salida_id):
    salida = get_object_or_404(HistorialSalida, pk=historial_salida_id)
    salida.delete()
    return redirect('historial_salidas')

#devoluciones
@login_required
def devoluciones(request):
    devoluciones = DevolucionMercancia.objects.all()
    return render(request, 'sistema/devoluciones.html', {'devoluciones': devoluciones})
@login_required
def crear_devolucion(request):
    if request.method == 'POST':
        form = DevolucionMercanciaForm(request.POST)
        if form.is_valid():
            devolucion = form.save(commit=False)
            salida_mercancia = devolucion.salida_mercancia

            # Validar que la cantidad devuelta no exceda la cantidad originalmente salida
            if devolucion.cantidad_devuelta <= salida_mercancia.cantidad:
                salida_mercancia.cantidad -= devolucion.cantidad_devuelta
                salida_mercancia.save()

                mercancia = salida_mercancia.mercancia
                mercancia.cantidad += devolucion.cantidad_devuelta
                mercancia.save()

                devolucion.user = request.user
                devolucion.save()
                return redirect('devoluciones')  # Redirigir a la lista de devoluciones
            else:
                return render(request, 'sistema/crear_devolucion.html', {
                    'form': form,
                    "error": "La cantidad devuelta excede la cantidad originalmente salida"
                })
    else:
        form = DevolucionMercanciaForm()

    return render(request, 'sistema/crear_devolucion.html', {'form': form})
@login_required
def deshacer_devolucion(request, devolucion_id):
    devolucion = get_object_or_404(DevolucionMercancia, pk=devolucion_id)

    # Restaurar la cantidad devuelta a la salida de mercancía
    salida_mercancia = devolucion.salida_mercancia
    salida_mercancia.cantidad += devolucion.cantidad_devuelta
    salida_mercancia.save()

    # Restar la cantidad devuelta de la mercancía
    mercancia = salida_mercancia.mercancia
    mercancia.cantidad -= devolucion.cantidad_devuelta
    mercancia.save()

    # Eliminar la devolución
    devolucion.delete()

    return redirect('devoluciones')


#reportes
class GenerarReporteProveedoresView(View):
    def get(self, request):
        proveedores = Proveedor.objects.all()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_proveedores.pdf"'

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []

        # Estilo del título
        title_style = getSampleStyleSheet()['Title']
        title = Paragraph("Reporte de Proveedores", title_style)
        elements.append(title)

        # Estilo de la tabla
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        # Datos de la tabla
        data = [['ID', 'Código', 'Nombre', 'Dirección', 'Teléfono', 'Activo']]
        for proveedor in proveedores:
            data.append([proveedor.id, proveedor.codigo, proveedor.nombre, proveedor.direccion, proveedor.telefono, 'Sí' if proveedor.activo else 'No'])

        # Crear tabla
        table = Table(data)
        table.setStyle(style)
        elements.append(table)

        # Fecha de creación del reporte
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fecha_style = ParagraphStyle(name='FechaEstilo', fontSize=10, alignment=1, spaceAfter=20)
        fecha_creacion = Paragraph(f"Fecha de creación del reporte: {fecha_actual}", style=fecha_style)
        elements.append(fecha_creacion)


        # Construir el documento PDF
        doc.build(elements)

        return response

class GenerarReporteSucursalesView(View):
    def get(self, request):
        sucursales = Sucursal.objects.all()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_sucursales.pdf"'

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []

        # Estilo del título
        title_style = getSampleStyleSheet()['Title']
        title = Paragraph("Reporte de Proveedores", title_style)
        elements.append(title)

        # Estilo de la tabla
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        # Datos de la tabla
        data = [['ID','Nombre', 'Dirección', 'Teléfono', 'Responsable', 'Activo']]
        for sucursal in sucursales:
            data.append([sucursal.id, sucursal.nombre, sucursal.direccion, sucursal.telefono, sucursal.responsable, 'Sí' if sucursal.activo else 'No'])

        # Crear tabla
        table = Table(data)
        table.setStyle(style)
        elements.append(table)

        # Fecha de creación del reporte
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fecha_style = ParagraphStyle(name='FechaEstilo', fontSize=10, alignment=1, spaceAfter=20)
        fecha_creacion = Paragraph(f"Fecha de creación del reporte: {fecha_actual}", style=fecha_style)
        elements.append(fecha_creacion)


        # Construir el documento PDF
        doc.build(elements)

        return response
    
class GenerarReporteMercanciasView(View):
    def get(self, request):
        mercancias = Mercancia.objects.all()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_mercancias.pdf"'

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []

        # Estilo del título
        title_style = getSampleStyleSheet()['Title']
        title = Paragraph("Reporte de Mercancías", title_style)
        elements.append(title)

        # Estilo de la tabla
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        # Datos de la tabla
        data = [['ID', 'Código', 'Nombre', 'Valor Unitario', 'Cantidad', 'Categoría', 'Activo']]
        for mercancia in mercancias:
            data.append([mercancia.id, mercancia.codigo, mercancia.nombre, mercancia.valor_unitario, mercancia.cantidad, mercancia.categoria.nombre, 'Sí' if mercancia.activo else 'No'])

        # Crear tabla
        table = Table(data)
        table.setStyle(style)
        elements.append(table)

        # Fecha de creación del reporte
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fecha_style = ParagraphStyle(name='FechaEstilo', fontSize=10, alignment=1, spaceAfter=20)
        fecha_creacion = Paragraph(f"Fecha de creación del reporte: {fecha_actual}", style=fecha_style)
        elements.append(fecha_creacion)

        # Construir el documento PDF
        doc.build(elements)

        return response

class GenerarReporteCategoriasView(View):
    def get(self, request):
        categorias = Categoria.objects.all()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_categorias.pdf"'

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []

        # Estilo del título
        title_style = getSampleStyleSheet()['Title']
        title = Paragraph("Reporte de Categorías", title_style)
        elements.append(title)

        # Estilo de la tabla
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        # Datos de la tabla
        data = [['ID', 'Nombre', 'Descripción', 'Activo']]
        for categoria in categorias:
            data.append([categoria.id, categoria.nombre, categoria.descripcion, 'Sí' if categoria.activo else 'No'])

        # Crear tabla
        table = Table(data)
        table.setStyle(style)
        elements.append(table)

        # Fecha de creación del reporte
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fecha_style = ParagraphStyle(name='FechaEstilo', fontSize=10, alignment=1, spaceAfter=20)
        fecha_creacion = Paragraph(f"Fecha de creación del reporte: {fecha_actual}", style=fecha_style)
        elements.append(fecha_creacion)

        # Construir el documento PDF
        doc.build(elements)

        return response
    
class GenerarReporteEntradasView(View):
    def get(self, request):
        entradas = EntradaMercancia.objects.all()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_entradas.pdf"'

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []

        # Estilo del título
        title_style = getSampleStyleSheet()['Title']
        title = Paragraph("Reporte de Entradas", title_style)
        elements.append(title)

        # Estilo de la tabla
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        # Datos de la tabla
        data = [['ID', 'Mercancía', 'Proveedor', 'Cantidad', 'Fecha']]
        for entrada in entradas:
            data.append([entrada.id, entrada.mercancia.nombre, entrada.proveedor.nombre, entrada.cantidad, entrada.fecha])

        # Crear tabla
        table = Table(data)
        table.setStyle(style)
        elements.append(table)

        # Fecha de creación del reporte
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fecha_style = ParagraphStyle(name='FechaEstilo', fontSize=10, alignment=1, spaceAfter=20)
        fecha_creacion = Paragraph(f"Fecha de creación del reporte: {fecha_actual}", style=fecha_style)
        elements.append(fecha_creacion)

        # Construir el documento PDF
        doc.build(elements)

        return response

class GenerarReporteHistorialEntradasView(View):
    def get(self, request):
        historiales = HistorialEntrada.objects.all()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_historial_entrada.pdf"'

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []

        # Estilo del título
        title_style = getSampleStyleSheet()['Title']
        title = Paragraph("Reporte de Historial de Entrada", title_style)
        elements.append(title)

        # Estilo de la tabla
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        # Datos de la tabla
        data = [['ID', 'Mercancía', 'Cantidad', 'Fecha']]
        for historial in historiales:
            data.append([historial.id, historial.mercancia.nombre, historial.cantidad, historial.fecha.strftime('%Y-%m-%d %H:%M:%S')])

        # Crear tabla
        table = Table(data)
        table.setStyle(style)
        elements.append(table)

        # Fecha de creación del reporte
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fecha_style = ParagraphStyle(name='FechaEstilo', fontSize=10, alignment=1, spaceAfter=20)
        fecha_creacion = Paragraph(f"Fecha de creación del reporte: {fecha_actual}", style=fecha_style)
        elements.append(fecha_creacion)

        # Construir el documento PDF
        doc.build(elements)

        return response
    
class GenerarReporteSalidasView(View):
    def get(self, request):
        salidas = SalidaMercancia.objects.all()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_salidas.pdf"'

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []

        # Estilo del título
        title_style = getSampleStyleSheet()['Title']
        title = Paragraph("Reporte de Salidas de Mercancía", title_style)
        elements.append(title)

        # Estilo de la tabla
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        # Datos de la tabla
        data = [['ID', 'Mercancía', 'Sucursal', 'Cantidad', 'Fecha']]
        for salida in salidas:
            data.append([salida.id, salida.mercancia.nombre, salida.sucursal.nombre, salida.cantidad, salida.fecha.strftime('%Y-%m-%d %H:%M:%S')])

        # Crear tabla
        table = Table(data)
        table.setStyle(style)
        elements.append(table)

        # Fecha de creación del reporte
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fecha_style = ParagraphStyle(name='FechaEstilo', fontSize=10, alignment=1, spaceAfter=20)
        fecha_creacion = Paragraph(f"Fecha de creación del reporte: {fecha_actual}", style=fecha_style)
        elements.append(fecha_creacion)

        # Construir el documento PDF
        doc.build(elements)

        return response

class GenerarReporteHistorialSalidasView(View):
    def get(self, request):
        historiales = HistorialSalida.objects.all()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_historial_salida.pdf"'

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []

        # Estilo del título
        title_style = getSampleStyleSheet()['Title']
        title = Paragraph("Reporte de Historial de Salida de Mercancía", title_style)
        elements.append(title)

        # Estilo de la tabla
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        # Datos de la tabla
        data = [['ID', 'Mercancía', 'Cantidad', 'Fecha']]
        for historial in historiales:
            data.append([historial.id, historial.mercancia.nombre, historial.cantidad, historial.fecha.strftime('%Y-%m-%d %H:%M:%S')])

        # Crear tabla
        table = Table(data)
        table.setStyle(style)
        elements.append(table)

        # Fecha de creación del reporte
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fecha_style = ParagraphStyle(name='FechaEstilo', fontSize=10, alignment=1, spaceAfter=20)
        fecha_creacion = Paragraph(f"Fecha de creación del reporte: {fecha_actual}", style=fecha_style)
        elements.append(fecha_creacion)

        # Construir el documento PDF
        doc.build(elements)

        return response

class GenerarReporteDevolucionesView(View):
    def get(self, request):
        devoluciones = DevolucionMercancia.objects.all()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_devoluciones.pdf"'

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []

        # Estilo del título
        title_style = getSampleStyleSheet()['Title']
        title = Paragraph("Reporte de Devoluciones de Mercancía", title_style)
        elements.append(title)

        # Estilo de la tabla
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

        # Datos de la tabla
        data = [['ID', 'Salida de Mercancía', 'Cantidad Devuelta', 'Fecha']]
        for devolucion in devoluciones:
            data.append([devolucion.id, devolucion.salida_mercancia.id, devolucion.cantidad_devuelta, devolucion.fecha.strftime('%Y-%m-%d %H:%M:%S')])

        # Crear tabla
        table = Table(data)
        table.setStyle(style)
        elements.append(table)

        # Fecha de creación del reporte
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fecha_style = ParagraphStyle(name='FechaEstilo', fontSize=10, alignment=1, spaceAfter=20)
        fecha_creacion = Paragraph(f"Fecha de creación del reporte: {fecha_actual}", style=fecha_style)
        elements.append(fecha_creacion)

        # Construir el documento PDF
        doc.build(elements)

        return response
