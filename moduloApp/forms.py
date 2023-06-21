from django import forms
from django.forms import ModelForm
from .models import Proveedor, Sucursal, Mercancia, EntradaMercancia, SalidaMercancia, Categoria

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['codigo', 'nombre', 'direccion', 'telefono']

class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ['nombre', 'direccion', 'telefono', 'responsable']

class MercanciaForm(forms.ModelForm):
    class Meta:
        model = Mercancia
        fields = ['nombre', 'codigo', 'valor_unitario', 'categoria']

class EntradaMercanciaForm(forms.ModelForm):
    class Meta:
        model = EntradaMercancia
        fields = ['mercancia', 'proveedor', 'cantidad']

class SalidaMercanciaForm(forms.ModelForm):
    class Meta:
        model = SalidaMercancia
        fields = ['mercancia', 'sucursal', 'cantidad']

class DevolucionForm(forms.ModelForm):
    class Meta:
        model = SalidaMercancia
        fields = ['mercancia', 'sucursal', 'cantidad']
    
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']

class RegistroCantidadForm(forms.Form):
    cantidad = forms.IntegerField(label='Cantidad', min_value=1)