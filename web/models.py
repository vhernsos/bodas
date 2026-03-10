from django.db import models
from django.contrib.auth.models import User


class TipoEvento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Ubicacion(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} - {self.ciudad}"


class Servicio(models.Model):
    CATEGORIA_CHOICES = [
        ('catering', 'Catering'),
        ('escenario', 'Stage'),
        ('iluminacion', 'Lighting'),
        ('seguridad', 'Security'),
        ('streaming', 'Streaming'),
        ('decoracion', 'Decoration'),
        ('otro', 'Other'),
    ]
    nombre = models.CharField(max_length=200)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()})"


class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    tipo = models.ForeignKey(TipoEvento, on_delete=models.SET_NULL, null=True)
    ubicacion = models.ForeignKey(
        Ubicacion, on_delete=models.SET_NULL, null=True, blank=True
    )
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    descripcion = models.TextField(blank=True)
    max_asistentes = models.PositiveIntegerField(default=100)
    organizador = models.ForeignKey(User, on_delete=models.CASCADE)
    servicios = models.ManyToManyField(Servicio, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    es_clon = models.BooleanField(default=False)
    evento_original = models.ForeignKey(
        'self', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='clones'
    )

    def __str__(self):
        return self.nombre


class ConfiguracionEvento(models.Model):
    evento = models.OneToOneField(
        Evento, on_delete=models.CASCADE, related_name='configuracion'
    )
    tiene_catering = models.BooleanField(default=False)
    tiene_escenario = models.BooleanField(default=False)
    tiene_iluminacion = models.BooleanField(default=False)
    tiene_seguridad = models.BooleanField(default=False)
    tiene_streaming = models.BooleanField(default=False)
    tiene_decoracion = models.BooleanField(default=False)
    notas_adicionales = models.TextField(blank=True)

    def __str__(self):
        return f"Config - {self.evento.nombre}"


class PlantillaEvento(models.Model):
    nombre = models.CharField(max_length=200)
    evento_base = models.ForeignKey(
        Evento, on_delete=models.CASCADE, related_name='plantillas'
    )
    descripcion = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class GlobalConfig(models.Model):
    """Database-backed storage for the Singleton pattern."""
    moneda = models.CharField(max_length=10, default='USD')
    porcentaje_impuestos = models.DecimalField(
        max_digits=5, decimal_places=2, default=16.00
    )
    limite_asistentes = models.PositiveIntegerField(default=5000)
    notificaciones_activas = models.BooleanField(default=True)
    modo_mantenimiento = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Global Configuration'

    def save(self, *args, **kwargs):
        self.pk = 1                   # enforce single row
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Global Configuration"