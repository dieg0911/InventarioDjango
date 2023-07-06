from django import forms
from django.forms import ModelForm
from .models import Proveedor, Sucursal, Mercancia, EntradaMercancia, SalidaMercancia, Categoria
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ('codigo', 'nombre', 'direccion', 'telefono')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo'].widget.attrs.update({'class': 'form-control'})
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control'})
        self.fields['telefono'].widget.attrs.update({'class': 'form-control'})


class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ('nombre', 'direccion', 'telefono', 'responsable')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion'].widget.attrs.update({'class': 'form-control'})
        self.fields['telefono'].widget.attrs.update({'class': 'form-control'})
        self.fields['responsable'].widget.attrs.update({'class': 'form-control'})

class MercanciaForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.filter(activo=True))

    class Meta:
        model = Mercancia
        fields = ['categoria', 'codigo', 'nombre', 'valor_unitario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['codigo'].widget.attrs.update({'class': 'form-control'})
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['valor_unitario'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        # Resto del código de validación si es necesario
        return cleaned_data

class EntradaMercanciaForm(forms.ModelForm):
    mercancia = forms.ModelChoiceField(queryset=Mercancia.objects.filter(activo=True))
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.filter(activo=True))
    class Meta:
        model = EntradaMercancia
        fields = ['mercancia', 'proveedor', 'cantidad']

    def __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['mercancia'].widget.attrs.update({'class': 'form-control'})
        self.fields['proveedor'].widget.attrs.update({'class': 'form-control'})
        self.fields['cantidad'].widget.attrs.update({'class': 'form-control'})

class SalidaMercanciaForm(forms.ModelForm):
    class Meta:
        model = SalidaMercancia
        fields = ['mercancia', 'sucursal', 'cantidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['mercancia'].widget.attrs.update({'class': 'form-control'})
        self.fields['sucursal'].widget.attrs.update({'class': 'form-control'})
        self.fields['cantidad'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        mercancia = cleaned_data.get('mercancia')
        cantidad = cleaned_data.get('cantidad')

        if mercancia and cantidad:
            if cantidad > mercancia.cantidad:
                self.add_error('cantidad', 'No hay suficiente stock disponible, solo hay {} unidades disponibles'.format(mercancia.cantidad))

        return cleaned_data

class DevolucionForm(forms.ModelForm):
    class Meta:
        model = SalidaMercancia
        fields = ['mercancia', 'sucursal', 'cantidad']
    
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control'})

# class RegistroCantidadForm(forms.Form):
#     cantidad = forms.IntegerField(label='Cantidad', min_value=1)

class RegistroEntradaForm(forms.Form):
    mercancia = forms.ModelChoiceField(queryset=Mercancia.objects.filter(activo=True))
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.filter(activo=True))
    cantidad = forms.IntegerField(label='Cantidad', min_value=1)

class RegistroSalidaForm(forms.Form):
    mercancia = forms.ModelChoiceField(queryset=Mercancia.objects.filter(activo=True))
    sucursal = forms.ModelChoiceField(queryset=Sucursal.objects.filter(activo=True))
    cantidad = forms.IntegerField(label='Cantidad', min_value=1)
    fecha = forms.DateField(label='Fecha', widget=forms.SelectDateWidget())