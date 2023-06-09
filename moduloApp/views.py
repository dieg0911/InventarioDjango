from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import ProveedorForm, SucursalForm
from .models import Proveedor, Sucursal
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request, 'sistema/index.html')

#home
def home(request):
    return render(request, 'sistema/basehome.html')

#login y logout
def loginuser(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm()
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm(),
                'error': 'Usuario y/o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('home')
        
def logoutuser(request):
        logout(request)
        return redirect('login')

#registro de usuarios
@login_required
def registro(request):
    if request.method == 'GET':
        return render(request, 'registro.html', {
            'form': UserCreationForm()
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('proveedores')
            except IntegrityError:
                return render(request, 'registro.html', {
                    'form': UserCreationForm,
                    "error": "El usuario ya existe"
                })
        return render(request, 'registro.html', {
            'form': UserCreationForm,
            "error": "Las contraseñas no coinciden"
        })

#proveedores, crear y editar proveedores
@login_required
def proveedores(request):
    Proveedor.objects.all()
    return render(request, 'sistema/proveedores.html', {'proveedores': Proveedor.objects.all()})

@login_required
def crear_proveedor(request):
    if request.method == 'GET':
        return render(request, 'sistema/crear_proveedor.html', {
            'form': ProveedorForm()
        })
    else:
        # form_proovedor = ProveedorForm(request.POST)
        # print(form_proovedor)
        try:
            form_proovedor = ProveedorForm(request.POST)
            new_proveedor = form_proovedor.save(commit=False)
            new_proveedor.user = request.user
            new_proveedor.save()
            print(new_proveedor)
            return redirect('proveedores')
        except ValueError:
           return render(request, 'sistema/crear_proveedor.html', {
            'form': ProveedorForm,
            "error": "Los datos no son validos" 
            })

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

@login_required
def eliminar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id)
    proveedor.delete()
    return redirect('proveedores')

#sucursales, crear y editar sucursales
@login_required
def sucursales(request):
    Sucursal.objects.all()
    return render(request, 'sistema/sucursales.html', {'sucursales': Sucursal.objects.all()})
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
            new_sucursal = form_sucursal.save(commit=False)
            new_sucursal.user = request.user
            new_sucursal.save()
            print(new_sucursal)
            return redirect('sucursales')
        except ValueError:
           return render(request, 'sistema/crear_sucursal.html', {
            'form': SucursalForm,
            "error": "Los datos no son validos" 
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