from django import forms
from .models import Evento, ConfiguracionEvento, GlobalConfig


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = [
            'nombre', 'tipo', 'ubicacion',
            'fecha_inicio', 'fecha_fin',
            'descripcion', 'max_asistentes', 'servicios',
        ]
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_fin':    forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'descripcion':  forms.Textarea(attrs={'rows': 3}),
            'servicios':    forms.CheckboxSelectMultiple(),
        }


class ConfiguracionEventoForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionEvento
        fields = [
            'tiene_catering', 'tiene_escenario', 'tiene_iluminacion',
            'tiene_seguridad', 'tiene_streaming', 'tiene_decoracion',
            'notas_adicionales',
        ]
        widgets = {
            'notas_adicionales': forms.Textarea(attrs={'rows': 3}),
        }


class GlobalConfigForm(forms.ModelForm):
    class Meta:
        model = GlobalConfig
        fields = [
            'moneda', 'porcentaje_impuestos',
            'limite_asistentes', 'notificaciones_activas',
            'modo_mantenimiento',
        ]


class BuildEventoForm(forms.Form):
    TIPO_CHOICES = [
        ('conferencia', 'Conference'),
        ('boda', 'Wedding'),
    ]
    CONFIG_CHOICES = [
        ('estandar',    'Standard'),
        ('completa',    'Complete'),
        ('personalizada', 'Custom'),
    ]
    nombre        = forms.CharField(max_length=200)
    tipo_builder  = forms.ChoiceField(choices=TIPO_CHOICES)
    configuracion = forms.ChoiceField(choices=CONFIG_CHOICES)
    ubicacion     = forms.CharField(max_length=200, required=False)
    fecha_inicio  = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    fecha_fin = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    max_asistentes  = forms.IntegerField(min_value=1, initial=100)
    descripcion     = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}), required=False
    )
    tiene_catering   = forms.BooleanField(required=False)
    tiene_escenario  = forms.BooleanField(required=False)
    tiene_iluminacion = forms.BooleanField(required=False)
    tiene_seguridad  = forms.BooleanField(required=False)
    tiene_streaming  = forms.BooleanField(required=False)
    tiene_decoracion = forms.BooleanField(required=False)


class CloneEventoForm(forms.Form):
    nombre       = forms.CharField(max_length=200, label="New Event Name")
    fecha_inicio = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="New Start Date"
    )
    fecha_fin = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="New End Date"
    )
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label="Description"
    )
    max_asistentes = forms.IntegerField(min_value=1, label="Max Attendees")